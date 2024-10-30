# This file is placed in the Public Domain.
# pylint: disable=C


"service"


import os


from nixt.persist import pidfile, pidname
from nixt.runtime import errors, forever, privileges, wrap


from .command import NAME, scanner
from .modules import face


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
