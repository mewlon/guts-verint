import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

# Initialize pygame
pygame.init()

# Set up the drawing window
#screen = pygame.display.set_mode((800, 600))

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

print(SCREEN_WIDTH)
print(SCREEN_HEIGHT)

#Title and Icon
pygame.display.set_caption("Save A Ball")
icon = pygame.image.load('Images/ball-icon.png')
pygame.display.set_icon(icon)

#Background Image
backgroundImg = pygame.image.load('Images/background.jpg')

#Ball image
ballImg = pygame.image.load('Images/ball64.png')

ballX = 400
ballY = 300

ballX_change = 0

def displayBall():
    screen.blit(ballImg, (ballX, ballY))

#Ball image
bulletImg = pygame.image.load('Images/bullet.png')

bulletX = 0
bulletY = 300

bulletX_change = 0

def displayBullet():
    screen.blit(bulletImg, (bulletX, bulletY))

def moveBallX():
    move = ballX+ballX_change

    if(move>=(SCREEN_WIDTH-64)):
        return SCREEN_WIDTH-64
    if(move<0):
        return 0

    return move

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

    ballX = moveBallX()

    bulletX += 0.5

    displayBullet()
    displayBall()

    pygame.display.update()

# Done! Time to quit.
pygame.quit()