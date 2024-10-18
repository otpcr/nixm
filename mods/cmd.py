# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"list of commands"


from nixm.object import keys


from . import getmain


Commands = getmain("Commands")


def cmd(event):
    if Commands:
        event.reply(",".join(sorted(keys(Commands.cmds))))
