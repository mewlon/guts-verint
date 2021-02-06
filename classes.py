import pygame
import os

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

#Path to images folder
def path_images(filename):
    return os.path.join("Images", filename)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(path_images("ball64.png")).convert()
        #.set_colorkey() indicates the color pygame will render as transparent
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            #Delay the falling down as loops are very fast
            for i in range(20):
                if i <= 10:
                    self.rect.y -= 0.5
                elif i > 10:
                    self.rect.y += 0.5
            #self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            #None
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Initialize pygame
pygame.init()

# Set up the drawing window
#screen = pygame.display.set_mode((800, 600))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Define constants for the screen width and height
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

print(SCREEN_WIDTH)
print(SCREEN_HEIGHT)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Run until the user asks to quit
running = True
while running:

    # Fill the background with white
    screen.fill((225, 187, 83))
    #screen.blit(backgroundImg, (0, 0))

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT:
                print("Left arrow pressed")
                ballX_change = -0.85
            if event.key == K_RIGHT:
                print("Right arrow is pressed")
                ballX_change = 0.85
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                print("Keystroke has been released")
                ballX_change = 0

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    pygame.display.update()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)

# Done! Time to quit.
pygame.quit()