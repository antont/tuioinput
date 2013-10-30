#now mixing in uinput too
import uinput

import tuio_rcv
import displayconf

"""uinput things: create a software mouse"""
already_handled_fingerids = set()

events = (
    uinput.ABS_X,
    uinput.ABS_Y,
    uinput.BTN_LEFT
    )

device = uinput.Device(events)

def normalise(display, x, y):
    """multidisplay support: 
    offset based on the position of the display in the physical layout"""
    if display in displayconf.displayoffsets:
        displayoff = displayconf.displayoffsets[display]
    else:
        #print "WARNING in tui2sysmouse: unknown display?", display
        #displayoff = (0, 0)
        return None, None

    x = displayoff[0] + (1920 * x)
    y = displayoff[1] + (1080 * y)
    #wish - works with some nice array type: coord += displayoff    
    
    return x, y

def main():
    while 1:
        tuio_rcv.each_frame()

        for fingerid, eventdata in tuio_rcv.clicks.iteritems():
            if fingerid not in already_handled_fingerids:
                already_handled_fingerids.add(fingerid)
                source, x, y = eventdata
                #print source
                display = source[0]
                x, y = normalise(display, x, y)
                if x is None:
                    continue
                print source, int(x), int(y)

                #syn=False to emit an "atomic" (x, y) + BTN DOWN event.    
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
