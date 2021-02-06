import pygame as pg
import os
import random

v = pg.math.Vector2

IMAGE_DIR = "Images"


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.image = pg.image.load(os.path.join(
            IMAGE_DIR, "ball64.png")).convert()
        # .set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)

        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        # position of the ball
        self.pos = v(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        # velocity of the ball
        self.vel = v(0, 0)
        # acceleration of the ball
        self.acc = v(0, 0)

        # Acceleration, Friction constants
        self.BALL_ACC = 0.5
        self.BALL_FRICTION = -0.12
        self.BALL_GRAVITY = 0.8

        self.BALL_JUMP = -20
        self.BALL_JUMP_CUT = -5
        self.jumping = False

    # Move the sprite based on user keypresses

    def update(self):

        # acceleration is downward unless certain keys are pressed
        self.acc = v(0, self.BALL_GRAVITY)

        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.acc.x = -self.BALL_ACC
        if pressed_keys[pg.K_RIGHT]:
            self.acc.x = self.BALL_ACC

        # apply friction
        self.acc.x += self.vel.x * self.BALL_FRICTION
        self.vel += self.acc
        # Equation of motion
        self.pos += self.vel + (self.acc*0.5)

        # Keep player on the screen
        if self.pos.x < 32:
            self.pos.x = 32
        if self.pos.x > self.SCREEN_WIDTH-32:
            self.pos.x = self.SCREEN_WIDTH-32
        if self.pos.y <= 32:
            self.pos.y = 32

        # Update the position of the ball
        self.rect.midbottom = self.pos

    def jump(self):

        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = self.BALL_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < self.BALL_JUMP_CUT:
                self.vel.y = self.BALL_JUMP_CUT


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = 1
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, info):
        self._layer = 3
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # self.image = pg.Surface((20, 10))
        # self.image.fill((255, 255, 255))

        self.image = pg.image.load(os.path.join(
            IMAGE_DIR, "bullet.png")).convert()
        # .set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)

        if(info['direction'] == "right"):
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=info['coordinates'])
        self.vel = info['speed']

    def update(self):
        self.rect.x -= self.vel
        pg.transform.flip(self.image, False, True)
        # Remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            self.kill()
