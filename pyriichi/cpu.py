#!/usr/bin/env python

import pygame

import events

class CPU:
    """CPU Class periodically posts TickEvent at 60 fps max."""
    def __init__(self, eventmanager):
        self.clock = pygame.time.Clock()
        self.eventmanager = eventmanager

    def run(self):
        self.running = 1
        while self.running:
            time_passed = self.clock.tick(60)
            self.eventmanager.post(events.TickEvent())

    def stop(self):
        self.running = 0