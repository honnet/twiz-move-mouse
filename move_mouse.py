from oscAPI import listen, readQueue, bind, init
from pyautogui import position as pos
from pyautogui import moveTo as move
from pyautogui import click


def main():
    init()
    oscid = listen(port=10001)
    bind(oscid, update_mouse, '/update')

    while True:
        readQueue(oscid)


def update_mouse(message, *args):
    m = message[2:]
    print m
    x, y = pos()
    move(x + m[0] * 10 - 5, y + m[1] * 10 - 5)

if __name__ == '__main__':
    main()
