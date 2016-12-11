#!/usr/bin/env python3
from sys import argv
from os.path import join, exists, isdir, splitext
from os import getenv, listdir, makedirs, remove, system
import json
_directory_ = join(getenv("HOME"), ".todo")


def dir_check():
    if exists(_directory_):
        if not isdir(_directory_):
            print("Couldn't create directory .todo, ",
                  "a file with the same name exists")
    else:
        makedirs(_directory_)


def list():
    lst = listdir(_directory_)
    if not lst:
        print("There are no TODOs to Show")
    else:
        for item in lst:
            name = splitext(item[0])
            data = None
            with open(join(_directory_, item), "r") as fil:
                data = json.loads(fil.read())
            toshow = "[" + str(name[0]) + "]"
            if data["message"]:
                toshow += " [M]"
            toshow += " " + data["title"]
            print(toshow)


def get_newname():
    lst = listdir(_directory_)
    if lst == []:
        return 1
    else:
        numlst = [int(splitext(x)[0]) for x in lst]
        return max(numlst) + 1


def delete(name):
    fil = join(_directory_, name+".json")
    if exists(fil):
        remove(fil)
    else:
        print("There is no ToDo with the specified ID")


def add(text):
    name = str(get_newname())
    data = {"title": text, "message": ""}
    with open(join(_directory_, name+".json"), "w") as fil:
        fil.write(json.dumps(data))
    print("Use 'todo edit " + name + "' to edit the file")


def edit(name):
    fil = join(_directory_, name+".json")
    if exists(fil):
        system("`echo $EDITOR` " + join(_directory_, argv[2]+".json"))
        quit()
    else:
        print("There is no ToDo with the specified ID")


def view(name):
    fil = join(_directory_, name+".json")
    if exists(fil):
        with open(fil) as filename:
            data = json.loads(filename.read())
            print(data["title"])
            print(25*"-")
            print(data["message"])
    else:
        print("There is no ToDo with the specified ID")

dir_check()
if len(argv) == 1:
    list()
elif len(argv) <= 3:
    argument = str(argv[1]).lower()
    if argument in ["list", "l"]:
        list()
    elif argument in ["view", "v"]:
        view(argv[2])
    elif argument in ["add", "a"]:
        if len(argv) <= 2:
            print("Please specify a title")
        else:
            add(argv[2])
    elif argument in ["delete", "d"]:
        delete(argv[2])
    elif argument in ["edit", "e"]:
        edit(argv[2])

else:
    print("Too many arguments!")
