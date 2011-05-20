#!/usr/bin/env python

import events

class Controller:
    def __init__(self, eventmanager):
        self.listen_for = events.ViewEvent
        self.eventmanager = eventmanager
        self.eventmanager.registerlistener(self)

    def notify(self, event):
        if isinstance(event, events.WaitForGameStartEvent):
            input("Press Enter to start game.")
            self.eventmanager.post(events.GameStartRequest())
        elif isinstance(event, events.WaitForHandStartEvent):
            input("Press Enter to start hand.")
            self.eventmanager.post(events.HandStartRequest())
            self.eventmanager.post(events.DealRequest()) # temporary
