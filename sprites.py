import pygame as pg
import os
from settings import *

v = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.SCREEN_WIDTH = game.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game.SCREEN_HEIGHT

        self.image = pg.image.load(os.path.join(IMAGE_DIR, "cuteMoon.png")).convert()
        # .set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)
        self.image = pg.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        self.shield = False
        self.shield_activation = -SHIELD_COOLDOWN

        # position of the ball
        self.pos = v(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        # velocity of the ball
        self.vel = v(0, 0)
        # acceleration of the ball
        self.acc = v(0, 0)

        self.jumping = False

    # Move the sprite based on user keypresses

    def update(self):
        #Check the shield timer
        now = pg.time.get_ticks()
        if now - self.shield_activation > SHIELD_DURATION:
            self.shield = False

        if self.shield:
            self.image = pg.image.load(os.path.join(IMAGE_DIR, "cuteMoon-shield.png")).convert()
            self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)
            self.image = pg.transform.scale(self.image, (64, 64))
        else:
            self.image = pg.image.load(os.path.join(IMAGE_DIR, "cuteMoon.png")).convert()
            self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)
            self.image = pg.transform.scale(self.image, (64, 64))

        # acceleration is downward unless certain keys are pressed
        self.acc = v(0, BALL_GRAVITY)

        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.acc.x = -BALL_ACC
        if pressed_keys[pg.K_RIGHT]:
            self.acc.x = BALL_ACC

        # apply friction
        self.acc.x += self.vel.x * BALL_FRICTION
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
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = BALL_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < BALL_JUMP_CUT:
                self.vel.y = BALL_JUMP_CUT

class Clouds(pg.sprite.Sprite):
    def __init__(self, game, pos_1, pos_2):
        self._layer = 1
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        width = int(abs(pos_1[0] - pos_2[0]))
        height = int(abs(pos_1[1] - pos_2[1]))

        if width < CLOUD_WIDTH_MIN:
            width = CLOUD_WIDTH_MIN

        if width > CLOUD_WIDTH_MAX:
            width = CLOUD_WIDTH_MAX

        height = int(width * 0.6)


        self.image = pg.image.load(os.path.join(IMAGE_DIR, "cloud.png")).convert()
        # .set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((0, 0, 0), pg.RLEACCEL)

        self.image = pg.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

        self.rect.x = pos_1[0]
        self.rect.y = pos_1[1]

        self.creation_time = pg.time.get_ticks()
    
    def update(self):
        now = pg.time.get_ticks()
        
        if now-(self.game.start_game_timer+SPAWN_DELAY)>0:
            self.rect.x -= PLATFORM_SPEED

        if self.rect.right < 0:
            self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, info):
        self.info = info
        self._layer = 3
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.image.load(os.path.join(IMAGE_DIR, info['image'])).convert()
        # .set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)

        if(info['direction'] == "right"):
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=info['coordinates'])
        self.vel = info['speed']

    def update(self):
        if(self.info['direction'] == "bottom"):
            self.rect.y += self.vel
        else:
            self.rect.x -= self.vel
        # Remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            self.kill()
