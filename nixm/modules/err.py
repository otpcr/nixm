# This file is placed in the Public Domain.
# pylint: disable=W0105


"show errors"


from nixm.main    import Commands
from nixm.runtime import Errors


def err(event):
    nmr = 0
    for exc in Errors.errors:
        for line in exc:
            event.reply(line.strip())
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")


"register"


def register():
    Commands.add(err)
