#!/usr/bin/env python3

from __future__ import division

import model.scoring

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
        """Declare riichi.  Raises RiichiError if riichi is already declared.
        
double
    include yaku for double riichi.  Defaults to False. 
    
"""
        if self.riichi:
            raise RiichiError("already declared")
        if self.points >= 1000:
            raise RiichiError("not enough points")
        self.points -= 1000
        self.riichi = 1
        self.ippatsu = 1
        if double:
            self.double_riichi = 1

    def sort(self):
        """Sort player's hand in place."""
        scoring.sort(self.hand)

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
            raise ModelError("Player", "chi", str(tiles))

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
            raise ModelError("Player", "pon ", str(tiles))

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
            raise ModelError("Player", "kan", str(tiles))

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
            raise ModelError("Player", "ckan", str(tiles))

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
        count = scoring.tocount(self.hand)
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
            count = scoring.tocount(self.hand)[start:start + 9]
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


class AI:
    def __init__(self, player):
        self.player = player

    def calc_hand(self):
        pass

    def calc_discard(self):
        pass

    def calc_meld(self, tile):
        pass


class Hypothesis:
    """Class that represents a hypothetical hand for AI."""
    def __init__(self, hand, targets, out):
        """hand
    list of tiles already in hand
targets
    list of hypothetical tiles to wait for.  Either/or tiles are kept in a
    sublist, e.g. if a hand needs either P3 or P6 for P3-5 or P4-6, then targets
    would contain [P3, P6] as an element.
out
    list of tiles already discarded or melded

"""
        self.hand = hand
        self.targets = targets

    def calc(self, out):
        """Returns a list of tuples, thus: (hypothetical hand, probability of
hand, number of waits, score).

out
    list of tiles already discarded or melded
    
"""
        final = self.gen_hands()
        for i, hand in enumerate(final):
            p = self.chance(hand, out)
            c = len(self.targets)
            s = model.scoring.score() # asdfasdf
            final[i] = [hand, p, c]
        return final

    def gen_hands(self):
        """Returns a list of final possible hands based on self.hand and
        self.targets."""
        final = []
        current = self.hand[:]
        count = 0
        self._rparse(final, current, count)
        return final

    def _rparse(self, final, current, count):
        """Recursive function for gen_hands()."""
        for x in self.targets[count:]:
            if isinstace(x, list):
                self._rparse(final, current, count)
                break
            else:
                current.append(x)
                count += 1

    def chance(self, final, out):
        """Returns the number of tiles left that can finish hand.
final
    ONE possible hand
out
    list of tiles discarded/melded

"""
        outcount = model.scoring.tocount(out)
        count = model.scoring.tocount(final)
        total = sum(outcount)
        current = 0
        for i in range(34):
            if count[i] > 0:
                x = 4 - outcount[i]
                if x < 1:
                    return 0
                current += x
            return current


class PlayerError(Exception):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return repr(self.val)


class RiichiError(PlayerError):
    pass


if __name__ == '__main__':
    pass
