#!/usr/bin/env python

import events.view

class Controller:
    def __init__(self, view, model):
        self.listen_for = events.view.ViewEvent
        self.view = view
        self.model = model

    def notify(self, event):
        if isinstance(event, events.view.WaitForGameStartEvent):
            input("Press Enter to start game.")
            self.model.start()
        elif isinstance(event, events.view.WaitForHandStartEvent):
            input("Press Enter to start hand.")
            self.model.start_hand()
            self.model.hand.deal() # temporary
