# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"list of commands"


from nixm.object import keys
from nixm.main   import Commands


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))
