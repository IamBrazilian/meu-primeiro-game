import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER  # Camada do player
        self.groups = game.all_sprites  # Ligação com all_sprites da classe game
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.pos_x = 0
        self.pos_y = 0 

        self.pos = 'down'

        self.current_sprite = 1

        self.down_animation = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(67, 2, self.width, self.height), ]
        
        self.up_animation = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(67, 34, self.width, self.height), ]

        self.right_animation = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(67, 66, self.width, self.height), ]
        
        self.left_animation = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(67, 98, self.width, self.height), ]


    def update(self):
        self.moviment()
        self.player_animation()
        self.enemy_collision()

        self.rect.y += self.pos_y
        self.blocks_collision('y')
        self.rect.x += self.pos_x
        self.blocks_collision('x')

        self.pos_y = 0
        self.pos_x = 0

    def moviment(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.pos_x += PLAYER_SPEED
            self.pos = 'right'

        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.pos_y += PLAYER_SPEED
            self.pos = 'down'

        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.pos_x -= PLAYER_SPEED
            self.pos = 'left'

        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.pos_y -= PLAYER_SPEED
            self.pos = 'up'

        if keys[pygame.K_a] & keys[pygame.K_d] & keys[pygame.K_s] or keys[pygame.K_a] & keys[pygame.K_s]:
            self.pos = 'down'

    def player_animation(self):
        if self.pos == 'down':
            if self.pos_y == 0:
                self.image = self.down_animation[0]
            else:
                self.image = self.down_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                self.foot_steps()
                if self.current_sprite >= 3:
                    self.current_sprite = 1
                    foot_step_4.play()

        if self.pos == 'up':
            if self.pos_y == 0:
                self.image = self.up_animation[0]
            else:
                self.image = self.up_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                self.foot_steps()
                if self.current_sprite >= 3:
                    self.current_sprite = 1
                    foot_step_4.play()
        
        if self.pos == 'right':
            if self.pos_x == 0:
                self.image = self.right_animation[0]
            else:
                self.image = self.right_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                self.foot_steps()
                if self.current_sprite >= 3:
                    self.current_sprite = 1
                    foot_step_4.play()

        if self.pos == 'left':
            if self.pos_x == 0:
                self.image = self.left_animation[0]
            else:
                self.image = self.left_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                self.foot_steps()
                if self.current_sprite >= 3:
                    self.current_sprite = 0
                    foot_step_4.play()

    def foot_steps(self):
        if self.current_sprite == 1.1:
            foot_step_1.play()
        if self.current_sprite == 1.6:
            foot_step_2.play()
        if self.current_sprite == 2.2:
            foot_step_3.play()
        if self.current_sprite == 2.8:
            foot_step_3.play()

    def blocks_collision(self, direction):
        
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.pos_x > 0:
                    self.rect.x = hits[0].rect.left - self.width
                    for sprites in self.game.all_sprites:
                        sprites.rect.x += PLAYER_SPEED
                if self.pos_x < 0:
                    self.rect.x = hits[0].rect.right
                    for sprites in self.game.all_sprites:
                        sprites.rect.x -= PLAYER_SPEED
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.pos_y > 0:
                    self.rect.y = hits[0].rect.top - self.height
                    for sprites in self.game.all_sprites:
                        sprites.rect.y += PLAYER_SPEED
                if self.pos_y < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprites in self.game.all_sprites:
                        sprites.rect.y -= PLAYER_SPEED

    def enemy_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemy, False, pygame.sprite.collide_mask)
        if hits:
            self.kill()
            player__death.play()
            playing_sound.stop()
            self.game.playing = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemy_spritesheet.get_sprite(2, 3, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.pos = random.choice(['right', 'left'])
        self.current_sprite = 1
        self.animation_loop = 0
        self.deslocamento = random.randint(10, 50)  # Deslocamento maximo do enimigo entre 7 a 30 px
        self.pos_x = 0
        self.pos_y = 0

        self.right_animation = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(67, 66, self.width, self.height), ]
        
        self.left_animation = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(67, 98, self.width, self.height), ]
        

    def update(self):
        self.enemy_loop()
        self.enemy_animation()

        self.rect.x += self.pos_x
        self.rect.y += self.pos_y

        self.pos_y = 0
        self.pos_x = 0

    def enemy_loop(self):
        if self.pos == 'right':
            self.pos_x += ENEMY_SPEED
            self.animation_loop += 1
            if self.animation_loop >= self.deslocamento:
                self.pos = 'left'

        if self.pos == 'left':
            self.pos_x -= ENEMY_SPEED
            self.animation_loop -= 1
            if self.animation_loop <= -self.deslocamento:
                self.pos = 'right'
    
    def enemy_animation(self):
        if self.pos == 'right':
            if self.pos_x == 0:
                self.image = self.right_animation[0]
            else:
                self.image = self.right_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                if self.current_sprite >= 3:
                    self.current_sprite = 1

        if self.pos == 'left':
            if self.pos_x == 0:
                self.image = self.left_animation[0]
            else:
                self.image = self.left_animation[math.floor(self.current_sprite)]
                self.current_sprite += 0.1
                if self.current_sprite >= 3:
                    self.current_sprite = 0


class Terrain(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = game.all_sprites, game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(993, 543, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(100, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('./data/font/PIXEARG_.TTF', fontsize)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg
        self.content = content

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attacks(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attack
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 1

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.attack_animation()
        self.enemy_collide()

    def attack_animation(self):
        direction = self.game.Player.pos
        
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

    def enemy_collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemy, True, pygame.sprite.collide_mask)
        if hits:
            enemy__death.play()
