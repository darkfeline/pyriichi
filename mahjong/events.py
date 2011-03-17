#!/usr/bin/env python3

from weakref import WeakKeyDictionary

class EventManager:
    def __init__(self):
        self.listeners = WeakKeyDictionary()
        self.events = []
        self.running = 0

    def registerlistener(self, listener):
        """Registers listener object.
        
listener
    reference to listener object
        
Listener definition:
listener.listen_for
listener.notify(event)

"""
        self.post(AddListenerEvent(listener))

    def unregisterlistener(self, listener):
        self.post(RemoveListenerEvent(listener))

    def post(self, event):
        """Post event to registered listeners who are set to receive that event
    type via listeners notify() method.  If EventManager isn't currently running (in
    a send loop), calls send().  
        
    """
        self.events.append(event)
        if not self.running:
            self.send()

    def send(self):
        """Sends events in stack."""
        while len(self.events) > 0:
            event = self.events.pop(0)
            if isinstance(event, EventManagerEvent):
                if isinstance(event, AddListenerEvent):
                    self.listeners[event.listener] = 1
                elif isinstance(event, RemoveListenerEvent):
                    del self.listeners[event.listener]
            for listener in self.listeners.keys():
                if event is self.listen_for or event in self.listen_for:
                    listener.notify(event)
        self.running = 0


class EventManagerEvent:
    pass


class AddListenerEvent(EventManagerEvent):
    def __init__(self, listener):
        self.listener = listener


class RemoveListenerEvent(EventManagerEvent):
    def __init__(self, listener):
        self.listener = listener


