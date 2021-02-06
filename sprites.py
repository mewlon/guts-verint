import pygame as pg
import os

v = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.image = pg.image.load(os.path.join("Images", "ball64.png")).convert()
        #.set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        #position of the ball
        self.pos = v(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        #velocity of the ball
        self.vel = v(0,0)
        #acceleration of the ball
        self.acc = v(0,0)

        #Acceleration, Friction constants
        self.BALL_ACC = 0.5
        self.BALL_FRICTION = -0.12
        self.BALL_GRAVITY = 0.8

        self.jump = False
        self.jumpCount = 10

    # Move the sprite based on user keypresses
    def update(self):
        
        #acceleration is downward unless certain keys are pressed
        self.acc = v(0, self.BALL_GRAVITY)

        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.acc.x = -self.BALL_ACC
        if pressed_keys[pg.K_RIGHT]:
            self.acc.x = self.BALL_ACC
        if pressed_keys[pg.K_UP]:
            self.vel.y = -20

        #apply friction
        self.acc.x += self.vel.x * self.BALL_FRICTION
        self.vel += self.acc
        #Equation of motion
        self.pos += self.vel + (self.acc*0.5)

        # Keep player on the screen
        if self.pos.x < 32:
            self.pos.x = 32
        if self.pos.x > self.SCREEN_WIDTH-32:
            self.pos.x = self.SCREEN_WIDTH-32
        if self.pos.y <= 32:
            self.pos.y = 32
        if self.pos.y >= self.SCREEN_HEIGHT-32:
            self.pos.y = self.SCREEN_HEIGHT-32

        #Update the position of the ball
        self.rect.center = self.pos

    def jump(self):
        #self.rect.x += 1
        #hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #self.rect.x -= 1
        #if hits:
        self.vel.y = -20


