#!/usr/bin/env python3

import os
import pygame

class View:
    def __init__(self):
        icon = pygame.image.load(os.path.join('images', 'tiles', '7z.gif'))
        pygame.display.set_icon(icon)
        self.display = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('PyRiichi')
        self.display.fill(pygame.Color('white'))
        self.flip()

        self.bgblitter = BGBlitter()

    def flip(self):
        pygame.display.flip()

    def opening(self):
        """Displays opening screen stuff."""
        self.display.fill(pygame.Color('green'))
        self.flip()

    def grid(self):
        """Draws grid for easier placement of objects. 40x40"""
        w, h = self.display.get_size()
        for x in range(0, w, 40):
            pygame.draw.line(self.display, pygame.Color("red"), (x, 0), (x, h))
        for y in range(0, h, 40):
            pygame.draw.line(self.display, pygame.Color("red"), (y, 0), (y, w))


class BGBlitter:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.images = pygame.image.load(os.path.join('images', 'textures',
                                                     'felt.gif')),
        self.size = self.images[0].get_size()
        
    def blit(self):
        w, h = self.display.get_size()
        for x in range(0, w, 40):
            for y in range(0, h, 40):
                self.display.blit(self.images[0], (x, y))



class UIBlitter:
    pass


class TileBlitter:
    def __init__(self):
        self.display = pygame.display.get_surface()
        images = []
        for img in ['1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '1s',
                    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '1m', '2m',
                    '3m', '4m', '5m', '6m', '7m', '8m', '9m', '1z', '2z', '3z',
                    '4z', '5z', '6z', '7z', '0z']:
            images.append(pygame.image.load(os.path.join('images', 'tiles', img)
                                            + '.gif'))
        self.images = tuple(images)
        self.size = images[0].get_size()

    def blit(self, loc, tiles, angle=0):
        """Blit tiles at loc.
        
loc
    (x, y)
tiles
    [tiles]
angle=0
    degrees
    
"""
        w, h = self.size  # dimensions of images
        surface = pygame.Surface((w * len(tiles), h))
        for num, tile in enumerate(tiles):
            surface.blit(self.images[tile.cmpval], (w * num, 0))
        surface = pygame.transform.rotate(surface, angle)
        self.display.blit(surface, loc)

    def blitc(self, loc, num, angle=0):
        """Blit a number of concealed tile at a location."""
        tiles = []
        class tmp:
            def __init__(self):
                self.cmpval = 34
        for i in range(num):
            tiles.append(tmp)
        self.blit(loc, tiles, angle)


class TextBlitter:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 17)
        self.display = pygame.display.get_surface()

    def blit(self, loc, txt):
        text = self.font.render(txt, True, (0, 0, 0), (255, 255, 255))
        rect = text.get_rect()
        rect.topleft = loc
        self.display.blit(text, rect)


