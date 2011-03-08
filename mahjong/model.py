#!/usr/bin/env python3

import mahjong.scoring
import mahjong.tiles
import random

class Player:
    def __init__(self, wind_num, points=25000):
        """wind_num
    the player's wind from ['east', 'south', 'west', 'north']
points
    player points

"""
        self.points = points
        self.wind = wind_num
        self.clear()

    def __len__(self):
        """Returns number of tiles in player's hand."""
        return len(self.hand)

    def draw(self, wall):
        """Add tile drawn from wall to hand."""
        self.current_draw = wall.draw()
        self.hand.append(self.current_draw)
        self.sort()

    def discard(self, tile):
        """Discard a tile in hand and add to player's discards."""
        self.hand.remove(tile)
        self.discards.append(tile)
        self.clear_draw()

    def clear_draw(self):
        """Clears self.current_draw, which references the instance of the tile
        currently "drawn."

"""
        del self.current_draw
        
    def cycle_wind(self):
        self.wind += 1
        self.wind %= 4

    def clear(self):
        """Resets attributes for new hand.  Clears tiles in hand."""
        self.hand = []
        self.sets = []
        self.discards = []
        self.riichi = 0
        self.double_riichi = 0
        self.ippatsu = 0

    def riichi(self, double=False):
        """Declare riichi.  Raises RiichiException if riichi is already declared.
        
double
    include yaku for double riichi.  Defaults to False. 
    
"""
        if self.riichi:
            raise RiichiException(0, 1)
        if self.points >= 1000:
            raise RiichiException(1)
        self.points -= 1000
        self.riichi = 1
        self.ippatsu = 1
        if double:
            self.double_riichi = 1

    def sort(self):
        """Sort player's hand in place."""
        mahjong.scoring.sort(self.hand)

    def iscomplete(self):
        return scoring.iscomplete(self.hand)

    def waits(self):
        return scoring.waits(self.hand)

    def chi(self, tiles):
        """Form a declared chi with tiles in hand.  When taking a discard, the
        tile should be added to the Player's hand prior to calling this method.

tiles
    list of tiles that form a chi

    """
        if scoring.ischi(tiles):
            set = []
            for tile in tiles:
                tile.chi = 1
                self.hand.remove(tile)
                set.append(tile)
            self.sets.append(set)
            self.clear_draw()
        else:
            raise ModelException("Player", "chi " + str(tiles))

    def pon(self, tiles):
        """Form a declared pon with tiles in hand.  When taking a discard, the
        tile should be added to the Player's hand prior to calling this method.

tiles
    list of tiles that form a pon

    """
        if scoring.ispon(tiles):
            set = []
            for tile in tiles:
                tile.pon = 1
                self.hand.remove(tile)
                set.append(tile)
            self.sets.append(set)
            self.clear_draw()
        else:
            raise ModelException("Player", "pon " + str(tiles))

    def kan(self, tiles, wall):
        """Form a declared kan with tiles in hand.  When taking a discard, the
        tile should be added to the Player's hand prior to calling this method.

tiles
    list of tiles that form a kan
wall
    Wall instance to draw replacement tile

    """
        if scoring.iskan(tiles):
            set = []
            for tile in tiles:
                tile.kan = 1
                self.hand.remove(tile)
                set.append(tile)
            self.sets.append(set)

            tile = wall.take()
            self.hand.append(tile)
            self.sort()
            self.current_draw = tile
        else:
            raise ModelException("Player", "kan:" + str(tiles))

    def ckan(self, tiles, wall):
        """Declares a concealed kan.
        
tiles
    list of tiles that form a kan
wall
    Wall instance to draw replacement tile

"""
        if scoring.iskan(tiles):
            set = []
            for tile in tiles:
                tile.ckan = 1
                self.hand.remove(tile)
                set.append(tile)
            self.sets.append(set)

            tile = wall.take()
            self.hand.append(tile)
            self.sort()
            self.current_draw = tile
        else:
            raise ModelException("Player", "ckan:" + str(tiles))

    def addkan(self, tile, wall):
        """Adds tile to declared kan.

tile
    tile to add to kan
wall
    Wall to draw replacement tile

"""
        if self.can_addkan(tile):
            self.hand.remove(tile)
            for x in self.sets:
                if (len(x) == 3 and x[0] == x[1] == x[3] == tile):
                    break
            for a in x:
                del a.pon
                a.kan = 1
                a.addedkan = 1
            x.append(tile)
            tile.kan = 1
            tile.addedkan = 1

    def can_pon(self, tile):
        """Returns True if Player can pon tile and False otherwise."""
        count = 0
        for x in self.hand:
            if x.cmpval == tile.cmpval:
                count += 1
            if count == 2:
                return True
        return False

    def can_kan(self, tile):
        """Returns True if Player can kan tile and False otherwise."""
        count = 0
        for x in self.hand:
            if x.cmpval == tile.cmpval:
                count += 1
            if count == 3:
                return True
        return False

    def can_ckan(self):
        """Returns a list of lists of tiles with which the Player can declare
        concealed kan."""
        count = mahjong.scoring.tocount(self.hand)
        possible = []
        for tilenum, num in enumerate(count):
            if num == 4:
                possible.append(tilenum)

        result = []
        for cmpval in possible:
            tmp = []
            for tile in self.hand:
                if tile.cmpval == cmpval:
                    tmp.append(tile)
            result.append(tmp)
        return result

    def can_addkan(self, tile):
        """Tests if Player can addkan(tile).  Returns True if Player has a pon
of the tile."""
        for x in self.sets:
            if len(x) == 3 and x[0] == x[1] == x[2] == tile:
                return True
        return False

    def can_chi(self, tile):
        """Returns number of chi Player can form with the tile."""
        try:
            tile.value
        except AttributeError:
            return 0
        else:
            val = tile.value
            start = ["PINZU", "SOUZU", "MANZU"].index(tile.type) * 9
            count = mahjong.scoring.tocount(self.hand)[start:start + 9]
            count[val - 1] += 1
            a = 0
            result = 0
            for i in range(9):
                if count[i] > 0:
                    a += 1
                    if a >= 3:
                        result += 1
                else:
                    a = 0
            return result


