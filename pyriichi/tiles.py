#!/usr/bin/env python

"""Reference

0 P1
1 P2
2 P3
3 P4
4 P5
5 P6
6 P7
7 P8
8 P9
9 S1
10 S2
11 S3
12 S4
13 S5
14 S6
15 S7
16 S8
17 S9
18 M1
19 M2
20 M3
21 M4
22 M5
23 M6
24 M7
25 M8
26 M9
27 E
28 S
29 W
30 N
31 W
32 G
33 R

"""

class Tile:
    """Tile class.
    Universal attributes
        name
            Name of tile
        type
            suit i.e. "PINZU", "SOUZU", "MANZU", "WINDS", "DRAGONS"
        cmpval
            unique value for each tile, for sorting

        For numbered Tiles:
        value
            numeric value of tile

    Flags
        Flags are set to 1 arbitrarily or unset to denote attributes of tiles.

        Properties
            green
            terminal
            red

        Scoring
            chi
                Tile is part of declared chi
            pon
                Tile is part of declared pon
            kan
                Tile is part of open declared kan
            ckan
                Tile is part of concealed declared kan
            addedkan
                Tile is part of a declared pon that has been extended into a
                kan.  pon flags are unset (del tile.pon) and kan flags are set
                for ease of scoring.  
            last
                Last tile; winning tile.  In addition, has either the tag ron
                or tsumo
            ron
                used with last; win by discard
            tsumo
                used with last; win by self-pick

        Other
            hidden
                This flag is set when a player's discard has been claimed.
                Used to facilitate calculating furiten but allow view to
                display player discards accordingly.  

    """
    def __init__(self, name, type, cmpval):
        self.name = name
        self.type = type
        self.cmpval = cmpval

    def __str__(self):
        """Returns Tile.name"""
        return self.name

    def __repr__(self):
        return str(self) + '()'

    def __eq__(self, other):
        """Compares tiles with cmpval attribute."""
        if not isinstance(other, Tile):
            return NotImplemented
        if self.cmpval == other.cmpval:
            return True
        else:
            return False

    def __ne__(self, other):
        """Compares tiles with cmpval attribute."""
        if not isinstance(other, Tile):
            return NotImplemented
        if self.cmpval != other.cmpval:
            return True
        else:
            return False


class P1(Tile):
    def __init__(self):
        Tile.__init__(self, 'P1', 'PINZU', 0)
        self.terminal = 1
        self.value = 1


class P2(Tile):
    def __init__(self):
        Tile.__init__(self, 'P2', 'PINZU', 1)
        self.value = 2


class P3(Tile):
    def __init__(self):
        Tile.__init__(self, 'P3', 'PINZU', 2)
        self.value = 3


class P4(Tile):
    def __init__(self):
        Tile.__init__(self, 'P4', 'PINZU', 3)
        self.value = 4


class P5(Tile):
    def __init__(self):
        Tile.__init__(self, 'P5', 'PINZU', 4)
        self.value = 5

class P5R(P5):
    def __init__(self):
        P5.__init__(self)
        self.name += 'R'
        self.red = 1

class P6(Tile):
    def __init__(self):
        Tile.__init__(self, 'P6', 'PINZU', 5)
        self.value = 6


class P7(Tile):
    def __init__(self):
        Tile.__init__(self, 'P7', 'PINZU', 6)
        self.value = 7


class P8(Tile):
    def __init__(self):
        Tile.__init__(self, 'P8', 'PINZU', 7)
        self.value = 8


class P9(Tile):
    def __init__(self):
        Tile.__init__(self, 'P9', 'PINZU', 8)
        self.terminal = 1
        self.value = 9


class S1(Tile):
    def __init__(self):
        Tile.__init__(self, 'S1', 'SOUZU', 9)
        self.terminal = 1
        self.value = 1


class S2(Tile):
    def __init__(self):
        Tile.__init__(self, 'S2', 'SOUZU', 10)
        self.green = 1
        self.value = 2


