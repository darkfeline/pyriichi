#!/usr/bin/env python3

import pygame
import os

class View:
    def __init__(self):
        icon = pygame.image.load(os.path.join('images', 'tiles', '7z.gif'))
        pygame.display.set_icon(icon)
        self.display = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('PyRiichi')
        self.display.fill(pygame.Color('white'))

    def flip(self):
        pygame.display.flip()

    def opening(self):
        """Displays opening screen stuff."""
        pass


class BGBlitter:
    def __init__(self, display):
        self.display = display
        self.images = pygame.image.load(os.path.join('images', 'textures',
                                                     'felt.gif')),
        self.size = self.images[0].get_size()
        
    def blit(self):
        pass
       # for x in range(display.get_width() // 


class UIBlitter:
    pass


class TileBlitter:
    def __init__(self, display):
        self.display = display
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
    def __init__(self, display):
        pygame.font.init()
        self.font = pygame.font.Font(None, 17)
        self.display = display

    def blit(self, loc, txt):
        text = self.font.render(txt, True, (0, 0, 0), (255, 255, 255))
        rect = text.get_rect()
        rect.topleft = loc
        self.display.blit(text, rect)


