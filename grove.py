from microbit import *
from microbit import i2c
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




charmap = {
    '0': 0x3f,
    '1': 0x06,
    '2': 0x5b,
    '3': 0x4f,
    '4': 0x66,
    '5': 0x6d,
    '6': 0x7d,
    '7': 0x07,
    '8': 0x7f,
    '9': 0x6f,
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'V': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    '-': 0x40,
    '_': 0x08,
    ' ': 0x00
}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7


class Grove4DigitDisplay:
    colon_index = 1

    def __init__(self, clk, dio, brightness=BRIGHT_DEFAULT):
        self.brightness = brightness

        # self.clk = GPIO(clk, direction=GPIO.OUT)
        # self.dio = GPIO(dio, direction=GPIO.OUT)
        self.clk = pin1
        self.dio = pin15
        self.data = [0] * 4
        self.show_colon = False

    def clear(self):
        self.show_colon = False
        self.data = [0] * 4
        self._show()

    def show(self, data):
        if type(data) is str:
            for i, c in enumerate(data):
                if c in charmap:
                    self.data[i] = charmap[c]
                else:
                    self.data[i] = 0
                if i == self.colon_index and self.show_colon:
                    self.data[i] |= 0x80
                if i == 3:
                    break
        elif type(data) is int:
            self.data = [0, 0, 0, charmap['0']]
            if data < 0:
                negative = True
                data = -data
            else:
                negative = False
            index = 3
            while data != 0:
                self.data[index] = charmap[str(data % 10)]
                index -= 1
                if index < 0:
                    break
                data = int(data / 10)

            if negative:
                if index >= 0:
                    self.data[index] = charmap['-']
                else:
                    self.data = charmap['_'] + [charmap['9']] * 3
        else:
            raise ValueError('Not support {}'.format(type(data)))
        self._show()

    def _show(self):
        with self:
            self._transfer(ADDR_AUTO)

        with self:
            self._transfer(STARTADDR)
            for i in range(4):
                self._transfer(self.data[i])

        with self:
            self._transfer(0x88 + self.brightness)

    def update(self, index, value):
        if index < 0 or index > 4:
            return

        if value in charmap:
            self.data[index] = charmap[value]
        else:
            self.data[index] = 0

        if index == self.colon_index and self.show_colon:
            self.data[index] |= 0x80

        with self:
            self._transfer(ADDR_FIXED)

        with self:
            self._transfer(STARTADDR | index)
            self._transfer(self.data[index])

        with self:
            self._transfer(0x88 + self.brightness)


    def set_brightness(self, brightness):
        if brightness > 7:
            brightness = 7

        self.brightness = brightness
        self._show()

    def set_colon(self, enable):
        self.show_colon = enable
        if self.show_colon:
            self.data[self.colon_index] |= 0x80
        else:
            self.data[self.colon_index] &= 0x7F
        self._show()

    def _transfer(self, data):
        for _ in range(8):
            self.clk.write_digital(0)
            if data & 0x01:
                self.dio.write_digital(1)
            else:
                self.dio.write_digital(0)
            data >>= 1
            sleep(1)
            self.clk.write_digital(1)
            sleep(1)

        self.clk.write_digital(0)
        self.dio.write_digital(1)
        self.clk.write_digital(1)
        self.dio.write_digital(0)

    def _start(self):
        self.clk.write_digital(1)
        self.dio.write_digital(1)
        self.dio.write_digital(0)
        self.clk.write_digital(0)

    def _stop(self):
        self.clk.write_digital(0)
        self.dio.write_digital(0)
        self.clk.write_digital(1)
        self.dio.write_digital(1)

    def __enter__(self):
        self._start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop()
# Write your code here :-)

