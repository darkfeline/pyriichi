#!/usr/bin/env python3

import pygame
import mahjong.cpu
import mahjong.events
import mahjong.controller
import mahjong.view
import mahjong.model

def main():
    # init stuff
    em = mahjong.events.EventManager()
    cpu = cpu.CPU(em)

    cpu.run()


if __name__=="__main__":
    main()
