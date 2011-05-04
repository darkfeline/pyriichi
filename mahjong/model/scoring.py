#!/usr/bin/env python

"""Hand Representations

sets
    tiles of hand split up into component parts, in lists
    e.g. chi chi pon pon pair

    A component part of a sets is a set.

hand
    all tiles in one list

count
    list with each element corresponding to the number of that tile in the
    hand.  Note that information about red tiles are lost.  

"""

from __future__ import division
import math

import model.tiles

def sort(hand):
    """Sort list of tiles in place."""
    hand.sort(key=lambda x: x.cmpval)

def tohand(*sets):
    """Converts hand representation from sets to hand.  Returns hand."""
    hand = []
    for set in sets:
        hand.extend(set)
    sort(hand)
    return hand

def tocount(hand):
    """Converts hand representation from hand to count.  Returns count."""
    count = [0 for i in range(34)]
    for tile in hand:
        count[tile.cmpval] += 1
    return count

def makesets(hand):
    """Make sets representations from hand.  Returns a list of lists of tiles.  """
    sort(hand)
    possible = []
    
    if is7pairs(hand):
        x = []
        for i in range(7):
            a, b = i * 2, i * 2 + 1
            if not ispair(hand[a], hand[b]):
                raise ScoringException("makesets", "not a pair:" + str(hand[a])
                                       + str(hand[b]))
            x.append([a, b])
        possible.append(x)

    _rmakesets(hand, [], possible)
    return possible

def _rmakesets(hand, used, possible):
    """Recursive part of makesets()."""
    if len(hand) < 1:
        possible.append(used[:])
        return

    sort(hand)
    if has_kan(hand, hand[0]):
        used.append(hand[:4])
        hand = hand[4:]
        _rmakesets(hand, used, possible)
        hand.extend(used.pop())

    sort(hand)
    if has_pon(hand, hand[0]):
        used.append(hand[:3])
        hand = hand[3:]
        _rmakesets(hand, used, possible)
        hand.extend(used.pop())

    sort(hand)
    if has_chi(hand, hand[0]):
        used.append(hand[:3])
        hand = hand[3:]
        _rmakesets(hand, used, possible)
        hand.extend(used.pop())

    sort(hand)
    if ispair(hand):
        used.append(hand[:2])
        hand = hand[2:]
        _rmakesets(hand, used, possible)
        hand.extend(used.pop())

def has_pon(hand, tile):
    """Returns True if the tile can form a pon in the hand and False
    otherwise."""
    count = 0
    for x in self.hand:
        if x.cmpval == tile.cmpval:
            count += 1
        if count == 3:
            return True
    return False

def has_kan(hand, tile):
    """Returns True if the tile can form a kan in the hand and False
    otherwise."""
    count = 0
    for x in self.hand:
        if x.cmpval == tile.cmpval:
            count += 1
        if count == 4:
            return True
    return False

def has_chi(hand, tile):
    """Returns a tuple of the values of the tiles of the chi if the tile can
    form a chi in the hand and False otherwise."""
    try:
        tile.value
    except AttributeError:
        return False
    else:
        val = tile.value
        start = ["PINZU", "SOUZU", "MANZU"].index(tile.type) * 9
        count = tocount(self.hand)[start:start + 9]
        count[val - 1] += 1

        x = 0
        a, b = val - 2, val + 2
        if a < 0:
            a = 0
        elif b > 9:
            b = 9
        for i in range(a, b + 1):
            if count[i] > 0:
                x += 1
                if x == 3:
                    return (i - 2, i - 1, i)
            else:
                x = 0
        return False

