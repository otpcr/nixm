# This file is placed in the Public Domain.
# pylint: disable=W0105,W0719


"debug"


from ..command import Commands


"defines"


def register():
    "register commands."
    Commands.add(dbg)


"commands"


def dbg(event):
    "raise exception."
    raise Exception("yo!")
