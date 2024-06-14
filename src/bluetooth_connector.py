import serial
import datetime
import json
import time
from databases import Database
import logging
logger = logging.getLogger('Katiau')
def write_bluetooth(data: bytes):
    serialPort = serial.Serial(
        port="COM9", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    logger.info(f'Escrevendo na COM9: {data}')
    return serialPort.write(data)




async def get_current_percurso(db:Database):
    data = await db.fetch_one("SELECT idPercurso FROM percurso ORDER BY idPercurso DESC LIMIT 1;")
    # print('idPercurso: ', data['idPercurso'])
    return data['idPercurso']

async def save_telemetria_in_db(db: Database, telemetria):
    idPercurso = await get_current_percurso(db)

    logger.info(f'{idPercurso}, {telemetria}')
    sql = f"""INSERT INTO telemetria (idPercurso, distTotal, posX, posY, velocidade, aceleracao, corrente, energia, data) VALUES 
    ({idPercurso}, {telemetria['distTotal']}, {telemetria['posX']}, {telemetria['posY']}, {telemetria['velocidade']}, {telemetria['aceleracao']}, {telemetria['corrente']}, {telemetria['energia']}, '{telemetria['data']}')"""
    # print(sql)
    await db.execute(sql)
    logger.info('Registro Telemetria inserido no banco')


async def read_bluetooth(db: Database):
    logger.info("Processo de leitura de bluetooth iniciado.")
    port = "COM10"
    while 1:
        try:
            serialPort = serial.Serial(
                port=port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
            )
        except serial.SerialException:
            logger.error(f'Não foi possível conectar ao bluetooth na porta {port}. Tentando novamente em 10 seg')
            time.sleep(10)
            continue
        break

    logger.info(f'Bluetooth conectado com sucesso na porta {port}')

    while 1:
        time.sleep(0.1)
        if serialPort.in_waiting > 0:
            data_recieved = serialPort.readline()
            car_record = json.loads(data_recieved)
            car_record['data'] = datetime.datetime.now().isoformat()
            # print(car_record)
            await save_telemetria_in_db(db, car_record)
            continue


if __name__ == '__main__':
    DATABASE_URL="sqlite:///./katiau.db"
    db = Database(DATABASE_URL) 
    import asyncio
    asyncio.run(read_bluetooth(db))