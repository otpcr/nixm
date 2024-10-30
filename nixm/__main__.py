# This file is in the Public Domain.


"run"


import sys


from .bin import admin, cli, console, daemon, service


if __name__ == "__main__":
    if "-a" in sys.argv:
        admin.wrapped()
    elif "-c" in sys.argv:
        console.wrapped()
    elif "-d" in sys.argv:
        daemon.wrapped()
    elif "-s" in sys.argv:
        service.wrapped()
    elif len(sys.argv) >= 2:
        cli.wrapped()
    