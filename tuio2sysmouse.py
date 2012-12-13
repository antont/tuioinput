#now mixing in uinput too
import uinput

import tuio_rcv

already_handled_fingerids = set()

events = (
    uinput.ABS_X,
    uinput.ABS_Y,
    uinput.BTN_LEFT
    )

device = uinput.Device(events)

def normalise(x, y):
    return (x * 1920), y * 1080

def main():
    while 1:
        tuio_rcv.each_frame()

        for num, coord in tuio_rcv.clicks.iteritems():
            if num not in already_handled_fingerids:
                already_handled_fingerids.add(num)
                x, y = coord
                x, y = normalise(x, y)
                
                #syn=False to emit an "atomic" (5, 5) event.    
                device.emit(uinput.ABS_X, int(x), syn=False)
                device.emit(uinput.ABS_Y, int(y), syn=False)
                device.emit(uinput.BTN_LEFT, 1)
                device.emit(uinput.BTN_LEFT, 0)
        
            #else:
                #glColor4f(0.1, 0.2, 1.0, 1.0)
    
    #to clear the already handled things from the tuio reader side
    tuio_rcv.clicks.clear()

if __name__ == '__main__':
    main()