def calc(fu, han, east, type, honba=0):
    """Calculates score from fu, han, taking into account who won and what type
of win.  For tsumo non-east, returns a tuple where the first item is score for
non-East, and the second item is score for East.

Formula
    fu is rounded up to the nearest 10.  The base score is fu * 2 ** (2 + han),
    which is divided into 4 or 2:1:1 or 2:2:2 depending on the type of win.
    Each portion is then rounded up to the nearest 100.  Honba points are then
    added.

east
    1 if East wins, 0 otherwise
type
    type of win, i.e. ron, tsumo
honba
    number of repeat counters

"""
    score = 0
    # double yakuman
    if han >= 26:
        score = 16000
    # yakuman
    elif han >= 13:
        score = 12000
    # sanbaiman
    elif han >= 11:
        score = 6000
    # baiman
    elif han >= 8:
        score = 4000
    # haneman
    elif han >= 6:
        score = 3000
    # mangan
    elif han >= 5:
        score = 2000
    else:
        # round fu to ceiling 10
        if fu != 25 and fu % 10 != 0:
            fu = math.ceil(fu / 10) * 10
        # Calculate base score
        score = fu * 2 ** (2 + han)

    def round(x):
        return int(math.ceil(x / 100) * 100)

    if type == "ron":
        if east:
            score *= 6
        else:
            score *= 4
        score = round(score)
        score += honba * 300
        return score
    elif type == "tsumo":
        if east:
            score *= 2
            score = round(score)
            score += honba * 100
            return score
        else:
            score = (round(score) + (honba * 100), round(score * 2) + (honba *
                                                                       100))
            return score
    else:
        raise ScoringException("calc", type + " is not a valid value for type")

def matchtype(hand, *types, any=0):
    """Checks if all tiles in hand matches one type of the types provided.  If
there's a match, returns matched type, else returns nothing.  types are
strings.  If any is set to 1, matchtype will attempt to match any type e.g.
matchtype(hand, 'a', 'b', any=1) will match a hand with tiles of only 'a' and
'b' types, as opposed to matchtype(hand, 'a', 'b', any=0), which matches a hand
of all 'a' or all 'b' only."""
    if any:
        count = 0
        for type in [x.type for x in hand]:
            if type in types:
                count += 1
        if count == len(hand):
            return types
    for type in types:
        if [x.type for x in hand].count(type) == len(hand):
            return type
    return

def concealed(*sets):
    """Returns True if all sets are concealed, False otherwise. If there's
only one set, takes into account the last tile."""
    if len(sets) == 1:
        for tile in sets[0]:
            try:
                tile.last
                tile.ron
            except AttributeError:
                pass
            else:
                return False
    else:
        for set in sets:
            for tile in set:
                try:
                    tile.kan
                except AttributeError:
                    pass
                else:
                    return False
                try:
                    tile.pon
                except AttributeError:
                    pass
                else:
                    return False
                try:
                    tile.chi
                except AttributeError:
                    pass
                else:
                    return False
    return True

def counttile(list, tile):
    """Returns number of a tile in list."""
    num = 0
    for x in list:
        if tile.cmpval == x.cmpval:
            num += 1
    return num

def nexttile(tile):
    """Returns the tile that comes after tile.  Used for dora."""
    for suit in tiles.SUITS:
        for i, x in enumerate(suit):
            if isinstance(tile, x):
                i += 1
                if i >= len(suit):
                    i = 0
                return suit[i]()

def is13orphan(hand):
    """Checks hand for 13 Orphans."""
    count = []
    for x in [tiles.P1, tiles.P9, tiles.S1, tiles.S9, tiles.M1, tiles.M9,
              tiles.E, tiles.S, tiles.W, tiles.N, tiles.Wh, tiles.G, tiles.R]:
        count.append(counttile(hand, x()))
    if count.count(2) == 1 and count.count(1) == 13:
        return True
    else:
        return False

def is7pairs(hand):
    """Checks hand for 7 Pairs."""
    count = []
    for suit in tiles.SUITS:
        for x in suit:
            count.append(counttile(hand, x()))
    if count.count(2) == 7:
        return True
    else:
        return False

def isnagashi(discards):
    """Checks if all discards are honors."""
    for tile in discards:
        try:
            tile.value
        except AttributeError:
            if not tile.cmpval > 26:
                return False
    return True

def iscomplete(hand):
    """Checks hand recursively for completeness. Wrapper for recursive
function.

hand
    list of tiles in hand representation
    
"""
    # assemble hand as list representation
    if total == 14:
        if is13orphan(hand):
            return True
        if is7pairs(hand):
            return True
    return _riscomplete(tocount(hand), [0 for i in range(34)])

