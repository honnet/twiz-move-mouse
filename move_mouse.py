from oscAPI import listen, readQueue, bind, init
from pymouse import PyMouse
from math import cos, sin
M = PyMouse()
W, H = M.screen_size()

twiz_max = { "up":0.0627876896915,   "down": 0.322699455539,     # az max, az min
             "left":0.183024346828, "right": 0.257259473205 }   # rz min, rz max


mi = 999
ma = 0

def main():
    init()
    oscid = listen(port=10001)
    bind(oscid, update_mouse, '/update')

    # TODO: compute the 4 max values and the ranges

    while True:
        readQueue(oscid)


def update_mouse(message, *args):
    mx, my = M.position()
    az, rz = message[2:]
    rz += .5 # to get range [0;1]
    az += .5
    az = sin(az) # improves range

    global ma
    global mi
    ma = max(ma, rz)
    mi = min(mi, rz)

    print rz, '\t', mi, ma
    #print 'twiz data:', az, rz, '\tmouse:', mx, my
    # M.move(x + m[0] * 10 - 5, y + m[1] * 10 - 5)

if __name__ == '__main__':
    main()
