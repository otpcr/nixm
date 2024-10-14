# This file is placed in the Public Domain.
# pylint: disable=C,W0105,W0611


"create service file"


import getpass


from nixm.main import NAME, Commands


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""


def srv(event):
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


"register"


def register():
    Commands.add(srv)