def _riscomplete(hand, store):
    """Recursive function to check for hand completeness.  

hand
    list of tiles in count representation currently being checked
store
    list of tiles in count representation currently taken out

"""
    total = sum(hand)
    # is a pair
    if total == 2:
        if hand.count(2) == 1:
            return True
        else:
            return False
    # look for kan
    for i, num in enumerate(hand):
        if num == 4:
            hand[i] = 0
            store[i] = 4
            if _riscomplete(hand, store):
                return True
            store[i] = 0
            hand[i] = 4

    # pon
    for i, num in enumerate(hand):
        if num >= 3:
            hand[i] -= 3
            store[i] += 3
            if _riscomplete(hand, store):
                return True
            store[i] -= 3
            hand[i] += 3
    # chi
    for i, num in enumerate(hand[:26]):
        if i % 9 <= 7:
            if hand[i] >= 1 and hand[i + 1] >= 1 and hand[i + 2] >= 1:
                hand[i] -= 1
                hand[i + 1] -= 1
                hand[i + 2] -= 1
                store[i] += 1
                store[i + 1] += 1
                store[i + 2] += 1
                if _riscomplete(hand, store):
                    return True
                store[i] -= 1
                store[i + 1] -= 1
                store[i + 2] -= 1
                hand[i] += 1
                hand[i + 1] += 1
                hand[i + 2] += 1
    return False

def ischi(set):
    """Tests if the given list of tiles form a chi.  If it does, returns the
lowest tile, else returns nothing."""
    if len(set) == 3:
        if matchtype(set, 'PINZU', 'SOUZU', 'MANZU'):
            sort(set)
            if set[0].value + 2 == set[1].value + 1 == set[2].value:
                return set[0]
    return

def ispon(set):
    """Tests if the given list of tiles form a pon.  If it does, returns the
tile, else returns nothing."""
    if len(set) == 3:
        temp = [tile.cmpval for tile in set]
        if temp.count(temp[0]) == 3:
            return set[0]
    return

def iskan(set):
    """Tests if the given list of tiles form a kan.  If it does, returns the
tile, else returns nothing."""
    if len(set) == 4:
        temp = [tile.cmpval for tile in set]
        if temp.count(temp[0]) == 4:
            return set[0]
    return

def ispair(set):
    """Tests of the given list of tiles form a pair.  If it does, returns the
tile, else returns nothing."""
    if len(set) == 2 and set[0].cmpval == set[1].cmpval:
        return set[0]
    else:
        return

def waits(hand):
    """Finds the waits of the list of tiles provided, in hand format.  Waits are
returned as a list of CLASS OBJECTS, NOT INSTANCES.  If no waits, returns an
empty list."""
    waits = []
    for suit in SUITS:
        for tile in suit:
            temp = hand[:]
            temp.append(tile())
            sort(temp)
            if iscomplete(temp):
                waits.append(tile)
    return waits

