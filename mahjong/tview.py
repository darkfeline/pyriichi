#!/usr/bin/env python3

import events.model
import events.view

class View:
    def __init__(self, eventmanager, model):
        self.listen_for = events.model.ModelEvent
        self.eventmanager = eventmanager
        self.model = model

    def startmenu(self):
        self.clear()
        print('Welcome to PyRiichi')
        self.eventmanager.post(events.view.WaitForGameStartEvent())

    def showscore(self):
        self.clear()

        print("Scores")
        for x in range(4):
            print("Player {}:{}".format(x + 1, self.model.players[x].points))
        print("Next dealer is Player " + str(self.model.dealer + 1))
        print("(Original dealer is Player " + str(self.model.home + 1) + ")")


    def showhand(self):
        self.clear()

        print("Scores")
        for x in range(4):
            print("Player " + str(x + 1), end="")
            #if x == 0:
            #    print(" (E)", end="")
            print(":", end="")
            print(self.model.players[x].points)
        print()
        
        print("Discards")
        for x in range(4):
            print("Player {} ({}): ".format((self.model.dealer + x) % 4 + 1, 
                        ['E', 'S', 'W', 'N'][x]), end="")
            for tile in self.model.hand.players[x].hand:
                try:
                    tile.hidden
                except AttributeError:
                    pass
                else:
                    print(tile, end=" ")
            print()
        print()

        print("Declared")
        for x in range(4):
            print("Player {} ({}): ".format((self.model.dealer + x) % 4 + 1, 
                        ['E', 'S', 'W', 'N'][x]), end="")
            for set in self.model.hand.players[x].sets:
                for tile in set:
                    print(tile, end=" ")
                print(end=" ")
            print()
        print()

        print("Hand")
        x = self.model.hand.current_player
        p = self.model.players[x]
        for tile in p.hand:
            print(tile, end=" ")

    def clear(self):
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

    def notify(self, event):
        if isinstance(event, events.model.GameStartEvent):
            self.showscore()
            self.eventmanager.post(events.view.WaitForHandStartEvent())
        elif isinstance(event, events.model.HandStartEvent):
            self.showhand()  # this is temporary


