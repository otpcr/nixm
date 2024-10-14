# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"uptime"


import time


from nixm.main    import STARTTIME, Commands
from nixm.persist import laps


def upt(event):
    event.reply(laps(time.time()-STARTTIME))


"register"


def register():
    Commands.add(upt)
