#!/usr/bin/env python3

class Mediator:
    def __init__(self):
        self.model = None
        self.view = None
        self.controller = None

    def add_model(self, model):
        self.model = model
        model.mediator = self

    def add_view(self, view):
        self.view = view
        view.mediator = self

    def add_controller(self, controller):
        self.controller = controller
        controller.mediator = self


