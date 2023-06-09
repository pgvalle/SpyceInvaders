import pygame
from pygame.locals import *

from constants import *
from enums     import *

class Invader:
    INVADER1_IMG = pygame.image.load('assets/invader1.png')
    INVADER2_IMG = pygame.image.load('assets/invader2.png')
    INVADER3_IMG = pygame.image.load('assets/invader3.png')

    IMAGES = [INVADER1_IMG, INVADER2_IMG, INVADER3_IMG]

    def __init__(self, x, y, t):
        self.t = t # invader type
        self.i = 0 # animation state
        # position
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rect(self):
        if self.t == 2:
            return pygame.Rect(self.x, self.y, 12, 8)
        if self.t == 1:
            return pygame.Rect(self.x + 1, self.y, 11, 8)
        return pygame.Rect(self.x + 2, self.y, 8, 8)

    def render(self, canvas):
        tex = Invader.IMAGES[self.t]
        canvas.blit(tex, (self.x, self.y), (self.i, 0, 12, 8))


class Horde:
    def __init__(self):
        self.state = HordeStates.SPAWNING

        self.invaders = []
        self.invaders_updated = 0
        # appending invaders in a specific order
        for y in range(128, 64-1, -16):
            for x in range(26, 202, 16):
                self.invaders.append(Invader(x, y, 0))
        # correcting invader types
        for i in range(22):
            self.invaders[i + 22].t = 1 # 2nd and 3rd rows
            self.invaders[i     ].t = 2 # 4th and 5th rows

        # movement direction
        self.dx = 2
        self.dy = 0

    def has_reached_border(self):
        bounds = pygame.Rect(12, 0, WIDTH - 24, HEIGHT)
        for invader in self.invaders:
            rect = pygame.Rect(invader.x, invader.y, 12, 8)
            if not bounds.contains(rect):
                return True
        return False

    def update(self):
        if   self.state == HordeStates.SPAWNING:
            self.invaders_updated += 1
            if self.invaders_updated == len(self.invaders):
                self.state = HordeStates.MOVING
                self.invaders_updated = 0
        elif self.state == HordeStates.MOVING:
            # don't try to update an empty horde
            if len(self.invaders) == 0:
                return
            # update invader
            i = self.invaders_updated
            self.invaders[i].move(self.dx, self.dy)
            self.invaders[i].i = (self.invaders[i].i + 12) % 24
            # update number of updated invaders
            self.invaders_updated = (i + 1) % len(self.invaders)
            # all updated
            if self.invaders_updated == 0:
                if self.has_reached_border():
                    self.dx = -self.dx
                    self.dy = 8
                else:
                    self.dy = 0

    def render(self, canvas):
        if   self.state == HordeStates.SPAWNING:
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
        self.timer = 2000
        self.death_anim_i = 0
    
    def update(self, timelapse):
        if   self.state == CannonStates.ALIVE:
            keyboard = pygame.key.get_pressed()
            if keyboard[pygame.K_LEFT]:
                self.x -= 1
            if keyboard[pygame.K_RIGHT]:
                self.x += 1
        elif self.state == CannonStates.DYING:
            self.timer -= timelapse
            if self.timer <= 0:
                # state change. Set fields
                self.state = CannonStates.DEAD
                self.x = WIDTH # prevent unexpected collisions
                self.lives -= 1
                self.timer = 2000
                self.death_anim_i = 0
        elif self.state == CannonStates.DEAD:
            self.timer -= timelapse
            if self.timer <= 0:
                # state change. Set fields
                self.state = CannonStates.ALIVE
                self.x = 12
                self.timer = 0
                self.death_anim_i = 0

    def render(self, canvas):
        pos = self.x, HEIGHT - 32
        if   self.state == CannonStates.ALIVE:
            canvas.blit(Cannon.IMAGE, pos, (0, 0, 16, 8))
        elif self.state == CannonStates.DYING:
            canvas.blit(Cannon.IMAGE, pos, (16 + 16*self.death_anim_i, 0, 16, 8))
        elif self.state == CannonStates.DEAD:
            pass
