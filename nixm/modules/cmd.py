# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


"show list of commands"


from ..command import NAMES


def cmd(event):
    event.reply(",".join(sorted(NAMES.keys())))
