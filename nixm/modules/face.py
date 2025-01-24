# This file is placed in the Public Domain.
# pylint: disable=W0611
# ruff: noqa: F401


"interface"


import importlib


class Table:

    mods = {}

    @staticmethod
    def add(mod):
        Table.mods[mod.__name__] = mod

    @staticmethod
    def get(name):
        return Table.mods.get(name, None)

    @staticmethod
    def load(name):
        Table.mods[name] = mod = importlib.import_module(name, 'nixm.modules')
        return mod


"callbacks"


MODS = (
    'cmd',
    'err',
    'flt',
    'fnd',
    'irc',
    'log',
    'mbx',
    'mdl',
    'mod',
    'req',
    'rss',
    'rst',
    'slg',
    'tdo',
    'thr',
    'tmr',
    'udp',
    'upt',
    'wsd'
)


for name in MODS:
    mname = f"nixm.modules.{name}"
    Table.load(mname)


def __dir__():
    return MODS
