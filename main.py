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
        self.screen = pg.display.set_mode((1280, 720))
        #screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # Define constants for the screen width and height
        self.SCREEN_WIDTH = pg.display.Info().current_w
        self.SCREEN_HEIGHT = pg.display.Info().current_h

        #set the font
        self.font_name = pg.font.match_font('arial')

        #Title and Icon
        pg.display.set_caption("Save A Ball")
        icon = pg.image.load(os.path.join("Images", "ball-icon.png"))
        pg.display.set_icon(icon)

        # Setup the clock
        self.clock = pg.time.Clock()
        self.FPS = 90

        # load the background
        self.bkgd = pg.image.load("Images/parallax-mountain-bg.png").convert()
        # scale background to size of display
        self.bkgd = pg.transform.scale(self.bkgd, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #position background in correct place
        self.x = 0

        self.running = True

    def new(self):
        # start a new game

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        # Create and Add player to all_sprites group
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # create a list of platform
        self.platform_list = [(0, self.SCREEN_HEIGHT - 40, self.SCREEN_WIDTH/2, 40),
                              (self.SCREEN_WIDTH/2 - 50, self.SCREEN_HEIGHT*3/4, 100, 20)]

        for plat in self.platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

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

        # check if the ball, while falling, hits the platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False

        # check losign condition
        if self.player.rect.bottom > self.SCREEN_HEIGHT:
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

        rel_x = self.x % self.bkgd.get_rect().width
        #display the background into the game
        self.screen.blit(self.bkgd, (rel_x - self.x % self.bkgd.get_rect().width, 0))
        if rel_x < self.SCREEN_WIDTH:
            self.screen.blit(self.bkgd, (rel_x, 0))
        #move the background towards the left so that the player moves right
        pg.draw.line(self.screen, (255, 0, 0), (rel_x, 0), (rel_x, self.SCREEN_HEIGHT), 3)
        self.x -= 1
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


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
