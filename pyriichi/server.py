#!/usr/bin/env python

from pprint import pprint

from twisted.spread import pb
from twisted.spread.pb import DeadReferenceError
from twisted.cred import checkers, protal

import game
import events
import network
import logging

logging.add("server", "server.log")

class TextLogView:
    def __init__(self, eventmanager):
        self.eventmanager = eventmanager
        self.listen_for = events.Event
        self.eventmanager.registerlistener(self)
        self.log = logging.Log("events.log")

    def notify(self, event):
        self.log.write(str(event))


class TimerController:
    def __init__(self, eventmanager, reactor, reg):
        self.eventmanager = eventmanager
        self.eventmanager.registerlistener(self)
        self.listen_for = events.ServerEvent

        self.reactor = reactor
        self.num_clients = 0

        self.shared_object_reg = reg

    def app_started(self):
        self.reactor.callLater(1, self.Tick)

    def tick(self):
        if self.num_clients == 0:
            return

        self.eventmanager.post(events.TickEvent())
        self.reactor.callLater(1, self.Tick)

    def post_mortem(event):
        self.reactor.stop()
        logging.write("server", "FATAL EVENT. STOPPING REACTOR."
        x = logging.logs["server"]
        pprint(self.shared_object_reg, x)

    def notify(self, event):
        if isinstance(event, events.ClientConnectEvent):
            self.num_clients += 1
            if self.num_clients == 1:
                self.tick()
        elif isinstance(event, events.ClientDisconnectEvent):
            self.num_clients -= 1
        elif isinstance(event, events.FatalEvent):
            self.post_mortem(event)


class NetworkClientController(pb.Avatar):
    def __init__(self, eventmanager, avatarID, realm, reg):
        self.eventmanager = eventmanager

        self.avatarID = avatarID
        self.realm = realm

        self.shared_object_reg = reg

    def client_disconnect(self):
        self.eventmanager.post(events.ClientDisconnectEvent(self.avatarID))

    def perspective_get_sync(self):
        game = self.shared_object_reg.get_game()
        if game == None:
            raise Exception('Game unset')
        gameID = id(game)
        game_dict = game.get_state(self.shared_object_reg)

        return [gameID, game_dict]

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


class Model(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.game_key = None

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        if isinstance(val, game.Game):
            self.game_key = key

    def get_game(self):
        return self[self.game_key]


def startserver():
    from twisted.internet import reactor
    em = events.EventManager()
    reg = Model()

    log = TextLogView(em)
    ncc = NetworkClientController(em, reg)
    ncv = NetworkClientView(em, reg)
    game = game.Game(em)
    reg[id(game)] = game

    reactor.listenTCP(8000, pb.PBServerFactory(ncc))
    reactor.run()

if __name__ == '__main__':
    startserver()
