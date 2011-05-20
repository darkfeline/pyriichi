#!/usr/bin/env python

#import twisted.protocols
from twisted.spread import pb

import events
import network

#class Protocol(twisted.protocols.basic.LineReceiver):
#    def lineReceived(self, data):
#        d = self.factory.getData(data)

#        def onError(err):
#            return 'Internal error in server'
#        d.addErrback(onError)

#        def writeResponse(message):
#            self.transport.write(message + '\r\n')
#            self.transport.loseConnection()
#        d.addCallback(writeResponse)


#class Factory(twisted.internet.protocol.ServerFactory):
#    protocol = Protocol

#    def getData(self, data):
#        return twisted.internet.defer.succeed("Hello World!")


class TextLogView:
    def __init__(self, eventmanager):
        self.eventmanager = eventmanager
        self.listen_for = events.Event
        self.eventmanager.registerlistener(self)
        self.log = open("server.log", "a")

    def notify(self, event):
        self.log.write(repr(event))


class NetworkClientController(pb.Root):
    def __init__(self, eventmanager, reg):
        self.eventmanager = eventmanager
        self.eventmanager.registerlistener(self)

        self.shared_object_reg = reg

    def remote_client_connect(self, client):
        ev = events.ClientConnectEvent(client)
        self.eventmanager.post(ev)
        return 1

    def remote_get_object_state(self, id):
        if not self.shared_object_reg.has_key(id):
            return [0, 0]
        obj = self.shared_object_reg[id]
        return [id, obj.get_state_to_copy(self.shared_object_reg)]

    def remote_network_event(self, event):
        self.eventmanager.post(event)
        return 1

    def notify(self, event):
        pass


class NetworkClientView:
    def __init__(self, eventmanager, reg):
        self.eventmanager = eventmanager
        self.listen_for = events.Event
        self.eventmanager.registerlistener(self)

        self.clients = []
        self.shared_object_reg = reg

    def sent_event(self, event):
        if not isinstance(ev, pb.Copyable):
            name = event.__class__.__name__
            copyable_name = "Copyable" + name
            if not hasattr(network, copyable_name):
                return None
            x = getattr(network, copyable_name)
            event = x(event, self.shared_object_reg)

        if event.__class__ not in network.server2client_events:
            return None

        return event

    def notify(self, event):
        if isinstance(event, events.ClientConnectEvent):
            self.clients.append(event.client)
        else:
            event = self.sent_event(event)
            if not event:
                return

            for client in self.clients:
                client.callRemote("server_event", event)


def startserver():
    from twisted.internet import reactor
    em = events.EventManager()
    reg = {}

    log = TextLogView(em)
    ncc = NetworkClientController(em, reg)
    ncv = NetworkClientView(em, reg)
    game = game.Game(em)
    reg[id(game)] = game

    reactor.listenTCP(8000, pb.PBServerFactory(ncc))
    reactor.run()

if __name__ == '__main__':
    startserver()
