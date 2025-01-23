# This file is placed in the Public Domain.
# pylint: disable=C0116


"uptime"


import time


from nixm.persist import elapsed
from nixm.runtime import STARTTIME


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
