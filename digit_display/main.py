from microbit import *
from digit_display import *

display.show(Image.HAPPY)
grove_display = Grove4DigitDisplay(15, 1)
t = 1234
count = 0
print('hello, world')

while True:

    grove_display.show(t)
    grove_display.set_colon(count & 1)
    t += 1
    count += 1
    print(t)
    sleep(50)