class S3(Tile):
    def __init__(self):
        Tile.__init__(self, 'S3', 'SOUZU', 11)
        self.green = 1
        self.value = 3


class S4(Tile):
    def __init__(self):
        Tile.__init__(self, 'S4', 'SOUZU', 12)
        self.green = 1
        self.value = 4


class S5(Tile):
    def __init__(self):
        Tile.__init__(self, 'S5', 'SOUZU', 13)
        self.value = 5

class S5R(S5):
    def __init__(self):
        S5.__init__(self)
        self.name += 'R'
        self.red = 1

class S6(Tile):
    def __init__(self):
        Tile.__init__(self, 'S6', 'SOUZU', 14)
        self.green = 1
        self.value = 6


class S7(Tile):
    def __init__(self):
        Tile.__init__(self, 'S7', 'SOUZU', 15)
        self.value = 7


class S8(Tile):
    def __init__(self):
        Tile.__init__(self, 'S8', 'SOUZU', 16)
        self.green = 1
        self.value = 8


class S9(Tile):
    def __init__(self):
        Tile.__init__(self, 'S9', 'SOUZU', 17)
        self.terminal = 1
        self.value = 9


class M1(Tile):
    def __init__(self):
        Tile.__init__(self, 'M1', 'MANZU', 18)
        self.terminal = 1
        self.value = 1


class M2(Tile):
    def __init__(self):
        Tile.__init__(self, 'M2', 'MANZU', 19)
        self.value = 2


class M3(Tile):
    def __init__(self):
        Tile.__init__(self, 'M3', 'MANZU', 20)
        self.value = 3


class M4(Tile):
    def __init__(self):
        Tile.__init__(self, 'M4', 'MANZU', 21)
        self.value = 4


class M5(Tile):
    def __init__(self):
        Tile.__init__(self, 'M5', 'MANZU', 22)
        self.value = 5

class M5R(M5):
    def __init__(self):
        M5.__init__(self)
        self.name += 'R'
        self.red = 1

class M6(Tile):
    def __init__(self):
        Tile.__init__(self, 'M6', 'MANZU', 23)
        self.value = 6


class M7(Tile):
    def __init__(self):
        Tile.__init__(self, 'M7', 'MANZU', 24)
        self.value = 7


class M8(Tile):
    def __init__(self):
        Tile.__init__(self, 'M8', 'MANZU', 25)
        self.value = 8


class M9(Tile):
    def __init__(self):
        Tile.__init__(self, 'M9', 'MANZU', 26)
        self.terminal = 1
        self.value = 9


class E(Tile):
    def __init__(self):
        Tile.__init__(self, 'E', 'WINDS', 27)


class S(Tile):
    def __init__(self):
        Tile.__init__(self, 'S', 'WINDS', 28)


class W(Tile):
    def __init__(self):
        Tile.__init__(self, 'W', 'WINDS', 29)


class N(Tile):
    def __init__(self):
        Tile.__init__(self, 'N', 'WINDS', 30)


class Wh(Tile):
    def __init__(self):
        Tile.__init__(self, 'Wh', 'DRAGONS', 31)


class Gr(Tile):
    def __init__(self):
        Tile.__init__(self, 'Gr', 'DRAGONS', 32)
        self.green = 1


class Rd(Tile):
    def __init__(self):
        Tile.__init__(self, 'Rd', 'DRAGONS', 33)


PINZU = [P1, P2, P3, P4, P5, P6, P7, P8, P9]
SOUZU = [S1, S2, S3, S4, S5, S6, S7, S8, S9]
MANZU = [M1, M2, M3, M4, M5, M6, M7, M8, M9]
WINDS = [E, S, W, N]
DRAGONS = [Wh, Gr, Rd]
SUITS = [PINZU, SOUZU, MANZU, WINDS, DRAGONS]
