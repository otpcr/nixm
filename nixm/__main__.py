# This file is placed in the Public Domain.
# pylint: disable=C,R0903,W0105,W0212,W0611,W0613,W0718,E0402


"main"


import os
import pathlib
import sys
import time
import _thread


from .clients import Client, Config
from .command import NAMES, Commands, Table, command, parse, spl
from .modules import face
from .objects import dumps
from .persist import Workdir, pidname
from .runtime import Event, Fleet, errors, later, launch


import nixm.clients


"defines"


cfg   = Config()
p     = os.path.join
pname = f"{Config.name}.modules"


Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")


"output"


def debug(txt):
    if "v" in cfg.opts:
        output(txt)


def output(txt):
    # output here
    print(txt)


"console"


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        output(txt.encode('utf-8', 'replace').decode("utf-8"))


class Console(CLI):

    def announce(self, txt):
        #output(txt)
        pass

    def callback(self, evt):
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt


"utilities"


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    output(f"{Config.name.upper()} since {tme}")


def check(txt):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for c in txt:
            if c in arg:
                return True
    return False


def daemon(verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


"scripts"


def background():
    daemon(True)
    privileges()
    pidfile(pidname(Config.name))
    Commands.add(cmd)
    Table.inits(Config.init)
    forever()


def console():
    import readline # noqa: F401
    Commands.add(cmd)
    parse(cfg, " ".join(sys.argv[1:]))
    Config.init = cfg.sets.init or Config.init
    Config.opts = cfg.opts
    if "v" in cfg.opts:
        banner()
        nixm.clients.output = print
    if "i" in cfg.opts:
        for _mod, thr in Table.inits(Config.init, pname):
            if "w" in cfg.opts:
                thr.join()
    csl = Console()
    csl.start()
    forever()


def control():
    if len(sys.argv) == 1:
        return
    Commands.add(cmd)
    Commands.add(srv)
    Commands.add(tbl)
    parse(cfg, " ".join(sys.argv[1:]))
    csl = CLI()
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = cfg.otxt
    command(evt)
    evt.wait()


def service():
    privileges()
    pidfile(pidname(Config.name))
    Commands.add(cmd)
    Table.inits(Config.init)
    forever()


"commands"


def cmd(event):
    event.reply(",".join(sorted(NAMES)))


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (Config.name.upper(), name, name, name, Config.name))


def tbl(event):
    Table.scan(face)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("")
    event.reply("")
    event.reply('"lookup tables"')
    event.reply("")
    event.reply("")
    event.reply(f"NAMES = {dumps(Commands.names, indent=4, sort_keys=True)}")
    

"data"


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


"runtime"


def wrap(func):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        output("")
    except Exception as exc:
        later(exc)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
    for line in errors():
        output(line)


def wrapped():
    wrap(main)


def wraps():
    wrap(service)


def main():
    if check("c"):
        wrap(console)
    elif check("d"):
        background()
    elif check("s"):
        wrap(service)
    else:
        control()


if __name__ == "__main__":
    main()
