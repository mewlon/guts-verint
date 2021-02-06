import pygame as pg
import os



class Player(pg.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Player, self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.image = pg.image.load(os.path.join("Images", "ball64.png")).convert()
        #.set_colorkey() indicates the color pg will render as transparent
        self.image.set_colorkey((255, 255, 255), pg.RLEACCEL)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        self.jump = False
        self.jumpCount = 10

    # Move the sprite based on user keypresses
    def update(self):
        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.rect.x += -10
        if pressed_keys[pg.K_RIGHT]:
            self.rect.x += 10
        
        if self.jump:
            if self.jumpCount >= -10:
                neg = -1
                if self.jumpCount < 0:
                    neg = 1
                moveUp = (self.jumpCount**2) * 0.5 * neg
                self.jumpCount -= 1

                self.rect.move_ip(0, moveUp)
            else:
                self.jump = False
                self.jumpCount = 10
        else:
            if pressed_keys[pg.K_UP]:
                self.jump = True
                #self.rect.move_ip(0, -5)
            if pressed_keys[pg.K_DOWN]:
                #None
                self.rect.y += 5

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT


