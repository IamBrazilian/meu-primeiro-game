import pygame
pygame.mixer.init()

effect_melee = pygame.mixer.Sound('./data/sounds/swosh-08.ogg')
click_sound = pygame.mixer.Sound('./data/sounds/click_2.ogg')
enemy__death = pygame.mixer.Sound('./data/sounds/enemy_death.ogg')
player__death = pygame.mixer.Sound('./data/sounds/player_death.ogg')
intro_sound = pygame.mixer.Sound('./data/sounds/intro_music.ogg')
playing_sound = pygame.mixer.Sound('./data/sounds/playing_music.ogg')

foot_step_1 = pygame.mixer.Sound('./data/sounds/step_cloth1.ogg')
foot_step_2 = pygame.mixer.Sound('./data/sounds/step_cloth2.ogg')
foot_step_3 = pygame.mixer.Sound('./data/sounds/step_cloth3.ogg')
foot_step_4 = pygame.mixer.Sound('./data/sounds/step_cloth4.ogg')

WIN_WIDHT = 800
WIN_HEIGHT = 640

TILESIZE = 32

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

FPS = 60


map = [
    'ppppppppppppppppppppppppp',
    'p...........e...........p',
    'p....e.....e............p',
    'p.........e...e.........p',
    'p........e.....e........p',
    'p...............e.......p',
    'p.........l.......e.....p',
    'p...........e....e......p',
    'p.....e...ee....e.......p',
    'p...eeeeee.....e....ee..p',
    'p.........e..ee.........p',
    'p.....ee................p',
    'p.....e............eee..p',
    'p..........e............p',
    'p........eeee......e....p',
    'p.......ee...e....e.....p',
    'p................e......p',
    'p....eeeeee.e.eee.......p',
    'p.......................p',
    'ppppppppppppppppppppppppp'
]
