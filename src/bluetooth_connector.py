import serial
import datetime
import json
import time
from databases import Database
from .logger import logger

class BluetoothConnector:
    port='COM10'
    baudrate=115200
    serialPort: serial.Serial
    db: Database
    def __init__(self, db: Database, port='COM10', baudrate=115200) -> None:
        self.port=port
        self.baudrate=baudrate
        self.db = db
        

    def start_connection(self):
        while 1:
            try:
                self.serialPort = serial.Serial(
                    port=self.port, baudrate=self.baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
                    )
            except serial.SerialException as e:
                logger.error(f'Não foi possível conectar ao bluetooth na porta {self.port}. Tentando novamente em 10 seg')
                logger.error(e)
                time.sleep(10)
                continue
            break
        logger.info(f'Bluetooth conectado com sucesso na porta {self.port}')

    def write_bluetooth(self, data: str):
        bin_data =  bytes(data.encode('utf-8'))
        logger.info(f'Escrevendo na {self.port}: {bin_data}')
        res = self.serialPort.write(bin_data)
        return res 

    async def get_current_percurso(self):
        data = await self.db.fetch_one("SELECT idPercurso FROM percurso WHERE ativo = 1;")
        if data is None:
            logger.info('Nenhum percurso encontrado')
            return None
        return data['idPercurso']

    async def save_telemetria_in_db(self, telemetria):
        idPercurso = await self.get_current_percurso()
        if idPercurso is None:
            logger.info('Nenhum percurso ativo no momento. Ignorando registro de telemetria')
            return

        logger.info(f'{idPercurso}, {telemetria}')
        sql = f"""INSERT INTO telemetria (idPercurso, distTotal, posX, posY, velocidade, aceleracao, corrente, energia, data) VALUES 
        ({idPercurso}, {telemetria['distTotal']}, {telemetria['posX']}, {telemetria['posY']}, {telemetria['velocidade']}, {telemetria['aceleracao']}, {telemetria['corrente']}, {telemetria['energia']}, '{telemetria['data']}')"""
        # print(sql)
        await self.db.execute(sql)
        logger.info('Registro Telemetria inserido no banco')

    async def finish_percurso(self):
        logger.info("Percurso Finalizado")
        active_percurso_id = await self.get_current_percurso()
        if active_percurso_id is None:
            logger.info("Nenhum percurso ativo no momento, ignorando comando de inativação")
            return
        await self.db.execute(f"UPDATE percurso SET ativo = 0 WHERE idPercurso = {active_percurso_id}")


    async def read_bluetooth(self):
        logger.info("Processo de leitura de bluetooth iniciado.")

        # TODO: INSEIRIR SerialException para tratar caso de desconexão.
        try:
            while 1:
                time.sleep(0.05)
                if self.serialPort.in_waiting > 0:
                    data_recieved = self.serialPort.readline()
                    print(f"data_recieved: {data_recieved}")
                    data_recieved = json.loads(data_recieved)
                    if "evento" in data_recieved:
                        data_recieved = None
                        await self.finish_percurso()
                        continue
                    data_recieved['data'] = datetime.datetime.now().isoformat()
                    # print(car_record)
                    await self.save_telemetria_in_db(data_recieved)
                    continue
        except serial.SerialException as e:
            logger.error(e)
            logger.info("Dispositivo desconectado.")
        


if __name__ == '__main__':
    DATABASE_URL="sqlite:///./katiau.db"
    db = Database(DATABASE_URL) 
    import asyncio
    bt_conn = BluetoothConnector(db)
    bt_conn.start_connection()
    asyncio.run(bt_conn.read_bluetooth())