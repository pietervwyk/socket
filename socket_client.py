import RPi.GPIO as GPIO
import socket
import LTR390
import time
import struct

HOST = "192.168.137.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
    

def start_sensors():
    uv_sensor = LTR390.LTR390()
    uv_sensor.SetIntVal(5, 20)
    time.sleep(1)
    try:
        while True:
            print(uv_sensor.UVS())
            s.send(str(uv_sensor.UVS()).encode('utf8'))
#             s.send(bytes("Message from client.", "utf-8"))   
            time.sleep(0.5)
    except KeyboardInterrupt:
        exit()

start_sensors()