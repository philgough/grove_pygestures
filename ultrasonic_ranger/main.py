from microbit import *
from ultrasonic import *

display.show(Image.YES)

while True:
    dist = measurementInCM()
    print((dist, ))
    sleep(10)