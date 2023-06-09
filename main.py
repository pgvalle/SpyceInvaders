import pygame
from pygame.locals import *

from constants import *
from entities  import *
from enums     import GameScreens

'''GAME SCREEN STUFF'''

def process_play_event(state, event):
    pass

def update_play(state):
    state.horde.update()
    state.cannon.update(state.get_timelapse())

def render_play(state):
    canvas = state.canvas

    canvas.fill((0, 0, 0))
    state.horde.render(canvas)
    state.cannon.render(canvas)

    # scale canvas to real window size before rendering
    surface = state.surface
    pygame.transform.scale(canvas, surface.get_size(), surface)
    pygame.display.flip()

class Game:
    def __init__(self):
        self.screen = GameScreens.PLAY
        # internal clock
        self.time_before = 0
        self.time_now    = 0
        self.event_await_time = 1000 // FPS
        # window setup
        self.surface = pygame.display.set_mode((2*WIDTH, 2*HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        # game entities
        self.horde = Horde()
        self.cannon = Cannon()

    def update_clock(self):
        self.time_before = self.time_now
        self.time_now    = pygame.time.get_ticks()

    def get_timelapse(self):
        return self.time_now - self.time_before

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.screen = GameScreens.NONE
        else:
            if   self.screen == GameScreens.PLAY:
                process_play_event(self, event)

    def frame(self):
        if   self.screen == GameScreens.PLAY:
            update_play(self)
            render_play(self)

    def loop(self):
        while self.screen != GameScreens.NONE:
            event = pygame.event.wait(self.event_await_time)
            if event.type == pygame.NOEVENT:
                self.frame()
                self.update_clock()

                # reset event await time
                self.event_await_time = 1000 // FPS
            else:
                self.process_event(event)
                self.update_clock()

                # wait less time next iteration
                self.event_await_time -= self.get_timelapse()
                # pygame needs this for this game loop logic to work
                if self.event_await_time <= 0:
                    no_event = pygame.event.Event(pygame.NOEVENT)
                    pygame.event.post(no_event)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Spyce Invaders')
    Game().loop()
    pygame.quit()

