# This file is placed in the Public Domain.
# pylint: disable=W0105


"uptime"


import time


from ..command import Commands
from ..persist import laps
from ..runtime import STARTTIME


"defines"


def register():
    "register commands."
    Commands.add(upt)


"commands"


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))
