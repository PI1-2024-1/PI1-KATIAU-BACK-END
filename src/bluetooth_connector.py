import serial
import datetime
import json
from databases import Database
# import socket
# sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# baddr = 'fc:b4:67:8c:85:fa'
# channel = 4

def write_bluetooth(data: bytes):
    serialPort = serial.Serial(
        port="COM9", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    serialPort.write(data)




async def get_current_percurso(db:Database):
    return await db.execute("SELECT idPercurso FROM percurso ORDER BY idPercurso DESC LIMIT 1;")

async def save_telemetria_in_db(db: Database, telemetria):
    idPercurso = get_current_percurso(db)

    
    sql = f"""INSERT INTO telemetria (idPercurso, distTotal, posX, posY, velocidade, aceleracao, corrente, energia, data) VALUES 
    ({idPercurso}, {telemetria['distTotal']}, {telemetria['posX']}, {telemetria['posY']}, {telemetria['velocidade']}, {telemetria['aceleracao']}, {telemetria['corrente']}, {telemetria['energia']}, {telemetria['data']})"""
    await db.execute(sql)


async def read_bluetooth(db: Database):
    serialPort = serial.Serial(
        port="COM10", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    while 1:
        if serialPort.in_waiting > 0:
            data_recieved = serialPort.readline()
            car_record = json.loads(data_recieved)
            car_record['data'] = datetime.datetime.now().isoformat()
            print(car_record)
            await save_telemetria_in_db(db, car_record)
            continue


if __name__ == '__main__':
    read_bluetooth()