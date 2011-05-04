#!/usr/bin/env python

import pygame

import model.cpu
import events.manager
import tcontroller
import tview
import model.game

def main():
    # init stuff
    em = events.manager.EventManager()
    cp = model.cpu.CPU(em)

    m = model.game.Game(em)
    v = tview.View(em, m) 
    c = tcontroller.Controller(v, m)
    em.registerlistener(v)
    em.registerlistener(c)

    #cp.run()
    v.startmenu()


if __name__=="__main__":
    main()