def score(east, winds, *sets, honba=0, bonus=[], dora=[], ura=[]):
    """Returns (score, yaku), where score is the score and yaku is the list of
yaku matched, in all lower case, in Japanese.  For tsumo non-East, returns a
tuple where the first item is score for non-East, and the second item is score
for East.

Assumes hand is complete and separated correctly.  Seven Pairs must be passed as
seven lists.  

Special wins han, such as Blessings and Nagashi Mangan, should be added to bonus
and will be handled appropriately .  Haitei, Robbbing a Kong, Rinchan Kaihou,
Riichi, Ippatsu, Double Riichi should be added to bonus.  Dora indicator tiles
should be added to dora and ura-dora to ura.

east 
    1 if East wins, 0 otherwise
winds
    Round and player winds.  If East round Dealer, use ['E', 'E']
sets
    lists of tile parts of hand.
honba
    number of repeat counters
bonus
    other yaku; list in lower case in Japanese
    possible yaku: 
        nagashi mangan
        tenhou
        chihou
        renhou
        riichi
        ippatsu
        daburu riichi
        rinchan kaihou
        chan kan
        haitei
dora
    list of dora indicators
ura
    list of ura-dora indicators
    
""" 
    # Nagashi Mangan
    if 'nagashi mangan' in bonus:
        return calc(20, 5, east, 'tsumo', honba), ['nagashi mangan']

    type = ''
    for tile in tohand(*sets):
        try:
            tile.ron
        except AttributeError:
            pass
        else:
            type = 'ron'
            break
        try:
            tile.tsumo
        except AttributeError:
            pass
        else:
            type = 'tsumo'
            break

    # Blessing of Heaven/Earth/Man
    if 'tenhou' in bonus:
        return calc(20, 13, east, type, honba), ['tenhou']
    elif 'chihou' in bonus:
        return calc(20, 13, east, type, honba), ['chihou']
    elif 'renhou' in bonus:
        return calc(20, 13, east, type, honba), ['renhou']

    # Big Four Winds
    count = 0
    for x in sets:
        if len(x) >=3 and matchtype(x, 'WINDS'):
            count += 1
    if count == 4:
        return calc(20, 26, east, type, honba), ['dai suushii']

    # Little Four Winds
    count = 0
    pair = 0
    for x in sets:
        if matchtype(x, "WINDS"):
            if len(x) >= 3:
                count += 1
            elif len(x) == 2:
                pair += 1
    if count == 3 and pair == 1:
        return calc(20, 13, east, type, honba), ['shou suushii']

    # Big Three Dragons
    count = 0
    for x in sets:
        if len(x) >= 3 and matchtype(x, 'DRAGONS'):
            count += 1
    if count == 3:
        return calc(20, 13, east, type, honba), ['dai sangen']

    # All Honors
    count = 0
    for x in sets:
        if matchtype(x, "WINDS", "DRAGONS"):
            count += 1
    if count == 5:
        return calc(20, 13, east, type, honba), ['tsuu iisou']

    # All Terminals
    try:
        for set in sets:
            # If this raises AttributeError, then not all terminals
            types = [tile.terminal for tile in set]
    except AttributeError:
        pass
    else:
        return calc(20, 13, east, type, honba), ['chinrouto']

    # All Green
    try:
        for set in sets:
            types = [tile.green for tile in set]
    except AttributeError:
        pass
    else:
        return calc(20, 13, east, type, honba), ['ryuu iisou']

    # Four Kongs
    count = 0
    for x in sets:
        if len(x) == 4:
            count += 1
    if count == 4:
        return calc(20, 13, east, type, honba), ['suu kan tsu']

    # Four Concealed Pungs
    han = 13
    count = 0
    if concealed(*sets):
        for set in sets:
            if (counttile(set, set[0]) == len(set) and len(set) >= 3 and
            concealed(set)):
                count += 1
                # win on pair
                if len(set) == 2:
                    try:
                        set[0].last
                    except AttributeError:
                        pass
                    else:
                        han += 13
                    try:
                        set[1].last
                    except AttributeError:
                        pass
                    else:
                        han += 13
    if count == 4:
        return calc(20, han, east, type, honba), ['suu ankou']

    # Nine Gates
    han = 0
    temp = tohand(*sets)
    i = 0
    while i < len(temp):
        if temp[i].type in ['DRAGONS', 'WINDS']:
            temp.pop(i)
        else:
            i += 1
    values = [tile.value for tile in temp]
    if (matchtype(tohand(*sets), "PINZU", "SOUZU", "MANZU") and 
    values.count(1) >= 3 and 
    values.count(2) >= 1 and
    values.count(3) >= 1 and
    values.count(4) >= 1 and
    values.count(5) >= 1 and
    values.count(6) >= 1 and
    values.count(7) >= 1 and
    values.count(8) >= 1 and
    values.count(9) >= 3):
        han += 13
        for i, tile in enumerate(tohand(*sets)):
            try:
                tile.last
            except AttributeError:
                pass
            else:
                values.pop(i)
                break
        if (values.count(1) == 3 and values.count(2) == 1 and 
            values.count(3) == 1 and values.count(4) == 1 and 
            values.count(5) == 1 and values.count(6) == 1 and 
            values.count(7) == 1 and values.count(8) == 1 and 
            values.count(9) == 3):
            han += 13
    if han > 0:
        return calc(20, han, east, type, honba), ['chuuren pooto']

    # Thirteen Orphans
    han = 0
    hand = tohand(*sets)
    if is13orphan(hand):
        han += 13
        for tile in hand:
            try:
                tile.last
            except AttributeError:
                pass
            else:
                hand.remove(tile)
                count = []
                for x in [tiles.P1, tiles.P9, tiles.S1, tiles.S9, tiles.M1,
                          tiles.M9, tiles.E, tiles.S, tiles.W, tiles.N,
                          tiles.Wh, tiles.G, tiles.R]:
                    count.append(counttile(hand, x()))
                if count.count(1) == 13:
                    han += 13
                break
    if han > 0:
        return calc(20, han, east, type, honba), ['kokushi musou']

    # Regular Hand Scoring ###################################################
    fu = han = 0
    yaku = []
    for x in bonus:
        if x == 'riichi':
            han += 1
            yaku.append(x)
        elif x == 'ippatsu':
            han += 1
            yaku.append(x)
        elif x == 'daburu riichi':
            han += 1
            yaku.append(x)
        elif x == 'rinchan kaihou':
            han += 1
            yaku.append(x)
        elif x == 'chan kan':
            han += 1
            yaku.append(x)
        elif x == 'haitei':
            han += 1
            yaku.append(x)
    # Full Flush
    if matchtype(tohand(*sets), "PINZU", "SOUZU", "MANZU"):
        han += 5
        yaku.append('chinitsu')
        if concealed(*sets):
            han += 1

    # Twice Pure Double Chi
    # This is counted in Pure Double Chi.  If there are two Pure Double Chi, an
    # extra han is added for a total of 3 han.

    # Terminals in All Sets
    count = 0
    switch = False  # don't want this for all terminal hands
    for set in sets:
        for tile in set:
            try:
                tile.terminal
                count += 1
                if not switch and ischi(set):
                    switch = True
                break
            except AttributeError:
                pass
    if count == 4 and switch:
        han += 2
        yaku.append('junchan taiyai')
        if concealed(*sets):
            han += 1

    # All Terminals and Honors
    count = 0
    for tile in tohand(*sets):
        try:
            if tile.type in ['DRAGONS', 'WINDS'] or tile.terminal:
                count += 1
        except AttributeError:
            break
    if count == 14:
        han += 2
        yaku.append('honroutou')

    # Little Three Dragons
    temp = tocount(tohand(*sets))[31:33]
    try:
        temp.remove(2)
    except ValueError:
        pass
    else:
        if temp[0] >= 3 and temp[1] >= 3:
            han += 2
            yaku.append('shou sangen')

    # Half Flush
    temp = tohand(*sets)
    i = 0
    while i < len(temp):
        if temp[i].type in ['WINDS', 'DRAGONS']:
            temp.pop(i)
        else:
            i += 1
    if matchtype(temp, temp[0].type):
        han += 2
        yaku.append('honitsu')

    # All Pungs
    temp = tocount(tohand(*sets))
    if temp.count(3) + temp.count(4) == 4:
        han += 2
        yaku.append('toitoi hou')

    # Three Kongs
    if tocount(tohand(*sets)).count(4) == 3:
        han += 2
        yaku.append('san kan tsu')
    
    # Three Concealed Pungs
    count = 0
    for set in sets:
        if concealed(*sets) and ispon(set) or iskan(set):
            count += 1
    if count >= 3:
        han += 2
        yaku.append('san ankou')

    # Triple Pung
    temp = []
    # Isolate only numbered tiles
    for set in sets:
        if ispon(set) or iskan(set) and set[0] not in ["DRAGONS", "WINDS"]:
            temp.append(set[0])
    if len(temp) >= 3:
        key = 0
        types = [tile.type for tile in temp]
        for tile in temp:
            if types.count(tile.type) == 1:
                key = tile.value
                break
        count = []
        for tile in temp:
            if ("PINZU" not in count and tile.value == key and 
                tile.type == "PINZU"):
                count.append("PINZU")
            if ("SOUZU" not in count and tile.value == key and 
                tile.type == "SOUZU"):
                count.append("SOUZU")
            if ("MANZU" not in count and tile.value == key and 
                tile.type == "MANZU"):
                count.append("MANZU")
        if 'PINZU' in count and 'SOUZU' in count and 'MANZU' in count:
            han += 2
            yaku.append('san shoku dokuu')

    # Seven Pairs
    if concealed(*sets) and is7pairs(tohand(*sets)):
        han += 2
        fu = 25
        yaku.append('chii toitsu')

    # Outside Hand
    count = 0
    switch = False
    for set in sets:
        key = 0
        if ischi(set):
            key = ischi(set)
            if not switch:
                switch = True
            if key.value in [1, 7]:
                count += 1
                break
        elif ispon(set):
            key = ispon(set)
        elif iskan(set):
            key = iskan(set)
        elif ispair(set):
            key = ispair(set)
        try:
            if key and key.type in ["DRAGONS", "WINDS"] or key.value in [1, 9]:
                count += 1
        except AttributeError:
            pass
    if count == len(sets):
        han += 1
        yaku.append('chanta')
        if concealed(*sets):
            han += 1

    # Fanpai
    for set in sets:
        if ispon(set) or iskan(set):
            if set[0].type == "DRAGONS":
                han += 1
                yaku.append('fanpai')
            if set[0].type == winds[0]:
                han += 1
                yaku.append('fanpai')
            if set[0].type == winds[1]:
                han += 1
                yaku.append('fanpai')

    # Pure Straight
    temp = []
    for set in sets:
        tile = ischi(set)
        if tile:
            temp.append(tile)
    if len(temp) >= 3:
        for suit in ['PINZU', 'SOUZU', 'MANZU']:
            if [tile.type for tile in temp].count(suit) >= 3:
                x = [tile.value for tile in temp]
                if (x.count(1) >= 1 and 
                    x.count(4) >= 1 and 
                    x.count(7) >= 1):
                    han += 1
                    yaku.append('itsu')
                    if concealed(*sets):
                        han += 1

    # Mixed Triple Chi
    count = [0, 0, 0]
    temp = []
    key = 0
    for set in sets:
        tile = ischi(set)
        if tile:
            temp.append(tile)
    if len(temp) >= 3:
        for tile in temp:
            if [x.type for x in temp].count(tile.type) == 1:
                key = tile.value
    if key != 0:
        for i, suit in enumerate(['PINZU', 'SOUZU', 'MANZU']):
            for tile in temp:
                if tile.type == suit and tile.value == key:
                    count[i] = 1
                    break
    if count.count(1) == 3:
        han += 1
        yaku.append('san shoku doujun')
        if concealed(*sets):
            han += 1

    # Pure Double Chi
    if concealed(*sets):
        temp = []
        count = 0
        for set in sets:
            key = ischi(set)
            if key:
                if key.cmpval not in temp:
                    temp.append(key.cmpval)
                else:
                    temp.remove(key.cmpval)
                    count += 1
        if count == 1:
            han += 1
            yaku.append('iipeikou')
        elif count == 2:
            han += 3
            yaku.append('ryan peikou')

    # Pinfu
    if concealed(*sets):
        count = 0
        for set in sets:
            sort(set)
            if ischi(set):
                try:
                    set[0].last
                except AttributeError:
                    pass
                else:
                    count += 1
                    continue
                try:
                    set[2].last
                except AttributeError:
                    pass
                else:
                    count += 1
                    continue
            elif ispair(set):
                # If pair is concealed, then it can't be single wait
                if concealed(*sets):
                    count += 1
        if count == 5:
            han += 1
            yaku.append('pinfu')

    # Tanyao
    # tanyao will be allowed for open hands
    switch = 0
    for tile in tohand(*sets):
        if tile.type in ['DRAGONS', 'WINDS']:
            switch = 1
            break
        try:
            tile.terminal
        except AttributeError:
            pass
        else:
            switch = 1
            break
    if not switch:
        han += 1
        yaku.append('tanyao chuu')

    # Menzen Tsumo
    if concealed(*sets) and type == 'tsumo':
        han += 1 
        yaku.append('menzen tsumo')

    # There needs to be at least one han
    if han < 1:
        raise ScoringException("score", "han is less than one: " + han)

    # Calculate fu
    # Don't do this for seven pairs
    if fu != 25:
        # Calculate fu for win
        if concealed(*sets) and type == 'ron':
            fu += 30
        else:
            fu += 20
        # Calculate fu for sets
        for set in sets:
            base = 0
            if ispon(set):
                base = 2
                tile = ispon(set)
            elif iskan(set):
                base = 8
                tile = iskan(set)
            if base != 0:
                if concealed(*sets):
                    base *= 2
                if tile.type in ['DRAGONS', 'WINDS']:
                    base *= 2
                try:
                    tile.terminal
                except AttributeError:
                    pass
                else:
                    base *= 2
                fu += base
                # Calculate fu for pair
                tile = ispair(set)
                if tile:
                    if tile.type == 'DRAGONS' or tile.type in winds:
                        fu += 2
        # fu for tsumo
        if type == 'tsumo' and 'pinfu' not in yaku:
            fu += 2
        # open pinfu
        if not concealed(*sets) and fu == 20:
            fu += 2
        # single waits
        for set in sets:
            sort(set)
            if ischi(set):
                try:
                    set[0].last
                except AttributeError:
                    pass
                else:
                    fu += 2
                    break
                try:
                    set[2].last
                except AttributeError:
                    pass
                else:
                    fu += 2
                    break
            else:
                # If pair, pon, kan is not concealed, then it's single wait
                if not concealed(set):
                    fu += 2
                    break

    # Dora, Ura Dora
    if len(dora) > 0:
        for tile in dora:
            count = counttile(tohand(*sets), nexttile(tile))
            han += count
            yaku.extend(['dora' for i in range(count)])
    if len(ura) > 0 and 'riichi' in yaku:
        for tile in ura:
            count = counttile(tohand(*sets), nexttile(tile))
            han += count
            yaku.extend(['ura dora' for i in range(count)])

    return calc(fu, han, east, type, honba), yaku


