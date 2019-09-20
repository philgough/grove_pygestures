from microbit import *
from digit_display import *

display.show(Image.HAPPY)
# initialise the display at pin 15/1
grove_display = Grove4DigitDisplay(15, 1)
t = 1234
count = 0
sleep(400)

while True:
    # show the current value of t to the display
    grove_display.show(t)

    # flash the colon on the digital display
    grove_display.set_colon(count & 1)

    # update value of t
    t += 1
    # update value of counter (to flash the colon on the digital display)
    count += 1

    sleep(50)
