# coding=utf-8
from threading import Thread


def loop():
    while True:
        pass


if __name__ == '__main__':

    for i in range(30000):
        t = Thread(target=loop)
        print(t)
        t.start()

    while True:
        pass

