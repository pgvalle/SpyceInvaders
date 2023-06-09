from enum import Enum

class GameScreens(Enum):
    NONE  = 0
    MENU  = 1
    DEMO  = 3
    PLAY  = 4
    PAUSE = 5
    OVER  = 6

'''Screens enums'''

class MenuStates(Enum):
    pass

class PauseStates(Enum):
    # idle state but text keeps blinking
    BLINK_SHOW = 1
    BLINK_HIDE = 2

    RESUMING = 3


'''Entities enums'''

class HordeStates(Enum):
    SPAWNING = 0
    MOVING   = 1

class CannonStates(Enum):
    ALIVE = 0
    DYING = 1
    DEAD  = 2

class TouristStates(Enum):
    ALIVE    = 0
    DYING    = 1
    DEAD     = 2 # show score
    SPAWNING = 3
