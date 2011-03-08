#!/usr/bin/env python3

import pygame.sprite

class Manager(pygame.sprite.Group):
    def __init__(self, display, mediator):
        pygame.sprite.Group.__init__()
        self.listen_types = event.ButtonRequest,
        self.display = display
        self.mediator = mediator
        self.images = {}
        path = os.path.join('images', 'buttons')
        for img in os.listdir(path):
            if img.endswith('.gif'):
                self.images[img[:-4]] = pygame.image.load(os.path.join(path,
                                                                       img))

    def add(self, button, loc):
        sprite = pygame.sprite.Sprite()
        sprite.image, sprite.rect = self.images[button], self.image[button].rect
        sprite.rect.topleft = loc
        pygame.sprite.Group.add(self, sprite)

    def notify(self, ev):
        pass


class Controller:
    def __init__(self, eventmanager):
        self.listen_types = event.ButtonControllerRequest, event.MouseEvent
        self.eventmanager = eventmanager
        self.buttons = []
        self.waiting = {}
        self.clicked = None
    
    def checkbutton(self, button, pos):
        """
button
    tuple(button name, rect, event)
pos
    pos of mouse click

"""
        rect = button[1]
        if (rect.left[0] < pos[0] < rect.right[0] and 
            rect.up[1] < pos[1] < rect.down[1]):
            self.clicked = button
            tmp = event.ButtonBlitRequest(button[0], rect, 1)
            self.eventmanager.post(tmp)

    def notify(self, ev):
        if isinstance(ev, event.AddButtonRequest):
            self.eventmanager.post(event.ButtonBlitRequest(ev.button,
                                                           ev.loc))
            self.waiting[ev.button] = (ev.button, ev.ev)
        elif isinstance(ev, event.AddRectRequest):
            self.buttons.append(tuple(self.waiting[ev.button][0], ev.rect,
                                      self.waiting[ev.button][1]))
            del self.waiting[ev.button]
        elif isinstance(ev, event.MouseClickEvent):
            for k in self.buttons.keys():
                checkbutton(k[1], ev.pos)
        elif isinstance(ev, event.MouseUpEvent):
            tmp = event.ButtonBlitRequest(self.clicked[0], self.clicked[1])
            self.eventmanger.post(tmp)
            self.eventmanager.post(self.clicked[2])
            self.clicked = None
