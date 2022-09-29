#!/usr/bin/env python3          
                                
import signal                   
import sys
import RPi.GPIO as GPIO
import time, datetime, threading

class ANEMOMETER():
    def __init__(self):
        BUTTON_GPIO = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.counter = 0
        self.wind_speed = 0 # km/h
            
        def sensor_callback(channel):
            if not GPIO.input(BUTTON_GPIO):
                self.counter += 1
                
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=sensor_callback)
        self.timer_interrupt()

    def timer_interrupt(self):
        self.wind_speed = round(self.counter*0.315, 3)
        self.counter = 0
        threading.Timer(1.0, self.timer_interrupt).start()

    def get_wind_speed(self):
        return (self.wind_speed)

if __name__ == '__main__':
    sensor = ANEMOMETER()
    while True:
        time.sleep(2)
        print(f'wind_speed: {sensor.wind_speed}')