#!/usr/bin/env python

import random

import events.model
import model.player
import model.wall

class Hand:
    """Hand Flow Diagram

__init__()
deal()
    draw()<---------
    |-->addkan()   |    
    |   |-->...    |
    |-->ckan()     |
    |   |-->...    |
    --->agari()    |
    discard()      |
    |-->chi()------|
    |-->pon()------|
    |-->kan()------|
    --->agari()    |
    cycle()---------
abort()

Implementation notes
    Currently, only one person can declare agari.  Whoever is closest to east
    wins Nagashi Mangan if there are two players who can win on it.  

"""
    def __init__(self, round_wind, dealer, honba, riichi_pot, players):
        """round_wind
    current round wind as an int in range(4)
dealer
    current dealer as int in range(4)
honba
    number of repeat counters
riichi_pot
    points in riichi pot
players
    original player list.  Hand will reorder hand internally so that the dealer is the
    first item.

Attributes set after winning:

scores
    changes in score for all players
yaku
    list of yaku

"""
        self.round_wind = round_wind
        self.honba = honba
        self.riichi_pot = riichi_pot
        self.players = players[dealer:] + players[:dealer]
        for player in self.players:
            player.clear()
        self.wall = model.wall.Wall()
        self.dice = Dice()

        self.current_player = 0
        self.current_discard = None
        self.first_round = 1
        # after_kan = 1
        #   after kan declaration; score for rinchan kaihou
        # after_kan = 2
        #   after adding to kan; use for both rinchan kaihou and chan kan
        self.after_kan = 0

        # Flags*******************************************************
        # step=0 beginning of turn
        # step=1 current player has drawn/claimed tile
        # step=2 current player has discarded
        # step=-1 hand is over
        self.step = 0

    def deal(self):
        """Rolls dice and calls Wall.deal()."""
        roll = self.dice.roll()
        self.wall.deal(roll, self.players)

    def draw(self):
        """Current player draws.  If player has ippatsu flag, ippatsu is unset
        (one round has passed).  """
        if self.step == 0:
            player = self.players[self.current_player]
            if player.ippatsu:
                player.ippatsu = 0
            try:
                player.draw(self.wall)
            except WallEmptyError:
                self.abort()
            self.step = 1

    def discard(self, tile):
        """If draw flag is set, discard tile for current player and set discard
flag.

tile
    reference to tile to discard

"""
        if self.step == 1:
            player = self.players[self.current_player]
            player.discard(tile)

            self.current_discard = tile
            self.step = 2

    def agari(self, player):
        """Player calls win on current player's discard or self-draw.

Finds and scores all possible sets and uses highest score.  Sets self.scores
with array of score differences to be used by parent Game class.  

player
    player by index number
    
""" 
        playeri = self.players[player]
        east = 0
        if player is self.players[0]:
            east = 1
        winds = [self.round_wind, ['E', 'S', 'W', 'N'][player]]
        bonus = []

        # Set flags on player's tiles
        if self.current_player != player:
            self.current_discard.last = 1
            self.current_discard.ron = 1
            playeri.hand.append(self.current_discard)

            # renhou test
            if self.first_round:
                bonus.append('renhou')

            # chan kan test
            if self.after_kan == 2:
                bonus.append('chan kan')
                self.after_kan = 0
        else:
            playeri.current_draw.last = 1
            playeri.current_draw.tsumo = 1

            # tenhou/chihou test
            if self.first_round:
                if east:
                    bonus.append('tenhou')
                else:
                    bonus.append('chihou')


        # Add bonuses
        if len(self.wall) < 1:
            bonus.append("haitei")
        if playeri.riichi:
            bonus.append('riichi')
        if playeri.ippatsu:
            bonus.append('ippatsu')
        if playeri.double_riichi:
            bonus.append('daburu_riichi')
        if self.after_kan:
            bonus.append('rinchan kaihou')
        dora = self.wall.dora()
        ura = self.wall.ura()

        # Superceded by model.scoring.highest_score()
        ## Find all possible scores
        #possible = scoring.makesets(playeri.hand)
        #scorelist = []
        #for x in possible:
        #    y = playeri.sets[:]
        #    y.extend(x)
        #    scorelist.append(
        #        scoring.score(
        #            east, winds, *y, honba=self.honba, bonus=bonus,
        #            dora=dora, ura=ura
        #        )
        #    )

        ## Find highest score
        #max = 0
        #try:
        #    max_score = scorelist[max][0][0]
        #except TypeError:
        #    max_score = scorelist[max][0]
        #for i in range(1, len(scorelist)):
        #    try:
        #        current = scorelist[i][0][0]
        #    except TypeError:
        #        current = scorelist[i][0]
        #    if current > max_score:
        #        max = i
        #        max_score = current
        max = model.scoring.highest_score(
                east, winds, playeri.hand, playeri.sets, 
                honba=self.honba, bonus=bonus, dora=dora, ura=ura
        )

        # Calculate array of point differences
        x, self.yaku = max
        diff = []
        try:
            for i in range(1,4):
                diff[i] = -x[0]
            diff[0] = -x[1]
            diff[player] = 0
            diff[player] = -sum(diff)
        except TypeError:
            for i in range(4):
                diff[i] = -x
            diff[player] = 0
            diff[player] = -sum(diff)

        self.scores = tuple(diff)

    def abort(self):
        """Checks for Nagashi Mangan.  If a player satisfies conditions, wins
        off Nagashi Mangan, else sets self.scores as zeroed tuple."""
        for num, player in enumerate(self.players):
            if scoring.isnagashi(player.discards):
                if num == 0:
                    east = 1
                else:
                    east = 0
                winds = [self.round_wind, ['E', 'S', 'W', 'N'][num]]
                score = scoring.score(east, winds, honba=self.honba,
                                      bonus=['nagashi mangan']) 
                diff = []
                try:
                    for i in range(1,4):
                        diff[i] = -x[0]
                    diff[0] = -x[1]
                    diff[player] = 0
                    diff[player] = -sum(diff)
                except TypeError:
                    for i in range(4):
                        diff[i] = -x
                    diff[player] = 0
                    diff[player] = -sum(diff)
                self.scores = tuple(diff)
                return
        self.scores = (0, 0, 0, 0)

    def pon(self, player):
        """Player calls current player's discard.
        
player
    player by index
    
"""
        x = self.players[player]
        # hide in current player's discards
        self.current_discard.hidden = 1

        x.hand.append(self.current_discard)
        x.sort()
        set = []
        for i in range(3):
            for tile in x.hand:
                if tile.cmpval == self.current_discard.cmpval:
                    set.append(tile)
                    break
        x.pon(set)
        # change current player
        self.current_player = player
        # counts as draw
        self.step = 1
        # interrupts first round
        if self.first_round:
            self.first_round = 0

    def kan(self, player):
        """Player calls current player's discard.  Use ckan() for concealed kan.  
        
player
    player by index
    
"""
        x = self.players[player]
        # hide in current player's discards
        self.current_discard.hidden = 1

        x.hand.append(self.current_discard)
        x.sort()
        set = []
        for i in range(4):
            for tile in x.hand:
                if tile.cmpval == self.current_discard.cmpval:
                    set.append(tile)
                    break
        x.kan(set, self.wall)
        # change current player
        self.current_player = player
        # counts as draw
        self.step = 1
        self.after_kan = 1
        # interrupts first round
        if self.first_round:
            self.first_round = 0

    def ckan(self, tiles):
        """Current player declares concealed kan.
        
tiles
    list of tiles that compose the kan
    
"""
        if len(tiles) == 4:
            player = self.players[self.current_player]
            player.ckan(tiles, self.wall)
            self.after_kan = 1

    def addkan(self, tile):
        """Current player adds tile to pon."""
        player = self.players[self.current_player]
        self.current_discard = tile
        player.addkan(tile, self.wall)
        self.after_kan = 2

    def chi(self, tiles):
        """Player calls current player's discard.
        
tiles
    list of two tiles with which the current discard is to form a chi

"""
        x = self.players[(self.current_player + 1) % 4]
        # hide in current player's discards
        self.current_discard.hidden = 1

        x.hand.append(self.current_discard)
        x.sort()
        tiles.append(self.current_discard)
        x.chi(tiles)
        # change current player
        self.current_player += 1
        self.current_player %= 4
        # counts as draw
        self.step = 1
        # interrupts first round
        if self.first_round:
            self.first_round = 0

    def cycle(self):
        """Ends player turn by resetting flags and cycling to the next
        player."""
        if self.step == 2:
            self.step = 0
            self.current_discard = None
            self.current_player += 1
            if self.first_round and self.current_player > 4:
                self.first_round = 0
            self.after_kan = 0
            self.current_player %= 4


