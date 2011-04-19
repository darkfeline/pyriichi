#!/usr/bin/env python3

import random

import model.tiles

class Wall:
    def __init__(self):
        temp = []
        for suit in model.tiles.SUITS:
            for tile in suit:
                for i in range(4):
                    temp.append(tile())

        # swap in red fives
        red_done = [0, 0, 0]
        for i, x in enumerate(temp):
            if isinstance(x, model.tiles.P5) and not red_done[0]:
                temp[i] = model.tiles.P5R()
                red_done[0] = 1
            elif isinstance(x, model.tiles.S5) and not red_done[1]:
                temp[i] = model.tiles.S5R()
                red_done[1] = 1
            elif isinstance(x, model.tiles.M5) and not red_done[2]:
                temp[i] = model.tiles.M5R()
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
        """Total number of model.tiles in hand, including all four wall sections."""
        return sum([len(wall) for wall in self.walls])


    def draw(self):
        """Take next tile in wall (taking into consideration all four sections
and any breaks in wall.  If there are no more model.tiles in the wall, raise
WallEmptyError."""
        # in the beginning, if the dead wall was taken from the middle of a wall
        # section, may not draw from beginning of wall section
        if len(self) < 1:
            raise WallEmptyError()
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
        """Reverse draw, for replacing dead wall model.tiles."""
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
        # model.tiles are double-stacked
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
        """model.tiles
    list of model.tiles for dead wall
main_wall
    reference to main Wall instance that created this DeadWall instance

"""
        self.wall = model.tiles
        self.doralv = 1
        self.main_wall = main_wall

    def __len__(self):
        """Returns number of model.tiles in wall."""
        return len(self.wall)

    def can_kan(self):
        """Returns True if kans may still be declared and False otherwise."""
        if self.doralv < 5:
            return True
        else:
            return False
            
    def dora(self):
        """Returns a list of dora indicator model.tiles."""
        return [self.wall[x] for x in range(self.kanmodel.tiles, self.kanmodel.tiles + 2 *
                                            self.doralv, 2)]

    def ura(self):
        """Returns a list of ura-dora indicator model.tiles."""
        return [self.wall[x + 1] for x in range(self.kanmodel.tiles, self.kanmodel.tiles + 2
                                                * self.doralv, 2)]

    def take(self):
        """Pops a tile for kan replacement, also taking replacement tile from
main wall and adding dora.  If no more replacement model.tiles, raises
ModelError."""
        if self.doralv < 5:
            self.doralv += 1
            self.wall.append(self.main_wall.rdraw())
            return self.wall.pop(0)
        else:
            raise FiveKanError()


class WallError(Exception):
    pass


class WallEmptyError(WallError):
    pass


class FiveKanError(WallError):
    pass
