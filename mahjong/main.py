#!/usr/bin/env python3

import pygame
import cpu
import events
import controller
import view
import model

def main():
    # init stuff
    em = mahjong.events.EventManager()
    cpu = cpu.CPU(em)

    cpu.run()


if __name__=="__main__":
    main()
