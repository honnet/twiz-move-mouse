from oscAPI import listen, readQueue, bind, init
from pymouse import PyMouse
from math import cos, sin
import sys, select

# OSC instructions: send 'rz_d' (as X) and 'az_d' (as Y) TODO verify Y
# host='127.0.0.1', port=3333, OSCaddress='/update'

class Maus(): # Maus(host='127.0.0.1', port=3333, OSCaddress='/update') # TODO?
    M = PyMouse()
    W, H = M.screen_size()      # TODO: use if saturation too
    x_pos, y_pos = M.position() # useful to start from current position TODO: use it!

    isCalibrated = False
    x_min = +sys.float_info.max # left
    x_max = -sys.float_info.max # right
    y_min = +sys.float_info.max # low
    y_max = -sys.float_info.max # high

    def __init__(self, host='127.0.0.1', port=3333, OSCaddress='/update'):
        oscAPI.init()
        oscid = oscAPI.listen(host, port)
        oscAPI.bind(oscid, self.update_imu_data, OSCaddress)
        print "Listening to IP:", host, "- port:", port, "- OSC address:", OSCaddress

    def update_imu_data(self, message, *args):
        # TODO: use current mouse position
        self.x_pos, self.y_pos = message[2:] # value received from the twiz

        if self.isCalibrated:
            self.x_pos = ( (self.x_pos + 0.5 - self.x_min) / (self.x_max - self.x_min) ) * W
            self.y_pos = ( (self.y_pos + 0.5 - self.y_min) / (self.y_max - self.x_min) ) * H
            # TODO : invert y, smoothen, improve range...

            maus.move()
        else:
            self.x_pos = ( self.x_pos + 0.5 ) * W
            self.y_pos = ( self.y_pos + 0.5 ) * H
            print self.x_pos, self.y_pos                      # TODO: VERIFY THIS !!!!!!!!!!!!!!!!!

    def calibrate(self):
        print "Move in the wanted range (up + down) and press ENTER..."

        done = False
        while not done:
            done, x, x = select.select( [sys.stdin], [], [], .01 ) # 10ms timeout

            self.x_min = min(self.x_pos, self.x_min)
            self.y_min = min(self.y_pos, self.y_min)

            self.x_max = max(self.x_pos, self.x_max)
            self.y_max = max(self.y_pos, self.y_max)

        print "Calibration done - X:", self.x_min, self.x_max , "Y:", self.y_min, self.y_max
        self.isCalibrated = True

    def move(self):
        # M.move(x_pos, y_pos) # TODO
        print "Moving to:", x_pos, '\t', y_pos


def main():
    maus = Maus()

    while True:
        readQueue(oscid)

if __name__ == '__main__':
    main()