init_reg = "\xEF\x00\x32\x29\x33\x01\x34\x00\x35\x01\x36\x00\x37\x07\x38\x17\x39\x06\x3A\x12\x3F\x00\x40\x02\x41\xFF\x42\x01\x46\x2D\x47\x0F\x48\x3C\x49\x00\x4A\x1E\x4B\x00\x4C\x20\x4D\x00\x4E\x1A\x4F\x14\x50\x00\x51\x10\x52\x00\x5C\x02\x5D\x00\x5E\x10\x5F\x3F\x60\x27\x61\x28\x62\x00\x63\x03\x64\xF7\x65\x03\x66\xD9\x67\x03\x68\x01\x69\xC8\x6A\x40\x6D\x04\x6E\x00\x6F\x00\x70\x80\x71\x00\x72\x00\x73\x00\x74\xF0\x75\x00\x80\x42\x81\x44\x82\x04\x83\x20\x84\x20\x85\x00\x86\x10\x87\x00\x88\x05\x89\x18\x8A\x10\x8B\x01\x8C\x37\x8D\x00\x8E\xF0\x8F\x81\x90\x06\x91\x06\x92\x1E\x93\x0D\x94\x0A\x95\x0A\x96\x0C\x97\x05\x98\x0A\x99\x41\x9A\x14\x9B\x0A\x9C\x3F\x9D\x33\x9E\xAE\x9F\xF9\xA0\x48\xA1\x13\xA2\x10\xA3\x08\xA4\x30\xA5\x19\xA6\x10\xA7\x08\xA8\x24\xA9\x04\xAA\x1E\xAB\x1E\xCC\x19\xCD\x0B\xCE\x13\xCF\x64\xD0\x21\xD1\x0F\xD2\x88\xE0\x01\xE1\x04\xE2\x41\xE3\xD6\xE4\x00\xE5\x0C\xE6\x0A\xE7\x00\xE8\x00\xE9\x00\xEE\x07\xEF\x01\x00\x1E\x01\x1E\x02\x0F\x03\x10\x04\x02\x05\x00\x06\xB0\x07\x04\x08\x0D\x09\x0E\x0A\x9C\x0B\x04\x0C\x05\x0D\x0F\x0E\x02\x0F\x12\x10\x02\x11\x02\x12\x00\x13\x01\x14\x05\x15\x07\x16\x05\x17\x07\x18\x01\x19\x04\x1A\x05\x1B\x0C\x1C\x2A\x1D\x01\x1E\x00\x21\x00\x22\x00\x23\x00\x25\x01\x26\x00\x27\x39\x28\x7F\x29\x08\x30\x03\x31\x00\x32\x1A\x33\x1A\x34\x07\x35\x07\x36\x01\x37\xFF\x38\x36\x39\x07\x3A\x00\x3E\xFF\x3F\x00\x40\x77\x41\x40\x42\x00\x43\x30\x44\xA0\x45\x5C\x46\x00\x47\x00\x48\x58\x4A\x1E\x4B\x1E\x4C\x00\x4D\x00\x4E\xA0\x4F\x80\x50\x00\x51\x00\x52\x00\x53\x00\x54\x00\x57\x80\x59\x10\x5A\x08\x5B\x94\x5C\xE8\x5D\x08\x5E\x3D\x5F\x99\x60\x45\x61\x40\x63\x2D\x64\x02\x65\x96\x66\x00\x67\x97\x68\x01\x69\xCD\x6A\x01\x6B\xB0\x6C\x04\x6D\x2C\x6E\x01\x6F\x32\x71\x00\x72\x01\x73\x35\x74\x00\x75\x33\x76\x31\x77\x01\x7C\x84\x7D\x03\x7E\x01"

gestures = {
    0x01: 'right',
    0x02: 'left',
    0x04: 'up',
    0x08: 'down',
    0x10: 'forward',
    0x20: 'backward',
    0x40: 'clockwise',
    0x80: 'anticlockwise',
}

class Gesture:
    def _init_reg_part(self):
        for i in range(0, len(init_reg), 2):
            self._write_reg(ord(init_reg[i]), ord(init_reg[i+1]))

    def _init(self):
        i2c.init()
        temp = 0
        sleep(1)

        # Intentionally duplicated
        self._select_bank(0)

        temp = self._read_reg(0)
        if temp == 0x20:
            print("Writing registers")
            self._init_reg_part()
            #del init_reg
        self._select_bank(0)

    def _write_reg(self, addr, cmd):
        buf = bytearray([addr, cmd])
        i2c.write(0x73, buf, False)

    def _read_reg(self, addr):
        buf = bytearray([addr])
        i2c.write(0x73, buf, False)
        ret = i2c.read(0x73, 1, False)
        return ord(ret)

    def _select_bank(self, bank):
        if bank == 0:
            self._write_reg(0xEF, 0)
        elif bank == 1:
            self._write_reg(0xEF, 1)

    def __init__(self):
        self._init()
        sleep(200);

    def read(self):
        data = 0
        result = 0
        data = self._read_reg(0x43)
        if data in gestures:
            return gestures[data]
        else:
            data = self._read_reg(0x44)
            if data == 0x01:
                return 'wave'
        return 'none'
