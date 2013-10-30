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

#bugs now somehow, overheated? does clicks all the time.
#restarting the device helped.
    '192.168.1.104': (W, H),

    '192.168.1.105': (W*2, 0),
    '192.168.1.106': (W*2, H)
}
