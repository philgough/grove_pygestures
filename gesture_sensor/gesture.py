# Write your code here :-)
from microbit import *
from microbit import i2c
from micropython import const

init_reg = const(b"\xEF\x00\x37\x07\x38\x17\x39\x06\x40\x02\x42\x01\x46\x2D\x47\x0F\x48\x3C\x49\x00\x4A\x1E\x4C\x20\x4E\x1A\x51\x10\x5E\x10\x5F\x3F\x60\x27\x61\x28\x62\x00\x70\x80\x80\x42\x81\x44\x82\x04\x8B\x01\x8C\x37\x8F\x81\x90\x06\x95\x0A\x96\x0C\x97\x05\x99\x41\x9A\x14\x9C\x3F\x9D\x33\x9E\xAE\x9F\xF9\xA0\x48\xA1\x13\xA2\x10\xA3\x08\xA4\x30\xA5\x19\xA6\x10\xA7\x08\xA8\x24\xCC\x19\xCD\x0B\xCE\x13\xCF\x64\xD0\x21\xE3\xD6\xE5\x0C\xE6\x0A\xEE\x07\xEF\x01\x02\x0F\x03\x10\x04\x02\x06\xB0\x07\x04\x0A\x9C\x0B\x04\x25\x01\x27\x39\x28\x7F\x29\x08\x32\x1A\x33\x1A\x38\x36\x39\x07\x3E\xFF\x40\x77\x41\x40\x42\x00\x43\x30\x44\xA0\x45\x5C\x48\x58\x59\x10\x5A\x08\x5B\x94\x5C\xE8\x5D\x08\x5E\x3D\x5F\x99\x60\x45\x61\x40\x63\x2D\x64\x02\x65\x96\x66\x00\x67\x97\x68\x01\x69\xCD\x6A\x01\x6B\xB0\x6C\x04\x6D\x2C\x6E\x01\x72\x01\x73\x35\x75\x33\x76\x31\x77\x01\x7C\x84\x7D\x03\x7E\x01")

gestures = const({
    0x01: 'right',
    0x02: 'left',
    0x04: 'up',
    0x08: 'down',
    0x10: 'forward',
    0x20: 'backward',
    0x40: 'clockwise',
    0x80: 'anticlockwise',
})

class Gesture:
    def _init_reg_part(self):
        for i in range(0, len(init_reg), 2):
            self._write_reg(init_reg[i], init_reg[i+1])

    def _init(self, game_mode=False):
        i2c.init()
        temp = 0
        sleep(1)

        # Intentionally duplicated
        self._select_bank(0)

        temp = self._read_reg(0)
        if temp == 0x20:
            print("Writing registers")
            self._init_reg_part()
            # del init_reg
        self._select_bank(1)
        if game_mode:
            self._write_reg(0x65, 0x12)
        else:
            self._write_reg(0x65, 0xB7)
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

