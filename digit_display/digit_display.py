from microbit import *

# DO NOT TOUCH THIS FILE!
# Mu will say that the following line only has a single quote,
#  and is incomplete. This is a Mu bug - this file is valid.

charmap = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00?\x06[Ofm}\x07\x7fo\x00\x00\x00\x00\x00\x00\x00w\x7f9?yq}v\x06\x1fv8\x00\x00?s\x00\x00m\x00>>\x00\x00f[\x00\x00\x00\x00\x08\x00\x00|X^\x00\x00\x00t\x00\x00\x00\x06\x00T\\\x00\x00P'

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7


def getchar(c):
    return charmap[ord(c) - 32]

class Grove4DigitDisplay:
    colon_index = 1

    def __init__(self, clk=pin1, dio=pin15, brightness=BRIGHT_DEFAULT):
        self.brightness = brightness

        # self.clk = GPIO(clk, direction=GPIO.OUT)
        # self.dio = GPIO(dio, direction=GPIO.OUT)
        self.clk = clk
        self.dio = dio
        self.data = [0] * 4
        self.show_colon = False

    def clear(self):
        self.show_colon = False
        self.data = [0] * 4
        self._show()

    def show(self, data):
        if type(data) is str:
            for i, c in enumerate(data):
                self.data[i] = getchar(c)
                if i == self.colon_index and self.show_colon:
                    self.data[i] |= 0x80
                if i == 3:
                    break
        elif type(data) is int:
            self.data = [0, 0, 0, getchar('0')]
            if data < 0:
                negative = True
                data = -data
            else:
                negative = False
            index = 3
            while data != 0:
                self.data[index] = getchar(str(data % 10))
                index -= 1
                if index < 0:
                    break
                data = int(data / 10)

            if negative:
                if index >= 0:
                    self.data[index] = getchar('-')
                else:
                    self.data = getchar('_') + [getchar('9')] * 3
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

        self.data[index] = getchar(value)

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
