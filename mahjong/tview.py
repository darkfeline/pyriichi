#!/usr/bin/env python3

import model

class View:
    def __init__(self, eventmanager, model):
        self.listen_for = model.ModelEvent
        self.eventmanager = eventmanager
        self.model = model

    def startmenu(self):
        self.clear()
        print('Welcome to PyRiichi')
        self.eventmanager.post(WaitForStartEvent())

    def showUI(self):
        self.clear()

        print("Scores")
        for x in range(4):
            print("Player {}:{}".format(x + 1, self.model.players[0]), end=" ")
            if x == 0:
                print("(E)", end="")
        print()
        
        print("Discards")
        for x in range(4):
            print("Player {} ({}): ".format((self.model.dealer + x + 1) % 4, 
                        ['E', 'S', 'W', 'N'][x]), end="")
            for tile in self.model.hand.players[x]:
                try:
                    tile.hidden
                except AttributeError:
                    pass
                else:
                    print(tile, end=" ")

        print("Declared")
        for x in range(4):
            for tile in self.model.hand.players[x].sets:
                pass


    def clear(self):
        print('\n\n\n\n\n\n\n\n\n\n')

    def notify(self, event):
        pass


class ViewEvent:
    pass


class WaitForStartEvent(ViewEvent):
    pass


class WaitEvent(ViewEvent):
    pass
