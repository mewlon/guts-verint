import pygame as pg
import os
import random
from sprites import *


class Game:
    def __init__(self):
        # Initialize pygame
        pg.init()
        pg.mixer.init()

        # Set up the drawing window
        self.screen = pg.display.set_mode((800, 600))
        #screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # Define constants for the screen width and height
        self.SCREEN_WIDTH = pg.display.Info().current_w
        self.SCREEN_HEIGHT = pg.display.Info().current_h

        #set the font
        self.font_name = pg.font.match_font('georgia')

        #Title and Icon
        pg.display.set_caption("Save A Ball")
        icon = pg.image.load(os.path.join("Images", "ball-icon.png"))
        pg.display.set_icon(icon)

        # Setup the clock
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.ENEMY_SPAWN_DELAY = 2000

        self.running = True

    def new(self):
        # start a new game

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.enemy_timer = self.ENEMY_SPAWN_DELAY

        self.player = Player(self)

        # create a list of platform
        self.platform_list = [(0, self.SCREEN_HEIGHT - 40, self.SCREEN_WIDTH/2, 40),
                              (self.SCREEN_WIDTH/2 - 50, self.SCREEN_HEIGHT*3/4, 100, 20),
                              (self.SCREEN_WIDTH/2 - 50, self.SCREEN_HEIGHT*3/5, 100, 20)]

        for plat in self.platform_list:
            p = Platform(self, *plat)

        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop - update
        self.all_sprites.update()

        #spawn enemy
        now = pg.time.get_ticks()
        if now - self.enemy_timer > 4000 + random.choice([-1500,-1000,-500,0,500,1000,1500]):
            self.enemy_timer = now
            self.createEnemies()
            

        # check if the ball, while falling, hits the platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:

                #find the lowest platform hit
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                
                #if the ball is in the widht of the platform and reached the top of the platform, then stop it
                if self.player.pos.x < lowest.rect.right+8 and self.player.pos.x > lowest.rect.left-8:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # check losing condition : Falling down
        if self.player.rect.bottom > self.SCREEN_HEIGHT:
            self.playing = False

        # check losing condition : Being hit by an enemy
        enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.playing = False

    def events(self):
        # game loop - events

        for event in pg.event.get():
            # check for cosing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

                if event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()

    def draw(self):
        # game loop - draw

        # Fill the background with a color
        self.screen.fill((225, 187, 83))

        self.all_sprites.draw(self.screen)

        pg.display.update()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        # game over/continue
        self.screen.fill((0,255,255))
        self.draw_text("GAME OVER", 48, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4)
        self.draw_text("Score: ", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def createEnemies(self, n_enemies = random.randint(2,5), MinSpeedX = 7, MaxSpeedX = 9):

        space = 32*n_enemies

        x_coord = None
        y_coord = random.randint(0,self.SCREEN_HEIGHT-space)
        
        info = {}
        info['direction'] = random.choice(['right','left'])
        
        if info['direction'] == 'right':
            x_coord = self.SCREEN_WIDTH
            info['speed'] = random.randint(MinSpeedX, MaxSpeedX)
        if info['direction'] == 'left':
            x_coord = 0
            info['speed'] = -random.randint(MinSpeedX,MaxSpeedX)
    
        for i in range(n_enemies):
            info['coordinates'] = (x_coord, y_coord + 32*i)
            Enemy(self,info)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
