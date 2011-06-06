#!/usr/bin/env python

from weakref import WeakKeyDictionary
import re

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
            self.running = 1
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
                try:
                    for type in listener.listen_for:
                        if isinstance(event, type):
                            listener.notify(event)
                except TypeError:
                    if isinstance(event, listener.listen_for):
                        listener.notify(event)
        self.running = 0


class TickingEventManager(EventManager):
    def post(self, event):
        self.events.append(event)
        if isinstance(event, TickEvent):
            self.running = 1
            self.send()


# Base Event---------------------------------------------------
class Event:
    def __init__(self):
        self.name = "Event"

    def __str__(self):
        return self.name
    
    def _strip(self):
        return re.sub(r'\s', '', self.name)

    def __repr__(self):
        return self._strip() + "()"


# Global Events--------------------------------------------------
class TickEvent(Event):
    def __init__(self):
        self.name = "Tick Event"


class SecondEvent(Event):
    def __init__(self):
        self.name = "Second Event"


class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit Event"


# Event Manager Events-----------------------------------------
class EventManagerEvent(Event):
    def __init__(self):
        self.name = "Event Manager Event"


class AddListenerEvent(EventManagerEvent):
    def __init__(self, listener):
        self.name = "Add Listener Event"
        self.listener = listener

    def __repr__(self):
        return self._strip() + '(' + str(self.listener) + ')'


class RemoveListenerEvent(EventManagerEvent):
    def __init__(self, listener):
        self.listener = listener
        self.name = "Remove Listener Event"

    def __repr__(self):
        return self._strip() + '(' + str(self.listener) + ')'


# Model Events----------------------------------------
class ModelEvent(Event):
    def __init__(self):
        self.name = "Model Event"


class GameStartedEvent(ModelEvent):
    def __init__(self):
        self.name = "Game Start Event"


class HandStartedEvent(ModelEvent):
    def __init__(self):
        self.name = "Hand Start Event"


class HandEndedEvent(ModelEvent):
    def __init__(self):
        self.name = "Hand End Event"


class ModelRequest(ModelEvent):
    def __init__(self):
        self.name = "Model Request"
        

class GameStartRequest(ModelRequest):
    def __init__(self):
        self.name = "Game Start Request"


class HandStartRequest(ModelRequest):
    def __init__(self):
        self.name = "Hand Start Request"


class DealRequest(ModelRequest):
    def __init__(self):
        self.name = "Deal Request"


# Client Event-----------------------------------------
class ClientEvent(Event):
    def __init__(self):
        self.name = "Client Event"


class ServerConnectEvent(ClientEvent):
    def __init__(self, server):
        self.name = "Server Connect Event"
        self.server = server


# Server Event-----------------------------------------
class ServerEvent(Event):
    def __init__(self):
        self.name = "Server Event"


class ClientConnectEvent(ServerEvent):
    def __init__(self, client, avatarID):
        self.name = "Client Connect Event"
        self.client = client
        self.avatarID = avatarID


class ClientDisconnectEvent(ServerEvent):
    def __init__(self, avatarID):
        self.name = "Client Disconnect Event"
        self.avatarID = avatarID
        

class FatalEvent(ServerEvent):
    def __init__(self, *args):
        self.name = "Fatal Event"
        self.args = args
