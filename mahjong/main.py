#!/usr/bin/env python3

import pygame
import mahjong.cpu
import mahjong.mediator
import mahjong.controller
import mahjong.view
import mahjong.model

def main():
    # init stuff
    mediator = mahjong.mediator.Mediator()
    cpu = cpu.CPU(mediator)

    cpu.run()


if __name__=="__main__":
    main()
