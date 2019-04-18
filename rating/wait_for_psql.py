import socket
import time
import os

print('waiting for POSTGRESQL')

port = int(os.getenv('POSTGRES_PORT', '5432'))
host = os.getenv('POSTGRES_HOST', 'db')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        print('DB is listening. start connection')
        break
    except socket.error as ex:
        print('DB is not listening. waiting')
        time.sleep(0.5)
