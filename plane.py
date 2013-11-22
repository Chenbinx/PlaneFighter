# -*- coding: utf-8 -*-
# Filename: plane.py
# Author:   Chenbin
# Time-stamp: <2013-11-18 Mon 19:37:04>

import pygame
import os
import sys
import xml.etree.ElementTree as ET
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((480, 800), 0, 32)

def load_image(name, alpha=False):
    path = os.path.join(os.path.abspath('assets'), name)
    if alpha:
        return pygame.image.load(path).convert_alpha()
    else:
        return pygame.image.load(path).convert()

class atlas:
    atlas = {}

    def __init__(self, filename):
        self.surface = load_image(filename, alpha=True)
        xml = filename.split('.')[0] + '.xml'
        path = os.path.join(os.path.abspath('assets'), xml)
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            self.atlas[child.attrib['name']] = child.attrib

    def get_sprite(self, name):
        if name not in self.atlas:
            print 'Error, no spirite in cache'
            sys.exit(0)
        info = self.atlas[name]
        position = (int(info['x']), int(info['y']))
        rect = (int(info['width']), int(info['height']))
        return self.surface.subsurface(position, rect)



atlas = atlas('plane.png')

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Bullet(GameObject):
    images = []
    def __init__(self, screen, name=''):
        super(Bullet, self).__init__()
        self.images.append(atlas.get_sprite('bullet_0'))
        self.images.append(atlas.get_sprite('bullet_1'))

class FriendBullet(Bullet):
    speed = 100
    position = [0, 0]

    def __init__(self, screen, postion=(0, 0)):
        super(FriendBullet, self).__init__(screen)
        self.image = self.images[0]
        self.postion = postion
        self.screen = screen

    def update(self, ticks):
        d = self.speed * ticks
        self.position[1] -= d
        if self.position[1] > 0:
            self.screen.blit(self.image, self.position)

class Enemy(GameObject):
    type = ['enemy_s', 'enemy_m', 'enemy_b']

    def __init__(self, enemy_type):
        self.image = atlas.get_sprite(self.type[enemy_type])

class Plane(GameObject):
    number = 2                  # animations
    rate   = 5                  # fps
    images = []
    passed_time = 0.0
    def __init__(self, screen):
        super(Plane, self).__init__()
        self.images.append(atlas.get_sprite('hero_1'))
        self.images.append(atlas.get_sprite('hero_2'))
        self.image = self.images[0]
        self.rect = (100, 100)
        self.screen = screen

    def update(self, ticks, fired, postion=(0, 0)):
        self.passed_time += ticks
        self.order = (int)(self.passed_time * self.rate) % self.number
        if self.order == 0 and self.passed_time > self.rate:
            self.passed_time = 0
        self.image = self.images[self.order]
        self.screen.blit(self.image, postion)


class Background():
    images = []
    speed  = 100
    posy   = [-800.0, 0.0]
    def __init__(self, screen):
        self.images.append(load_image('bg_01.jpg'))
        self.images.append(load_image('bg_02.jpg'))

    def update(self, ticks):
        d = self.speed * ticks
        self.posy[0] += d
        self.posy[1] += d
        
        if self.posy[0] > 800:
            self.posy[0] = -800.0
        if self.posy[1] > 800:
            self.posy[1] = -800.0

        screen.blit(self.images[0], (0, self.posy[0]))
        screen.blit(self.images[1], (0, self.posy[1]))


p = Plane(screen)
bg = Background(screen)
clock = pygame.time.Clock()

es = Enemy(0)
em = Enemy(1)
eb = Enemy(2)

pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # screen.blit(bg, (0, 0))
    
    # screen.blit(p.image, (10, 10))
    ticks = clock.tick(60) / 1000.0
    position = pygame.mouse.get_pos()

    bg.update(ticks)

    lmb, mmb, rmb = pygame.mouse.get_pressed()
    fired = False
    if lmb:
        fired = True
    p.update(ticks, fired, position)
    screen.blit(es.image, (10, 10))
    screen.blit(em.image, (100, 100))
    screen.blit(eb.image, (200, 200))    

    pygame.display.flip()
