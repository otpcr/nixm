# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105


"log text"


import time


from nixt.object  import Object
from nixt.persist import find, fntime, laps, write


"classes"


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


"commands"


def log(event):
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
    write(obj)
    event.reply('ok')