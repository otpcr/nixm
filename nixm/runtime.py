# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0718


"threading"


import queue
import threading
import time
import traceback
import _thread


"defines"


STARTTIME = time.time()


"errors"


class Errors:

    errors = []

    @staticmethod
    def format(exc):
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors():
    for err in Errors.errors:
        yield from err


def later(exc):
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


"thread"


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self):
        func, args = self.queue.get()
        try:
            func(*args)
        except Exception as ex:
            later(ex)
            try:
                args[0].ready()
            except (IndexError, AttributeError):
                pass


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj):
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


"timers"


class Timer:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args   = args
        self.func   = func
        self.kwargs = kwargs
        self.sleep  = sleep
        self.name   = thrname or kwargs.get("name", name(func))
        self.state  = {}
        self.timer  = None
        print(self.args[0])

    def run(self):
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self):
        launch(self.start)
        super().run()


"reactor"


class Reactor:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Fleet.add(self)

    def callback(self, evt):
        func = self.cbs.get(evt.type, None)
        if func:
            try:
                evt._thr = launch(func, self, evt)
            except Exception as ex:
                later(ex)
                evt.ready()

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if "ready" in dir(evt):
                    evt.ready()
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put(evt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)

    def wait(self):
        self.queue.join()
        self.stopped.wait()


"fleet"


class Fleet:

    bots = {}

    @staticmethod
    def add(bot):
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def first():
        bots =  list(Fleet.bots.values())
        if bots:
            return bots[0]

    @staticmethod
    def get(name):
        return Fleet.bots.get(name, None)

    @staticmethod
    def say(orig, channel, txt):
        bot = Fleet.get(orig)
        bot.say(channel, txt)


"interface"


def __dir__():
    return (
        'STARTTIME',
        'Errors',
        'EVent',
        'Reactor',
        'Repeater',
        'Thread',
        'Timer',
        'errors',
        'later',
        'launch',
        'name'
    )
