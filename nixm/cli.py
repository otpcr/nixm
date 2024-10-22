# This file is place in the Public Domain.
# pylint: disable=C


"Nix Em"


import sys


from nixm.main    import Client, Config, Event, scanner, command, parse, wrap
from nixm.modules import face
from nixm.runtime import Errors


cfg = Config()


class CLI(Client):

    def raw(self, txt):
        print(txt)


def errors():
    for error in Errors.errors:
        for line in error:
            print(line)


def wrapped():
    wrap(main)
    if "v" in cfg.opts:
        errors()


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    scanner(face)
    evt = Event()
    evt.txt = cfg.txt
    csl = CLI()
    command(csl, evt)
    evt.wait()


if __name__ == "__main__":
    wrapped()
