#!/usr/bin/env python3
from sys import argv
from os.path import join, exists, isdir
from os import getenv
import json
import readline
import collections
_memofile_: str = join(getenv("HOME"), ".todo")
_memodata_: dict = {}
_hasfile_: bool = False


def input_prefill(prompt: str, text: str) -> str:
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result


def exist_check() -> None:
    if exists(_memofile_):
        if isdir(_memofile_):
            print("Couldn't create file .todo, ",
                  "a directory with the same name exists")
            quit()
        else:
            global _hasfile_
            _hasfile_ = True


def load_memos() -> None:
    global _memodata_
    if _hasfile_:
        filename = open(_memofile_, 'r')
        _memodata_ = json.loads(filename.read())


def list() -> None:
    if not _memodata_:
        print("There are no TODOs to show")
    else:
        _ordereddata_ = collections.OrderedDict(sorted(_memodata_.items()))
        for id in _ordereddata_:
            title: str = _ordereddata_[id]["title"]
            extended: bool = bool(_ordereddata_[id]["message"])
            toshow: str = "[" + str(id) + "] "
            if extended:
                toshow += "[M] "
            toshow += title
            print(toshow)


def delete(id) -> None:
    if _memodata_[id]:
        del _memodata_[id]
    else:
        print("There is no ToDo with the specified ID")


def makenewmemo() -> None:
    newid: int = len(_memodata_) + 1
    title: str = input("Title: ")
    message: str = ""
    print("Input the message. Use CTRL+D to memorize")
    while True:
        try:
            line: str = input()
        except EOFError:
            break
        message += line + "\n"
    memo_dictwrite(newid, title, message)


def memo_dictwrite(id: int, title: str, msg: str) -> None:
    data = {"title": title, "message": msg}
    _memodata_[id] = data
    print("You can use 'todo edit " + str(id) + "' to edit the memo")


def edit(id) -> None:
    if _memodata_[id]:
        newtitle: str = input_prefill("Title: ", _memodata_[id]["title"])
        newmessage: str = input_prefill("Message: ", _memodata_[id]["message"])
        memo_dictwrite(id, newtitle, newmessage)
    else:
        print("There is no ToDo with the specified ID")


def view(id) -> None:
    if _memodata_[id]:
        print(_memodata_[id]["title"])
        print(35*"-")
        print(_memodata_[id]["message"])
    else:
        print("There is no TODO with the specified ID")


def write_memos() -> None:
    filename = open(_memofile_, "w")
    filename.write(json.dumps(_memodata_))
    filename.close()


exist_check()
load_memos()
if len(argv) == 1:
    list()
elif len(argv) <= 3:
    argument = str(argv[1]).lower()
    if argument in ["list", "l"]:
        list()
    elif argument in ["view", "v"]:
        if (len(argv) == 3):
            view(argv[2])
        else:
            print("Not enough arguments")
            print("Use 'todo v <id>'")
    elif argument in ["add", "a"]:
        makenewmemo()
        write_memos()
    elif argument in ["delete", "d"]:
        if (len(argv) == 3):
            delete(argv[2])
            write_memos()
        else:
            print("Not enough arguments")
            print("Use 'todo d <id>'")
    elif argument in ["edit", "e"]:
        if (len(argv) == 3):
            edit(argv[2])
            write_memos()
        else:
            print("Not enough arguments")
            print("Use 'todo e <id>'")
else:
    print("Too many arguments!")
