import RPi.GPIO as GPIO
import socket
import LTR390
import dht22
import time
import struct
import random
import ANEMOMETER

# HOST = "192.168.137.1"  # The server's hostname or IP address
# HOST = '192.168.0.101'
HOST = "127.0.0.1"
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
    

def start_sensors():
    uv_sensor = LTR390.LTR390()
    dht_sensor = dht22.DHT22()
    uv_sensor.SetIntVal(5, 20)
    wind_sensor = ANEMOMETER.ANEMOMETER()
    time.sleep(1)
    try:
        while True:
            sensors = []
            sensors.append(str(wind_sensor.get_wind_speed()))
            sensors.append(str(dht_sensor.get_temperature()))
            sensors.append(str(dht_sensor.get_humidity()))
            sensors.append(str(uv_sensor.UVS()))
            message = ",".join(sensors)
            print(message)
            s.send(message.encode('utf8'))    
            time.sleep(5*60)
    except KeyboardInterrupt:
        exit()
        
def start_random():
    try:
        while True:
            val = random.randint(3, 9)
            print(val)
            s.send(str(val).encode('utf8'))    
            time.sleep(2)
    except KeyboardInterrupt:
        exit()

start_sensors()
#start_random()
