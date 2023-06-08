import pygame
from pygame.locals import *

from enum import Enum

pygame.init()

# important stuff
FPS = 60
WIDTH, HEIGHT = 224, 256
# assets
INVADER1_IMG = pygame.image.load('assets/invader1.png')
INVADER2_IMG = pygame.image.load('assets/invader2.png')
INVADER3_IMG = pygame.image.load('assets/invader3.png')

class Invader:
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
        self.dx = 2
        self.dy = 0
       
        self.invaders = []
        self.invaders_updated = 0
        # appending invaders in a specific order
        for y in range(128, 64 - 1, -16):
            for x in range(24, 200, 16):
                self.invaders.append(Invader(x, y, 0))
        # correcting invader types
        for i in range(22):
            self.invaders[i + 22].t = 1 # 2nd and 3rd rows
            self.invaders[i     ].t = 2 # 4th and 5th rows

    def has_collided_with_borders(self):
        bounds = pygame.Rect(12, 0, WIDTH - 24, HEIGHT)
        for invader in self.invaders:
            rect = pygame.Rect(invader.x, invader.y, 12, 8)
            if not bounds.contains(rect):
                return True
        return False

    def update(self):
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
            if self.has_collided_with_borders():
                self.dx = -self.dx
                self.dy = 8
            else:
                self.dy = 0

    def render(self, canvas):
        for invader in self.invaders:
            invader.render(canvas)


class Collisions:
    pass


class GameScreen(Enum):
    NONE = 0
    PLAY = 1

class GameState:
    def __init__(self):
        self.screen = GameScreen.PLAY
        # internal clock
        self.time_before = 0
        self.time_now    = 0
        self.event_await_time = 1000 // FPS
        # window
        self.surface = pygame.display.set_mode((2*WIDTH, 2*HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((WIDTH, HEIGHT))

    def update_clock(self):
        self.time_before = self.time_now
        self.time_now    = pygame.time.get_ticks()

    def get_timelapse(self):
        return self.time_now - self.time_before

state = GameState()
horde = Horde()

def process_event(event):
    if event.type == pygame.QUIT:
        state.screen = GameScreen.NONE

def update():
    horde.update()

def render():
    # quick aliases
    surface = state.surface
    canvas  = state.canvas

    canvas.fill((0, 0, 0))
    horde.render(canvas)
    # scale canvas to real window size before rendering
    pygame.transform.scale(canvas, surface.get_size(), surface)
    pygame.display.flip()

while state.screen != GameScreen.NONE:
    event = pygame.event.wait(state.event_await_time)
    if event.type == pygame.NOEVENT:
        # frame (state update and rendering) here
        update()
        render()

        state.update_clock()
        # reset event await time
        state.event_await_time = 1000 // FPS
    else:
        process_event(event)

        state.update_clock()
        # wait less time next iteration
        state.event_await_time -= state.get_timelapse()
        # pygame needs this for this game loop logic to work
        if state.event_await_time <= 0:
            no_event = pygame.event.Event(pygame.NOEVENT)
            pygame.event.post(no_event)

