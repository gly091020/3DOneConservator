# -*- coding: utf-8 -*-
import os.path

pai_chu = []


def get_is_have_file():
    for f in os.listdir(path):
        if f in pai_chu:
            continue
        if os.path.splitext(f)[1] == ".Z1":
            return os.path.join(path, f)


def get_all_file():
    l = []
    for f in os.listdir(path):
        if os.path.splitext(f)[1] == ".Z1":
            l.append(f)
    return l


def clear_temp():
    for f in os.listdir(path):
        if os.path.splitext(f)[1] == ".Z1":
            os.remove(os.path.join(path, f))


def get_temp_path():
    return os.path.join(os.environ["USERPROFILE"], r"AppData\Roaming\3D One 2015 Chs (x64)\temp")


path = get_temp_path()
