from microbit import *
from ultrasonic import *

rf = Rangefinder(pin1)

display.show(Image.YES)

while True:
    dist = rf.distance_cm()
    print((dist,))
    sleep(10)
