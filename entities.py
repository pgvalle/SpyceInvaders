import pygame
from pygame.locals import *

from settings import *
from enums    import *

import random

class Invader:
    INVADER1_IMG = pygame.image.load('assets/invader1.png')
    INVADER2_IMG = pygame.image.load('assets/invader2.png')
    INVADER3_IMG = pygame.image.load('assets/invader3.png')

    IMAGES = [INVADER1_IMG, INVADER2_IMG, INVADER3_IMG]

    def __init__(self, x, y, t):
        self.t = t # invader type
        self.img_x = 0 # animation state
        # position
        self.x = x
        self.y = y

    def rect(self):
        if self.t == 2:
            return pygame.Rect(self.x, self.y, 12, 8)
        if self.t == 1:
            return pygame.Rect(self.x + 1, self.y, 11, 8)
        return pygame.Rect(self.x + 2, self.y, 8, 8)

    def render(self, canvas):
        tex = Invader.IMAGES[self.t]
        canvas.blit(tex, (self.x, self.y), (self.img_x, 0, 12, 8))


class Horde:
    def __init__(self):
        self.state = HordeStates.SPAWNING

        self.invaders = []
        self.invaders_updated = 0
        # appending invaders in correct order and position
        for y in range(128, 64 - 1, -16):
            for x in range(26, 186 + 1, 16):
                self.invaders.append(Invader(x, y, 0))
        # fixing wrong invader types
        for i in range(22):
            self.invaders[i + 22].t = 1 # 2nd and 3rd rows
            self.invaders[i     ].t = 2 # 4th and 5th rows

        # velocity
        self.dx = 2
        self.dy = 0

    def has_reached_border(self):
        bounds = pygame.Rect(12, 0, WIDTH - 24, HEIGHT)
        for invader in self.invaders:
            if not bounds.contains((invader.x, invader.y, 12, 8)):
                return True
        return False

    def update(self):
        if self.state == HordeStates.SPAWNING:
            self.invaders_updated += 1
            if self.invaders_updated == len(self.invaders):
                self.state = HordeStates.MOVING
                self.invaders_updated = 0
        elif self.state == HordeStates.MOVING:
            # don't try to update an empty horde
            if len(self.invaders) == 0:
                return
            # update invader
            invader = self.invaders[self.invaders_updated]
            invader.x += self.dx
            invader.y += self.dy
            invader.img_x = (invader.img_x + 12) % 24

            self.invaders_updated += 1
            if self.invaders_updated == len(self.invaders):
                if self.has_reached_border():
                    self.dx = -self.dx
                    self.dy = 8
                else:
                    self.dy = 0

                self.invaders_updated = 0

    def render(self, canvas):
        if self.state == HordeStates.SPAWNING:
            for i in range(self.invaders_updated):
                self.invaders[i].render(canvas)
        elif self.state == HordeStates.MOVING:
            for invader in self.invaders:
                invader.render(canvas)


class Cannon:
    IMAGE = pygame.image.load('assets/cannon.png')

    def __init__(self):
        self.state = CannonStates.DEAD

        self.x = WIDTH
        self.lives = 3
        self.timer = 1000
        # dead state variables
        self.death_anim_timer = 75
        self.death_img_x = 16

    def update(self, timelapse):
        if self.state == CannonStates.ALIVE:
            keyboard = pygame.key.get_pressed()
            # movement
            if keyboard[pygame.K_LEFT]:
                self.x -= 1
            if keyboard[pygame.K_RIGHT]:
                self.x += 1
            # shooting
            if self.timer <= 0 and keyboard[pygame.K_SPACE]:
                print('shooting')
                self.timer = 1000
        elif self.state == CannonStates.DYING:
            # update death animation state
            if self.death_anim_timer <= 0:
                self.death_anim_timer = 75
                self.death_img_x = (self.death_img_x + 16) % 32

            self.death_anim_timer -= timelapse

            # state change to DEAD
            if self.timer <= 0:
                self.state = CannonStates.DEAD
                self.x = WIDTH # prevent unexpected collisions
                self.lives -= 1
                self.timer = 2000
                self.death_anim_timer = 75
                self.death_img_x = 0
        elif self.state == CannonStates.DEAD:
            # state change to ALIVE
            if self.timer <= 0:
                self.state = CannonStates.ALIVE
                self.x = 12
                self.timer = 0

        self.timer -= timelapse # always update timer

    def render(self, canvas):
        pos = self.x, HEIGHT - 32
        if self.state == CannonStates.ALIVE:
            canvas.blit(Cannon.IMAGE, pos, (0, 0, 16, 8))
        elif self.state == CannonStates.DYING:
            canvas.blit(Cannon.IMAGE, pos, (16 + self.death_img_x, 0, 16, 8))
        elif self.state == CannonStates.DEAD:
            pass


class Tourist:
    IMAGE = pygame.image.load('assets/tourist.png')

    def __init__(self):
        self.state = TouristStates.SPAWNING

        self.x = 16
        self.dx = 2
        self.score = 0
        self.timer = 0

    def update(self, timelapse):
        if self.state == TouristStates.ALIVE:
            self.x += self.dx
            # bound checking
            bounds = pygame.Rect(16, 0, WIDTH - 32, HEIGHT)
            if not bounds.contains((self.x, 40, 16, 8)):
                self.state = TouristStates.SPAWNING
                self.x = WIDTH
                self.dx = 0
                self.score = random.choice((100, 150, 200, 250, 300))
                self.timer = 20000 # 20s
        elif self.state == TouristStates.SPAWNING:
            if self.timer <= 0:
                r = random.randint(0, 1)
                self.state = TouristStates.ALIVE
                self.x = (16, WIDTH - 32)[r]
                self.dx = (2, -2)[r]
                self.timer = 0

        self.timer -= timelapse

    def render(self, canvas):
        if self.state == TouristStates.ALIVE:
            canvas.blit(Tourist.IMAGE, (self.x, 40), (4, 0, 16, 8))
        elif self.state == TouristStates.DYING:
            canvas.blit(Tourist.IMAGE, (self.x - 4, 40), (24, 0, 16, 8))
        elif self.state == TouristStates.DEAD:
            pass
        elif self.state == TouristStates.SPAWNING:
            pass
