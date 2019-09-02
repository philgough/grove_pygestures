from microbit import *
import utime

class Rangefinder:
    def __init__(self, pin):
        '''Setup a rangefinder on the specified pin'''
        self.pin = pin

    def distance_cm(self):
        '''Returns the distance from a rangefinder in cm'''
        self.pin.write_digital(0)
        utime.sleep_us(200)
        self.pin.write_digital(1)
        utime.sleep_us(500)
        self.pin.write_digital(0)
        init = utime.ticks_us()
        stop = init
        start = init
        flag = False
        timeout = 100000

        while not self.pin.read_digital():
            if utime.ticks_us() - init > timeout:
                return -1

        start = utime.ticks_us()

        while self.pin.read_digital():
            if utime.ticks_us() - start > timeout:
                return -1

        stop = utime.ticks_us()
        distance = (stop - start) * 343 / 20000
        print(stop, start)
        return distance
