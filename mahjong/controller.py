#!/usr/bin/env python3

import pygame
import mahjong.cpu

class Controller:
    def __init__(self, mediator):
        self.listen_types = (cpu.TickEvent,)
        self.mediator = mahjong.mediator.Mediator()
    def notify(self, ev):
        if isinstance(ev, cpu.TickEvent):
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.mediator.post(ControllerEvent('quit'))
                elif ev.type == pygame.KEYDOWN:
                    pass
                elif (ev.type == pygame.MOUSEBUTTONDOWN and
                      pygame.mouse.get_pressed()[0]):
                    tmp = MouseClickEvent(pygame.mouse.get_pos())
                    self.mediator.post(tmp)
                elif (ev.type == pygame.MOUSEBUTTONUP and not
                      pygame.mouse.get_pressed()[0]):
                    tmp = MouseUpEvent()
                    self.mediator.post(tmp)


class ControllerEvent:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return repr(self.val)


class MouseEvent:
    pass


class MouseClickEvent(MouseEvent):
    def __init__(self, pos):
        self.pos = pos

    def __getitem__(self, key):
        return self.pos[key]


class MouseUpEvent(MouseEvent):
    pass
