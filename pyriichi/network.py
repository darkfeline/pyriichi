#!/usr/bin/env python

import twisted.spread.pb

server2client_events = []
client2server_events = []

def add_class(original, to_add):
    if to_add not in original.__bases__:
        original.__bases__ += tuple(to_add)

def add_copy_class(x):
    add_class(x, pb.Copyable)
    add_class(x, pb.RemoteCopy)
