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

        while self.pin.read_digital() == 0:
            if utime.ticks_diff(start, init) > timeout:
                flag = True
                break
            else:
                start = utime.ticks_us()

        while self.pin.read_digital() == 1:
            if utime.ticks_diff(stop, init) > timeout:
                flag = True
                break
            else:
                stop = utime.ticks_us()

        if flag is True:
            flag = False
            return -1

        else:
            distance = utime.ticks_diff(stop, start) * 343 / 20000
            return distance
