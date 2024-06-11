import serial
import datetime
import json

# import socket
# sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# baddr = 'fc:b4:67:8c:85:fa'
# channel = 4


def read_bluetooth():
    serialPort = serial.Serial(
        port="COM10", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    while 1:
        if serialPort.in_waiting > 0:
            data_recieved = serialPort.readline()
            car_record = json.loads(data_recieved)
            car_record['date'] = datetime.datetime.now().isoformat()
            print(car_record)
            
            continue


if __name__ == '__main__':
    read_bluetooth()