import time
import board
import adafruit_dht



class DHT22:
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)
        self.prev_temperature = None
        self.counter = 0
        
    def get_temperature(self):
        try:
            temperature = self.dhtDevice.temperature
            self.prev_temperature = temperature
            self.counter = 0
            return temperature
        except RuntimeError as error:
            print(error.args[0])
            self.counter += 1
            if (self.counter < 3 and self.prev_temperature != None):
                return self.prev_temperature
            return None
    
    def get_humidity(self):
        try:
            humidity = self.dhtDevice.humidity
            return humidity
        except RuntimeError as error:
            print(error.args[0])
            return None


if __name__ == '__main__':
    sensor = DHT22()
    time.sleep(1)
    try:
        while True:
            print('Temeperature: ' + str(sensor.get_temperature()))
            print('Humidity: '+ str(sensor.get_humidity()))
            time.sleep(3)
            
    except KeyboardInterrupt:
        exit()