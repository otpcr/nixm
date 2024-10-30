# This file is placed in the Public Domain.
# pylint: disable=C


"service"


import os


from ..command import NAME, scanner
from ..modules import face
from ..persist import pidfile, pidname
from ..runtime import errors, forever, privileges, wrap


def main():
    privileges()
    pidfile(pidname(NAME))
    scanner(face, init=True)
    forever()


def wrapped():
    wrap(main)
    for line in errors():
        print(line)


if __name__ == "__main__":
    wrapped()
