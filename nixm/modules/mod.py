# This file is placed in the Public Domain.
# pylint: disable=W0105


"show available modules."


import os


from ..command import Commands


"register"


def register():
    "register commands."
    Commands.add(mod)


"commands"


def mod(event):
    "show available modules."
    path = os.path.dirname(__file__)
    mods = []
    for mdd in os.listdir(path):
        if mdd == "face.py":
            continue
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    event.reply(",".join(sorted(mods)))
