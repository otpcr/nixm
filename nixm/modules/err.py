# This file is placed in the Public Domain.
# pylint: disable=W0105


"show errors"


from ..command import Commands
from ..runtime import Errors


"defines"


def register():
    "register commands."
    Commands.add(err)


"commands"


def err(event):
    "show errors."
    nmr = 0
    for exc in Errors.errors:
        for line in exc:
            event.reply(line.strip())
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")
