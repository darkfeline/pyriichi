#!/usr/bin/env python3

import pygame
import cpu
import events
import tcontroller
import tview
import model

def main():
    # init stuff
    em = mahjong.events.EventManager()
    cp = cpu.CPU(em)

    m = model.Game(em)
    v = tview.View(em, m) 
    c = tcontroller.Controller(v, m)
    em.registerlistener(v)
    em.registerlistener(c)

    cp.run()


if __name__=="__main__":
    main()
