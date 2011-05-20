#!/usr/bin/env python

from twisted.spread import pb
from twisted.internet.selectreactor import SelectReactor
from twisted.internet.main import installReactor

import events
import network
import game

class NetworkServerView(twisted.spread.pb.Root):
    STATE_PREPARING = 0
    STATE_CONNECTING = 1
    STATE_CONNECTED = 2
    STATE_DISCONNECTING = 3
    STATE_DISCONNECTED = 4

    def __init__(self, eventmanager, reg):
        self.eventmanager = eventmanager
        self.listen_for = events.Event
        self.eventmanager.registerlistener(self)

        self.pb_client_factory = pb.PBClientFactory()
        self.state = NetworkServerView.STATE_PREPARING
        self.reactor = None
        self.server = None

        self.shared_object_reg = reg

    def attempt_connection(self, server_host, server_port):
        self.state = NetworkServerView.STATE_CONNECTING
        if self.reactor:
            self.reactor.stop()
            self.pump_reactor()
        else:
            self.reactor = SelectReactor()
            installReactor(self.reactor)
        connection = self.reactor.connectTCP(server_host, server_port,
                                             self.pb_client_factory)
        deferred = self.pb_client_factory.getRootObject()
        deferred.addCallback(self.connected)
        deferred.addErrback(self.connect_failed)
        self.reactor.startRunning()

    def disconnect(self):
        if not self.reactor:
            return
        self.reactor.stop()
        self.pump_reactor()
        self.state = NetworkServerView.STATE_DISCONNECTING

    def connected(self, server):
        self.server = server
        self.state = NetworkServerView.STATE_CONNECTED
        event = events.ServerConnectEvent(server)
        self.eventmanager.post(event)

    def connect_failed(self, server):
        self.eventmanager.post(events.QuitEvent())
        self.state = NetworkServerView.STATE_DISCONNECTED

    def pump_reactor(self):
        self.reactor.runUntilCurrent()
        self.reactor.doIteration(0)

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            if self.state == NetworkServerView.STATE_PREPARING:
                self.attempt_connection()
            elif self.state in [NetworkServerView.STATE_CONNECTED,
                                NetworkServerView.STATE_DISCONNECTING,
                                NetworkServerView.STATE_CONNECTING]:
                self.pump_reactor()
            return

        elif isinstance(event, events.QuitEvent):
            self.disconnect()
            return

        elif not isinstance(event, pb.Copyable):
            name = event.__class__.__name__
            copyable_name = "Copyable" + name
            if not hasattr(network, copyable_name):
                return
            copyable_class = getattr(network, copyable_name)
            if copyable_class not in network.client2server_events:
                return
            event = copyable_class(event, self.shared_object_reg)

        if event.__class__ not in network.client2server_events:
            return

        if self.server:
            self.server.callRemote("network_event", event)

            
class NetworkServerController(pb.Referenceable):
    def __init__(self, eventmanager):
        self.eventmanager = eventmanager
        self.eventmanager.registerlistener(self)

    def remote_server_event(self, event):
        self.eventmanager.post(event)
        return 1

    def notify(self, event):
        if isinstance(event, events.ServerConnectEvent):
            event.server.callRemote("client_connect", self)


def start_client():
    em = events.TickingEventManager()
    reg = {}

if __name__ == "__main__":
    start_client():
