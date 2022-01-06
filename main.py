import pygame
import sys
from sprites import *
from config import *


class Spritesheet():
    def __init__(self, file) -> None:
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((BLACK))
        return sprite

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDHT, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('./data/font/PIXEARG_.TTF', 32)

        self.character_spritesheet = Spritesheet('./data/sprites/character.png')
        self.terrain_spritesheet = Spritesheet('./data/sprites/terrain.png')
        self.enemy_spritesheet = Spritesheet('./data/sprites/enemy.png')
        self.attack_spritesheet = Spritesheet('./data/sprites/attack.png')
        self.intro_background = pygame.image.load('./data/sprites/introbackground.png')
        self.gameover_background = pygame.image.load('./data/sprites/gameover.png')

    def CreateBlocks(self):
        for i, linha in enumerate(map):
            for c, column in enumerate(linha):
                Ground(self, c, i)
                if column == 'p':
                    Terrain(self, c, i)
                if column == 'l':
                    self.Player = Player(self, c, i)
                if column == 'e':
                    Enemy(self, c, i)

    def new(self):
        self.playing = True
        intro_sound.stop()
        playing_sound.stop()
        playing_sound.play(-1)
        

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.attack = pygame.sprite.LayeredUpdates()

        self.CreateBlocks()
    
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.enemy_index()
            self.draw()

    def enemy_index(self):
        if len(self.enemy.sprites()) == 0:
            for sprite in self.all_sprites:
                sprite.kill()
            self.intro_screen()

    def draw(self):  
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.Player.pos == 'up':
                        Attacks(self, self.Player.rect.x, self.Player.rect.y - TILESIZE)

                    if self.Player.pos == 'down':
                        Attacks(self, self.Player.rect.x, self.Player.rect.y + TILESIZE)

                    if self.Player.pos == 'right':
                        Attacks(self, self.Player.rect.x + TILESIZE, self.Player.rect.y)

                    if self.Player.pos == 'left':
                        Attacks(self, self.Player.rect.x - TILESIZE, self.Player.rect.y)
                    effect_melee.play()

    def update(self):
        self.all_sprites.update()
        pygame.display.update()

    def game_over(self):
        text = self.font.render('Game Over', True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDHT / 2, WIN_HEIGHT / 2))
        button = Button(10, 10, 200, 50, BLACK, GREEN, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            
            if self.running:
                self.screen.blit(self.gameover_background, (0, 0))
                self.screen.blit(text, text_rect)
                self.screen.blit(button.image, button.rect)
                self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro_sound.stop()
        playing_sound.stop()
        intro_sound.play(-1)
        intro = True

        titulo = self.font.render('KKKK', True, BLACK)
        titulo_rect = titulo.get_rect(x=10, y=10)
        button = Button(10, 50, 100, 50, GREEN, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    intro = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.new()
                click_sound.play()
            
            if intro:
                self.screen.blit(self.intro_background, (0, 0))
                self.screen.blit(titulo, titulo_rect)
                self.screen.blit(button.image, button.rect)
                self.clock.tick(FPS)
            pygame.display.update()

game = Game()
game.intro_screen()
game.new()

while game.running:
    game.main()
    game.game_over()
pygame.quit()
sys.exit()
