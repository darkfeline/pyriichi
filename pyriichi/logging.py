#!/usr/bin/env python

import os.path

class Log:
    def __init__(self, fn):
        self.file = os.path.join("logs", fn)

    def write(self, str):
        with open(self.file, "a") as f:
            f.write(str)


logs = {}

def add(key, fn):
    global logs
    x = Log(fn)
    logs[key] = x
    return x

def write(key, str):
    logs[key].write(str)

if __name__ == "__main__":
    add("test", "logtest.log")
    write("test", "writing to test log")
