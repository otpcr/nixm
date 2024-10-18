# This file is placed in the Public Domain.


"modules"


import sys


def getmain(name):
    "retrieve from main."
    main = sys.modules.get("__main__")
    return getattr(main, name, None)