class Wall:
    def __init__(self):
        temp = []
        for suit in tiles.SUITS:
            for tile in suit:
                for i in range(4):
                    temp.append(tile())

        # swap in red fives
        red_done = [0, 0, 0]
        for i, x in enumerate(temp):
            if isinstance(x, tiles.P5) and not red_done[0]:
                temp[i] = tiles.P5R()
                red_done[0] = 1
            elif isinstance(x, tiles.S5) and not red_done[1]:
                temp[i] = tiles.S5R()
                red_done[1] = 1
            elif isinstance(x, tiles.M5) and not red_done[2]:
                temp[i] = tiles.M5R()
                red_done[2] = 1
            if sum(red_done) == 3:
                break

        random.seed()
        for i in range(10):
            random.shuffle(temp)
        self.walls = []
        # build walls
        for i in range(4):
            wall = []
            for j in range(17 * 2):
                randint = random.randrange(len(temp))
                wall.append(temp.pop(randint))
            self.walls.append(wall)

    def __len__(self):
        """Total number of tiles in hand, including all four wall sections."""
        return sum([len(wall) for wall in self.walls])


    def draw(self):
        """Take next tile in wall (taking into consideration all four sections
and any breaks in wall.  If there are no more tiles in the wall, raise
WallEmptyException."""
        # in the beginning, if the dead wall was taken from the middle of a wall
        # section, may not draw from beginning of wall section
        if len(self) < 1:
            raise WallEmptyException()
        try:
            if self.sep >= len(self.walls[self.pointer]):
                del self.sep
                self.pointer = (self.pointer + 1) % 4
            return self.walls[self.pointer].pop(self.sep)
        except AttributeError:
            if len(self.walls[self.pointer]) < 1:
                self.pointer = (self.pointer + 1) % 4
            return self.walls[self.pointer].pop(0)

    def rdraw(self):
        """Reverse draw, for replacing dead wall tiles."""
        try:
            self.sep -= 1
            if self.sep <= 0:
                del self.sep
            return self.walls[self.pointer].pop(self.sep)
        except AttributeError:
            return self.walls[(self.pointer - 1) % 4].pop()

    def deal(self, roll, player_list):
        east = None
        for i, player in enumerate(player_list):
            if player.wind == 0:
                east = i
                break
        self.pointer = self.sep = (east + roll - 1) % 4
        # remember, wall goes clockwise, but players are counted
        # counterclockwise
        self.pointer = (self.pointer - 4) % 4

        # separate dead wall
        dead = []
        # where to divide the wall
        # tiles are double-stacked
        self.sep *= 2
        if self.sep >= 14:
            dead.extend(self.walls[self.pointer][self.sep - 14:self.sep])
            del self.walls[self.pointer][self.sep - 14:self.sep]
            self.sep -= 14
        else:
            dead.extend(self.walls[self.pointer][:self.sep])
            del self.walls[self.pointer][:self.sep]
            dead.reverse()
            self.sep = 14 - self.sep
            prev_wall = (self.pointer - 1) % 4
            self.sep = len(self.walls[prev_wall]) - self.sep
            temp = self.walls[prev_wall][self.sep:]
            temp.reverse()
            dead.extend(temp)
            del self.walls[prev_wall][self.sep:]
            del self.sep
        self.dead = DeadWall(dead, self)

        # deal
        for i in range(3):
            for j in range(4):
                player = (east + j) % 4
                player_list[player].draw(self)
                player_list[player].draw(self)
                player_list[player].draw(self)
                player_list[player].draw(self)
        for j in range(4):
                player = (east + j) % 4
                player_list[player].draw(self)
                player_list[player].sort()

    def dora(self):
        """Wrapper for respective DeadWall method."""
        return self.dead.dora()

    def ura(self):
        """Wrapper for respective DeadWall method."""
        return self.dead.ura()

    def take(self):
        """Wrapper for respective DeadWall method."""
        return self.dead.take()


