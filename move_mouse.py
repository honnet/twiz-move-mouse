from oscAPI import listen, readQueue, bind, init
from pymouse import PyMouse
from math import cos, sin
M = PyMouse()
W, H = M.screen_size()
# mx, my = M.position()

x_min = 0.535187304020 # left
x_max = 0.616868846118 # right

y_min = 0.478545814753 # low
y_max = 0.584199279547 # high

def main():
    init()
    oscid = listen(port=10001)
    bind(oscid, update_mouse, '/update')

    # TODO: compute the 4 max values and the ranges

    while True:
        readQueue(oscid)


def update_mouse(message, *args):
    global x_min, y_min, x_max, y_max, W, H
    y_pos, x_pos = message[2:] # value recived from the twiz

    x_pos = ( (x_pos + 0.5 - x_min) / (x_max-x_min) ) * W
    y_pos = ( (y_pos + 0.5 - y_min) / (y_max-x_min) ) * H
    # TODO : invert y, smoothen, improve range...

    M.move(x_pos, y_pos)
    print x_pos, '\t', y_pos

if __name__ == '__main__':
    main()
