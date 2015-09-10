#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: gt_annotate.py <img>

Options:
    -h --help  Show this message
"""

import pygame
import cPickle as pickle

from mscr.util import AddSuffix
from docopt import docopt


class Annotate():
    COLOR = ((0, 0, 255), (255, 0, 0))
    WIDTH = 5
    CLS = ['txt', 'ms']

    def __init__(self, imgf):
        self._imgf = imgf
        self._img = pygame.image.load(imgf)
        self._clean = self._img.copy()
        self.__init_screen(self._img)
        self._ann = []

    def __init_screen(self, img):
        pygame.init()
        self._size = img.get_size()
        self._screen = pygame.display.set_mode(self._size)
        self._screen.blit(self._img, (0, 0))

    def run(self):
        p1, rect = [], []
        i, draw_on = 0,  False
        try:
            while True:
                e = pygame.event.wait()
                if e.type == pygame.QUIT:
                    raise StopIteration

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_0:
                        i = 0
                    if e.key == pygame.K_1:
                        i = 1
                    if e.key == pygame.K_c:
                        self._img = self._clean.copy()
                        self._screen.blit(self._clean, (0, 0))
                        self._ann = []
                    if e.key == pygame.K_s:
                        print self._ann
                        outfile = AddSuffix('gt', 'pck').run(self._imgf)
                        pickle.dump(self._ann, open(outfile, 'w'))
                        raise StopIteration

                if e.type == pygame.MOUSEBUTTONDOWN:
                    p1 = e.pos
                    pygame.draw.circle(self._screen, self.COLOR[i], p1,
                                       self.WIDTH)
                    draw_on = True

                if e.type == pygame.MOUSEBUTTONUP:
                    draw_on = False
                    self._img = pygame.display.get_surface().copy()
                    p1 = rect[0], rect[1]
                    p2 = rect[0] + rect[2], rect[1] + rect[3]
                    self._ann.append([self.CLS[i], [p1, p2]])

                if e.type == pygame.MOUSEMOTION:
                    if draw_on:
                        x1, y1 = p1
                        x2, y2 = e.pos[0], e.pos[1]
                        rect = (x1, y1, x2-x1, y2-y1)
                        self._screen.blit(self._img, (0, 0))
                        pygame.draw.rect(self._screen, self.COLOR[i], rect,
                                         self.WIDTH)

                pygame.display.flip()

        except StopIteration:
            pass

        pygame.quit()

    def show(self, ann=None):
        self.__init_screen(self._clean)
        ann = ann if ann else self._ann
        for cls, rect in ann:
            i = self.CLS.index(cls)
            if rect:
                pygame.draw.rect(self._screen, self.COLOR[i], rect,
                                 self.WIDTH)
        while True:
            pygame.display.flip()
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                pygame.quit()


if __name__ == '__main__':
    args = docopt(__doc__)
    ann = Annotate(args['<img>'])
    ann.run()