class DeadWall:
    """DeadWall class; intended to be used as part of Wall class."""
    def __init__(self, tiles, main_wall):
        """tiles
    list of tiles for dead wall
main_wall
    reference to main Wall instance that created this DeadWall instance

"""
        self.wall = tiles
        self.doralv = 1
        self.main_wall = main_wall

    def __len__(self):
        """Returns number of tiles in wall."""
        return len(self.wall)

    def can_kan(self):
        """Returns True if kans may still be declared and False otherwise."""
        if self.doralv < 5:
            return True
        else:
            return False
            
    def dora(self):
        """Returns a list of dora indicator tiles."""
        return [self.wall[x] for x in range(self.kantiles, self.kantiles + 2 *
                                            self.doralv, 2)]

    def ura(self):
        """Returns a list of ura-dora indicator tiles."""
        return [self.wall[x + 1] for x in range(self.kantiles, self.kantiles + 2
                                                * self.doralv, 2)]

    def take(self):
        """Pops a tile for kan replacement, also taking replacement tile from
main wall and adding dora.  If no more replacement tiles, raises
ModelException(self, "five kan")."""
        if self.doralv < 5:
            self.doralv += 1
            self.wall.append(self.main_wall.rdraw())
            return self.wall.pop(0)
        else:
            raise ModelException(self, DeadWall, "five kan")


class Dice:
    """Two six-sided die."""
    def __init__(self):
        random.seed()
    def roll(self):
        """Returns 2d6"""
        return random.randint(1, 6) + random.randint(1, 6)


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
        self.wall = Wall()
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


        # Find all possible scores
        possible = mahjong.scoring.makesets(playeri.hand)
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

        scorelist = []
        for x in possible:
            y = playeri.sets[:]
            y.extend(x)
            scorelist.append(
                mahjong.scoring.score(
                    east, winds, *y, honba=self.honba, bonus=bonus,
                    dora=dora, ura=ura
                )
            )

        # Find highest score
        max = 0
        try:
            max_score = scorelist[max][0][0]
        except TypeError:
            max_score = scorelist[max][0]
        for i in range(1, len(scorelist)):
            try:
                current = scorelist[i][0][0]
            except TypeError:
                current = scorelist[i][0]
            if current > max_score:
                max = i
                max_score = current
        # Calculate array of point differences
        x, self.yaku = scorelist[max]
        diff = []
        try:
            for i in range(1,4):
                diff[i] = -x[0]
            diff[0] = -x[1]
            diff[player] = 0
            diff[player] = -sum(diff)
        except TypeError:
            for i in range(4):
                diff[i] = -x[0]
            diff[player] = 0
            diff[player] = -sum(diff)

        self.scores = diff

    def abort(self):
        self.scores = [0, 0, 0, 0]


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
    def __init__(self):
        """Calls Game.reset"""
        self.reset()

    def reset(self):
        """Reset round wind, dealer, honba, riichi pot, players"""
        self.round_wind = 0
        self.dealer = 0
        self.honba = 0
        self.riichi_pot = 0
        self.players = [ Player(x) for x in range(4) ]

    def cycle(self):
        """Cycles current dealer and each player's wind.  If it is again the
original east's turn, cycle round wind."""
        self.dealer += 1
        self.dealer %= 4
        for player in self.players:
            player.cycle_wind()
        if self.dealer == 0:
            self.wind += 1
            self.wind %= 4

    def start_hand(self):
        """Returns hand; creates hand instance if none exists."""
        if not has_hand:
            self.hand = Hand(self.round_wind, self.dealer, self.honba,
                             self.riichi_pot, self.players)
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
        del self.hand


class ModelException(Exception):
    def __init__(self, cls, val):
        """cls
    class
val
    value of exception

"""
        self.cls = cls
        self.val = val

    def __str__(self):
        return str(self.cls) + ":" + repr(self.val)


class RiichiException(ModelException):
    def __init__(self, no_points=0, already_declared=0):
        self.val = (no_points, already_declared)


class WallEmptyException(ModelException):
    def __init__(self):
        pass


class ModelEvent:
    def __init__(self):
        pass


