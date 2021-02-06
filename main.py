import pygame as pg
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

        #Title and Icon
        pg.display.set_caption("Save A Ball")
        icon = pg.image.load('Images/ball-icon.png')
        pg.display.set_icon(icon)

        # Setup the clock
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.running = True
        

    def new(self):
        # start a new game

        self.all_sprites = pg.sprite.Group()
        #Create and Add player to all_sprites group
        self.player = Player(self)
        self.all_sprites.add(self.player)
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

    def events(self):
        # game loop - events
        
        for event in pg.event.get():
            #check for cosing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

    def draw(self):
        # game loop - draw

        # Fill the background with a color
        self.screen.fill((225, 187, 83))

        self.all_sprites.draw(self.screen)
        pg.display.update()

    def show_start_screen(self):
        pass

    def show_over_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_over_screen()

pg.quit()