def highest_score(east, winds, hand, sets, honba=0, bonus=[], dora=[], ura=[]):
    """Returns the highest score from score().

east 
    1 if East wins, 0 otherwise
winds
    Round and player winds.  If East round Dealer, use ['E', 'E']
hand
    list of tiles; player's hand
sets
    list of player's melds
honba
    number of repeat counters
bonus
    other yaku; list in lower case in Japanese
    possible yaku: 
        nagashi mangan
        tenhou
        chihou
        renhou
        riichi
        ippatsu
        daburu riichi
        rinchan kaihou
        chan kan
        haitei
dora
    list of dora indicators
ura
    list of ura-dora indicators
    
""" 
    possible = makesets(hand)
    # Find all possible scores
    scorelist = []
    for x in possible:
        y = sets[:]
        y.extend(x)
        scorelist.append(
            scoring.score(
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

    return scorelist[max]


class ScoringException(Exception):
    def __init__(self, func, val):
        self.func = func
        self.val = val
    def __str__(self):
        return func + ":" + repr(self.val)

if __name__ == '__main__':
    from model.tiles import *

    # 2000/4000, menzen tsumo, itsu, dora, dora
    print('2000/4000, menzen tsumo, itsu, dora, dora')
    a = [M1(), M2(), M3()]
    b = [M4(), M5(), M6()]
    c = [M7(), M8(), M9()]
    d = [P1(), P1(), P1()]
    d[2].last = 1
    d[2].tsumo = 1
    e = [S6(), S6()]
    s, y = score(0, ['S', 'E'], a, b, c, d, e, dora=[S5()], ura=[P7()])
    print(s)
    print(y)

    # 2900, fanpai, dora
    print('2900, fanpai, dora')
    a = [M4(), M5(), M6()]
    b = [P7(), P8(), P9()]
    c = [Rd(), Rd(), Rd()]
    for tile in c:
        tile.pon = 1
    d = [S6(), S7(), S8()]
    d[1].last = 1
    d[1].ron = 1
    e = [S1(), S1()]
    s, y = score(1, ['E', 'E'], a, b, c, d, e, dora=[S7()], ura=[S9()])
    print(s)
    print(y)
     
    # 2400, chi toitsu
    print('2400, chi toitsu')
    a = [S1(), S1()]
    b = [S2(), S2()]
    c = [S7(), S7()]
    c[1].last = 1
    c[1].ron = 1
    d = [M2(), M2()]
    e = [M3(), M3()]
    f = [P7(), P7()]
    g = [Rd(), Rd()]
    s, y = score(1, ['E', 'E'], a, b, c, d, e, f, g, dora=[S8()])
    print(s)
    print(y)

    # 1300, tanyao
    print('1300, tanyao')
    a = [S2(), S3(), S4()]
    b = [M2(), M3(), M4()]
    c = [M5(), M6(), M7()]
    d = [P6(), P7(), P8()]
    e = [M8(), M8()]
    e[0].last = 1
    e[0].ron = 1
    s, y = score(0, ['W', 'E'], a, b, c, d, e)
    print(s)
    print(y)
