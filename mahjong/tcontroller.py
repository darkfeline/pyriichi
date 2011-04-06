#!/usr/bin/env python3

import events.view

class Controller:
    def __init__(self, view, model):
        self.listen_for = events.view.ViewEvent
        self.view = view
        self.model = model

        self.view.startmenu()
        self.model.start()

    def notify(self, event):
        if isinstance(event, events.view.WaitForGameStartEvent):
            input()
            self.model.start()
        elif isinstance(event, events.view.WaitForHandStartEvent):
            input()
            self.model.start_hand()
