# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0902,R0903,W0105,W0613,E0402


"clients"


import queue
import threading
import time


from .command import command
from .objects import Default
from .runtime import Output, Reactor, launch


"config"


class Config(Default):

    name = Default.__module__.rsplit(".", maxsplit=2)[-2]


"client"


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


class Buffered(Client):

    def __init__(self):
        Client.__init__(self)
        Output.start()        


"event"


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def display(self):
        for txt in self.result:
            Fleet.say(self.orig, self.channel, txt)

    def done(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


"interface"


def __dir__():
    return (
        'Client',
        'Config',
        'Event'
    )
