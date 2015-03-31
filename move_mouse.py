from oscAPI import listen, readQueue, bind, init
from pymouse import PyMouse
M = PyMouse()
W, H = M.screen_size()


def main():
    init()
    oscid = listen(port=10001)
    bind(oscid, update_mouse, '/update')

    while True:
        readQueue(oscid)


def update_mouse(message, *args):
    m = message[2:]
    print m
    x, y = M.position()
    M.move(x + m[0] * 10 - 5, y + m[1] * 10 - 5)

if __name__ == '__main__':
    main()
