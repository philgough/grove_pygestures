from microbit import pin2
import utime


def measurementInCM():

    pin2.write_digital(0)
    utime.sleep_us(200)
    pin2.write_digital(1)
    utime.sleep_us(500)
    pin2.write_digital(0)
    init = utime.ticks_us()
    stop = init
    start = init
    flag = False
    timeout = 100000

    while pin2.read_digital() == 0:
        if utime.ticks_diff(start, init) > timeout:
            flag = True
            # print('escape!')
            break
        else:
            start = utime.ticks_us()

    while pin2.read_digital() == 1:
        if utime.ticks_diff(stop, init) > timeout:
            flag = True
            # print('escape!')
            break
        else:
            stop = utime.ticks_us()

    if flag is True:
        flag = False
        return -1

    else:
        distance = utime.ticks_diff(stop, start) * 343 / 20000
        return distance