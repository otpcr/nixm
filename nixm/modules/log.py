# This file is placed in the Public Domain.
# pylint: disable=R,W0105


"log text"


import time


from ..command import Commands
from ..object  import Object
from ..persist import find, laps, sync, fntime


"defines"


def register():
    "register commands."
    Commands.add(log)


"classes"


class Log(Object):

    "Log"

    def __init__(self):
        super().__init__()
        self.txt = ''


"commands"


def log(event):
    "log text."
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            lap = laps(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')
