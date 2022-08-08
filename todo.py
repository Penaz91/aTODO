#!/usr/bin/env python3
from os.path import join, exists, isdir
from os import getenv
import json
import readline
import collections
import argparse
import typing
import tempfile
from subprocess import call
_memofile_: str = join(getenv("HOME", "/"), ".todo")
_memodata_: dict = {}
_hasfile_: bool = False


EDITOR = getenv("EDITOR", "vi")


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
        _ordereddata_ = collections.OrderedDict(
            sorted(
                _memodata_.items(),
                key=lambda x: int(x[0])
            )
        )
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
    keylist: typing.List = [int(key) for key in _memodata_.keys()]
    newid: int = max(keylist) + 1
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


def edit_legacy(id) -> None:
    if _memodata_[id]:
        newtitle: str = input_prefill("Title: ", _memodata_[id]["title"])
        newmessage: str = input_prefill("Message: ", _memodata_[id]["message"])
        memo_dictwrite(id, newtitle, newmessage)
    else:
        print("There is no ToDo with the specified ID")


def edit(id) -> None:
    if _memodata_[id]:
        # Prepare a tempfile to open in editor
        title: str = input_prefill("Title: ", _memodata_[id]["title"])
        message: str = _memodata_[id]["message"]
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tmp") as fh:
            fh.write(message)
            fh.flush()
            call([EDITOR, fh.name])
            fh.seek(0)
            message = fh.read()
        memo_dictwrite(id, title, message)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", help="Action to perform", type=str,
        choices=(
            "list", "l", "view", "v", "add", "a", "edit", "e", "d", "delete"
        ),
        nargs="?", default="l"
    )
    parser.add_argument(
        "todo_id", nargs="?", default="", help="Todo ID", type=str
    )
    parser.add_argument(
        "--legacy", help="Use legacy editing action", action="store_true"
    )
    args = parser.parse_args()
    exist_check()
    load_memos()
    # ----- listing -----
    if args.action.lower() in ("list", "l"):
        list()
    # ----- viewing -----
    if args.action.lower() in ("view", "v"):
        if args.todo_id != "":
            view(args.todo_id)
        else:
            print("Not enough arguments")
            print("Use 'todo v <id>'")
    # ----- creation -----
    if args.action.lower() in ("add", "a"):
        makenewmemo()
        write_memos()
    # ----- deletion -----
    if args.action.lower() in ("delete", "d"):
        if args.todo_id != "":
            delete(args.todo_id)
            write_memos()
        else:
            print("Not enough arguments")
            print("Use 'todo d <id>'")
    # ----- editing -----
    if args.action.lower() in ("edit", "e"):
        if args.todo_id != "":
            if args.legacy:
                edit_legacy(args.todo_id)
            else:
                edit(args.todo_id)
            write_memos()
        else:
            print("Not enough arguments")
            print("Use 'todo e <id>'")


if __name__ == '__main__':
    main()
