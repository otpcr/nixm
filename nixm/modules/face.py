# This file is placed in the Public Domain.
# pylint: disable=W0611
# ruff: noqa: F401


"interface"


import importlib


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


def boot():
    for name in MODS:
        mname = f"nixm.modules.{name}"
        mod = importlib.import_module(mname, 'nixm.modules.face')


def __dir__():
    return MODS
