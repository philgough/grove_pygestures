# Write your code here :-)
from microbit import *
from microbit import i2c
import music

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

gesture = Gesture()

clockwise = Image("99999:"
                  "00009:"
                  "09009:"
                  "99990:"
                  "09000:")
anticlockwise = Image("99999:"
                      "90000:"
                      "90090:"
                      "09999:"
                      "00090:")
forward = Image("09090:"
                "99099:"
                "00000:"
                "99099:"
                "09090:")
backward = Image("99099:"
                 "90009:"
                 "00000:"
                 "90009:"
                 "99099:")
wave = Image("00090:"
			 "99999:"
			 "00000:"
			 "99999:"
			 "09000:")

gesture_map = {
    'up': Image.ARROW_N,
    'down': Image.ARROW_S,
    'left': Image.ARROW_W,
    'right': Image.ARROW_E,
    'forward': forward,
    'backward': backward,
    'clockwise': clockwise,
    'anticlockwise': anticlockwise,
    'wave': wave
}

sound_map = {
    'up': music.JUMP_UP,
    'down': music.JUMP_DOWN,
    'left': music.POWER_UP,
    'right': music.POWER_DOWN,
    'forward': music.BA_DING,
    'backward': music.WAWAWAWAA,
    'clockwise': music.RINGTONE,
    'anticlockwise': music.DADADADUM,
    'wave': music.PYTHON
}
while True:
    g = gesture.read()
    if g == 'none':
        display.show(Image.HAPPY)
    else:
        display.show(gesture_map[g])
        music.play(sound_map[g])
        sleep(300)


display.show(Image.GIRAFFE)
