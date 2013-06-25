import time
import uinput

import tuio_rcv

"""
support for multiple displays ('powerwall')
works also for external displays (had laptop+table in dev)
"""
W = 1920
H = 1080
displayoffsets = {
    '192.168.1.102': (0, 0),
    '192.168.1.101': (W, 0),
    '192.168.1.103': (0, H),
    '192.168.1.104': (W, H),
    '192.168.1.105': (W*2, 0),
    '192.168.1.106': (W*2, H)
}

fingerids_handled_last_round = set()
fingerid_lastseen = dict()

"""uinput things: create a software mouse"""
events = (
    uinput.ABS_X,
    uinput.ABS_Y,
    uinput.BTN_LEFT
    )

device = uinput.Device(events)

def normalise(display, x, y):
    """multidisplay support: 
    offset based on the position of the display in the physical layout"""
    if display in displayoffsets:
        displayoff = displayoffsets[display]
    else:
        print "WARNING in tui2sysmouse: unknown display?", display
        displayoff = (0, 0)

    x = displayoff[0] + (1920 * x)
    y = displayoff[1] + (1080 * y)
    #wish - works with some nice array type: coord += displayoff    
    
    return x, y

def main():
    dragging = False
    last_touch_timestamp = 0.0
    lastcoord = None, None
    while 1:
        tuio_rcv.each_frame()
        fingerids_handled_this_round = set()
        gotsome=False
        for fingerid, eventdata in tuio_rcv.clicks.iteritems():
            gotsome=True
            fingerids_handled_this_round.add(fingerid)

            source, x, y = eventdata
            #print source
            display = source[0]
            x, y = normalise(display, x, y)
            print source, int(x), int(y)

            #syn=False to emit an "atomic" (x, y) + BTN DOWN event.    
            device.emit(uinput.ABS_X, int(x), syn=False)
            device.emit(uinput.ABS_Y, int(y), syn=True)

            last_touch_timestamp = fingerid_lastseen[fingerid] = time.time()

        time.sleep(0.01)

        if len(fingerids_handled_this_round) > 1:
            fl = list(fingerids_handled_this_round)
            fl.sort(key=lambda x: fingerid_lastseen.get(fingerid, -1))
            print 'keeping oldest fingerid', fl[-1], 'out of', fingerids_handled_this_round
            fingerids_handled_this_round.clear()
            fingerids_handled_this_round.add(fl[-1])
        	
        # set difference yields elements that were only in last_round
        gone_fingerids = fingerids_handled_last_round - fingerids_handled_this_round
        if gone_fingerids:
            print fingerids_handled_last_round, 'minus', fingerids_handled_this_round
            print 'fingers that went away:', gone_fingerids
            
        appeared_fingerids = fingerids_handled_this_round - fingerids_handled_last_round
        if appeared_fingerids:
            print 'fingers that appeared:', appeared_fingerids
            
        if dragging is False and appeared_fingerids and not gone_fingerids:
            dragging = True
            device.emit(uinput.BTN_LEFT, 1)

#        if dragging is True and gone_fingerids and not appeared_fingerids:
        time_since_last_touch = time.time() - last_touch_timestamp
        if (dragging is True and
                len(fingerids_handled_this_round) == 0 and
                time_since_last_touch > 0.1):
            dragging = False
            device.emit(uinput.BTN_LEFT, 0)
        
        fingerids_handled_last_round.clear()
        fingerids_handled_last_round.update(fingerids_handled_this_round) 

        #to clear the already handled things from the tuio reader side
        tuio_rcv.clicks.clear()

if __name__ == '__main__':
    main()