class Game:
    def __init__(self, eventmanager):
        """Need to call self.start() to get things going."""
        self.eventmanager = eventmanager

    def start(self):
        """Sets round wind, dealer, honba, riichi pot, players"""
        self.round_wind = 0
        self.home = 0   # starting dealer
        self.dealer = 0
        self.honba = 0
        self.riichi_pot = 0
        self.players = [ model.player.Player(x) for x in range(4) ]
        self.eventmanager.post(events.model.GameStartEvent())

    def cycle(self):
        """Cycles current dealer and each player's wind.  If it is again the
original east's turn, cycle round wind."""
        self.dealer += 1
        self.dealer %= 4
        for player in self.players:
            player.cycle_wind()
        if self.dealer == self.home:
            self.wind += 1
            self.wind %= 4

    def start_hand(self):
        """Returns hand; creates hand instance if none exists."""
        if not self.has_hand():
            self.hand = Hand(self.round_wind, self.dealer, self.honba,
                             self.riichi_pot, self.players)
            self.eventmanager.post(events.model.HandStartEvent())
        return self.hand

    def has_hand(self):
        """Returns True if a hand instance currently exists and False
        otherwise."""
        try:
            self.hand
        except AttributeError:
            return False
        else:
            return True

    def end_hand(self):
        """Kills current hand instance and grabs information."""
        scores = (self.hand.scores[-self.dealer:] +
                  self.hand.scores[:-self.dealer])
        if not scores[0] == scores[1] == scores[2] == scores[3] == 0:
            yaku = self.hand.yaku
            for i in range(4):
                self.players[i].points += scores[i]
            self.honba = 0
            self.cycle()
        else:
            self.honba += 1
        self.eventmanager.post(events.model.HandEndEvent())
        del self.hand


class Dice:
    """Two six-sided die."""
    def __init__(self):
        random.seed()
    def roll(self):
        """Returns 2d6"""
        return random.randint(1, 6) + random.randint(1, 6)
