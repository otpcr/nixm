# This file is placed in the Public Domain.
# pylint: disable=W0105


"list of commands"


from nixm.main   import Commands
from nixm.object import keys


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))


"register"


def register():
    Commands.add(cmd)
