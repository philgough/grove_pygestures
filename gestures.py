def gesture(argument):
    switcher = {
        '0x01':GroveGesture.Right,
        '0x02':GroveGesture.Left,
        '0x04':GroveGesture.Up,
        '0x08':GroveGesture.Down,
        '0x10':GroveGesture.Forward,
        '0x20':GroveGesture.Backward,
        '0x40':GroveGesture.Clockwise,
        '0x80':GroveGesture.Anticlockwise,
        # wave is a special case... '0x44':GroveGesture.Wave,
                        # default:
                            # data = this.paj7620ReadReg(0x44);
                            # if (data == 0x01)
                                # result = GroveGesture.Wave;
                        # break;
        }
    return switcher.get(argument)
