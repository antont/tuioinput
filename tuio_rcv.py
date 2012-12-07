#!/usr/bin/env python3
from OSC import OSCServer
import sys
from time import sleep

server = OSCServer( ("10.20.219.225", 3333) )
server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

#we use tuio events now just to determine clicks.
#this is the list of clicks since prev clear
#tuio/multitaction id mapped to x,y coordpair
#only first data for an id is used - as in 'touchbegin' / 'mousedown'
clicks = {}

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args[2],args[0],1-args[1])

def tuio_callback(path, tags, args, source):
    print path
    print tags
    print args
    print source

def tuio2Dcur_callback(path, tags, args, source):
    #print tags
    if args[0] in ['alive', 'fseq']:
        return
    #print path,
    #print args
    _, num, x, y, a, b, c = args
    print num, x, y
    if num not in clicks:
        clicks[num] = (x, y)
        print clicks
    #print source

def default_handler(addr, tags, stuff, source):
    #print "SERVER: No handler registered for ", addr
    return None

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/user/1", user_callback )
server.addMsgHandler( "/user/2", user_callback )
server.addMsgHandler( "/user/3", user_callback )
server.addMsgHandler( "/user/4", user_callback )
server.addMsgHandler( "/tuio/2Dcur", tuio2Dcur_callback )
server.addMsgHandler("default", default_handler)
	
server.addMsgHandler( "/quit", quit_callback )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

if __name__ == '__main__':
    # simulate a "game engine"
    while run:
        # do the game stuff:
        #sleep(1)
        # call user script
        each_frame()

    server.close()
