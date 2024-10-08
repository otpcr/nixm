# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0611


"cli"


import sys


from .broker  import Broker
from .command import boot, command
from .modules import face
from .runtime import Client, Errors, Event


class CLI(Client):

    "CLI"

    def __init__(self):
        Client.__init__(self)
        Broker.add(self)
        self.register("event", command)

    def raw(self, txt):
        "print text."
        print(txt)


def errors():
    "print errors."
    for error in Errors.errors:
        for line in error:
            print(line)


def main():
    "main"
    boot(face)
    cli = CLI()
    evt = Event()
    evt.txt = " ".join(sys.argv[1:])
    command(cli, evt)
    evt.wait()


if __name__ == "__main__":
    main()
    errors()
