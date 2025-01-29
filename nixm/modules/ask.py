# This file is placed in the Public Domain.


import select
import sys


from ollama import chat
from ollama import ChatResponse


"api"


def api(txt):
    response: ChatResponse = chat(model='deepseek-v2:16b', messages=[
      {
        'role': 'user',
        'content': txt,
      },
    ])
    return response.message.content.strip()


"commands"


def ask(event):
    if event.rest:
        text = event.rest +"\n\n"
    if not select.select(
                         [sys.stdin, ],
                         [],
                         [],
                         0.0
                        )[0]:
        event.reply("ask <text>")
        return
    size = 0
    while 1:
        try:
            (inp, _out, err) = select.select(
                                             [sys.stdin,],
                                             [],
                                             [sys.stderr,]
                                            )
        except KeyboardInterrupt:
            return
        if err:
            break
        stop = False
        for sock in inp:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            text += txt + "\n"
            size += len(txt)
        if stop:
            break
    print(text)
    event.reply(api(text))
