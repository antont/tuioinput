#now mixing in uinput too
import uinput
import sys
import tuio_rcv

fingerids_handled_last_round = set()

events = (
    uinput.ABS_X,
    uinput.ABS_Y,
    uinput.BTN_LEFT
    )

device = uinput.Device(events)

def normalise(x, y):
    return (x * 1920), y * 1080

import time

def main():
    dragging = False
    while 1:
        tuio_rcv.each_frame()
        fingerids_handled_this_round = set()
        gotsome=False
        for num, coord in tuio_rcv.clicks.iteritems():
            gotsome=True
            fingerids_handled_this_round.add(num)
            x, y = coord
            x, y = normalise(x, y)
            #print 'emitting', x, y
            #syn=False to emit an "atomic" (5, 5) event.    
            device.emit(uinput.ABS_X, int(x), syn=False)
            device.emit(uinput.ABS_Y, int(y), syn=True)

        time.sleep(0.01)

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
        if dragging is True and len(fingerids_handled_this_round) == 0:
            dragging = False
            device.emit(uinput.BTN_LEFT, 0)
        fingerids_handled_last_round.clear()
        fingerids_handled_last_round.update(fingerids_handled_this_round) 
        #to clear the already handled things from the tuio reader side
        tuio_rcv.clicks.clear()

if __name__ == '__main__':
    main()
