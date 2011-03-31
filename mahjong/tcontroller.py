#!/usr/bin/env python3

import tview

class Controller:
    def __init__(self, view, model):
        self.listen_for = tview.ViewEvent
        self.view = view
        self.model = model

        self.view.startmenu()
        self.model.start()

    def notify(self, event):
        if isinstance(event, tview.WaitForStartEvent):
            input()
            self.model.start()
        elif isinstance(event, tview.WaitEvent):
            input()
