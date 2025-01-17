import pygame as pg
import os
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Initialize pygame
        pg.init()
        pg.mixer.init()

        # Set up the drawing window
        self.screen = pg.display.set_mode((800, 600))
        #self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # Define constants for the screen width and height
        self.SCREEN_WIDTH = pg.display.Info().current_w
        self.SCREEN_HEIGHT = pg.display.Info().current_h

        #set the font
        self.font_name = pg.font.match_font('georgia')

        #Title and Icon
        pg.display.set_caption(TITLE)
        icon = pg.image.load(os.path.join(IMAGE_DIR, "cuteMoon.png"))
        icon.set_colorkey((255, 255, 255), pg.RLEACCEL)
        pg.display.set_icon(icon)

        # Setup the clock
        self.clock = pg.time.Clock()

        #load HighScore
        self.load_data()

        #position background in correct place
        self.x_bkgd = 0

        # load the splash screen
        self.splash_bkgd = pg.image.load(os.path.join(IMAGE_DIR, "splash-screen.png")).convert()
        self.splash_bkgd = pg.transform.scale(self.splash_bkgd, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.x_splash_bkgd = 0

        # load the end screen
        self.end_bkgd = pg.image.load(os.path.join(IMAGE_DIR, "end-screen.png")).convert()
        self.end_bkgd = pg.transform.scale(self.end_bkgd, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.x_end_bkgd = 0
        
        self.pos_1 = (0,0)

        self.running = True

        
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        print(os.path.join(self.dir, SCORES_FILE))
        print(SCORES_FILE)
        with open(SCORES_FILE, 'r') as f:
            try:
                lines = f.readlines()
                line = lines[0].strip()
                self.highscore = int(line.strip())

            except Exception as e:
                print(e)
                self.highscore = 0

        # load sounds
        self.snd_dir = os.path.join(self.dir, "Sounds")
        self.jump_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Jump_20.wav'))

    def new(self):
        # start a new game

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.enemy_bullet_timer = SPAWN_DELAY
        self.enemy_lander_timer = SPAWN_DELAY

        self.MIN_LANDERS = MIN_LANDERS
        self.MAX_LANDERS = MAX_LANDERS

        self.increase_time = 200

        self.player = Player(self)

        # create a list of platform
        self.platform_list = [((self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT*3/4-10), (self.SCREEN_WIDTH/2 + 100, self.SCREEN_HEIGHT*3/4+10))]

        for plat in self.platform_list:
            Clouds(self, *plat)
        
        self.start_score = pg.time.get_ticks()
        
        #add background theme song
        pg.mixer.music.load(os.path.join(self.snd_dir, "Main_Theme.ogg"))

        self.run()

    def run(self):
        # game loop
        self.playing = True

        pg.mixer.music.play(loops=-1)
        
        self.start_game_timer = pg.time.get_ticks()

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pg.mixer.music.fadeout(800)

    def update(self):
        # game loop - update
        self.all_sprites.update()

        #spawn bullet
        self.create_Enemies_Bullet()

        #spawn bullet
        self.create_Enemies_Landers()
            
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
                        self.player.pos.y = lowest.rect.top+lowest.rect.height/2
                        self.player.vel.y = 0
                        self.player.jumping = False

        # check losing condition : Falling down
        if self.player.rect.bottom > self.SCREEN_HEIGHT:
            self.playing = False

        # check losing condition : Being hit by an enemy
        enemy_hits = pg.sprite.spritecollideany(self.player, self.enemies, False)
        if enemy_hits!=None:
            if self.player.shield:
                enemy_hits.kill()
                #self.player.shield = False
            else:
                self.playing = False

    def events(self):
        # game loop - events

        for event in pg.event.get():
            # check for closing the window with the close button
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                # check for closing the window with Esc
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

                # check for jumping
                if event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                # check for jumping short
                if event.key == pg.K_UP:
                    self.player.jump_cut()

            if event.type == pg.MOUSEBUTTONDOWN: 
                #if the mouse button equals LEFT
                if event.button == 1:
                    self.pos_1 = pg.mouse.get_pos()
                #if the mouse button equals Right
                if event.button == 3:
                    now = pg.time.get_ticks()
                    if now - self.player.shield_activation > SHIELD_COOLDOWN:
                        self.player.shield_activation = pg.time.get_ticks()
                        self.player.shield = True


            #Draw platforms
            if event.type == pg.MOUSEBUTTONUP: 
                #if the mouse button equals LEFT
                if event.button == 1:
                    pos_2 = pg.mouse.get_pos()

                    Clouds(self, self.pos_1, pos_2)

                    if len(self.platforms)>3:

                        lower = pg.time.get_ticks()
                        toKill = None
                        for cloud in self.platforms:
                            if cloud.creation_time < lower:
                                toKill = cloud
                                lower = cloud.creation_time
                                
                        toKill.kill()
                

    def draw(self):
        # game loop - draw

        # game scrolling background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.splash_bkgd, (self.x_bkgd, 0))
        self.screen.blit(self.splash_bkgd, (self.SCREEN_WIDTH + self.x_bkgd, 0))

        if self.x_bkgd == -self.SCREEN_WIDTH:
            self.screen.blit(self.splash_bkgd, (self.SCREEN_WIDTH + self.x_bkgd, 0))
            self.x_bkgd = 0
        self.x_bkgd -= 1

        self.all_sprites.draw(self.screen)

        self.score =  int((pg.time.get_ticks()-self.start_score)/100)
        self.draw_text("Score: "+str(self.score), 22, (255,255,255), 50, 10)

        pg.display.update()

    def show_start_screen(self):
        #game start/splash screen

        #Music
        pg.mixer.music.load(os.path.join(self.snd_dir, "Splash_Screen.ogg"))
        pg.mixer.music.play(loops=-1)

        self.screen.blit(self.splash_bkgd, (self.x_splash_bkgd, 0))
        self.draw_text(TITLE, 36, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4)
        self.draw_text("Player 1 - use LEFT, RIGHT and UP arrows to MOVE the ball", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        self.draw_text("Player 2 - DRAG your MOUSE to DRAW platforms and RIGHT click to SHIELD!", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 3 / 4)
        self.draw_text("High score: "+str(self.highscore), 22, (255,255,255), self.SCREEN_WIDTH / 2, 50)
        pg.display.flip()
        self.wait_for_key()

        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue

        pg.mixer.music.load(os.path.join(self.snd_dir, "Game_Over.ogg"))
        pg.mixer.music.play(loops=-1)

        self.screen.blit(self.end_bkgd, (self.x_end_bkgd, 0))
        self.draw_text("GAME OVER", 48, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4)
        self.draw_text("Score: "+str(self.score), 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New HIGH SCORE!", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 50)
            with open(SCORES_FILE, 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High score: "+str(self.highscore), 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 50)

        self.draw_text("Press a key to play again", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

        pg.mixer.music.fadeout(500)
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def create_Enemies_Bullet(self):
        now = pg.time.get_ticks()

        if now-(self.start_game_timer+SPAWN_DELAY)>BULLET_SPAWN_DELAY:
            if now - self.enemy_bullet_timer > BULLET_SPAWN_TIME + random.choice([-1500,-1000,-500,0,500,1000,1500]):

                self.enemy_bullet_timer = now
                n_enemies = random.randint(MIN_ENEMIES,MAX_ENEMIES)
                space = 32*n_enemies

                x_coord = None
                y_coord = random.randint(ENEMY_SIZE,self.SCREEN_HEIGHT-space)
                
                speed = random.randint(MIN_SPEED_X, MAX_SPEED_X)

                info = {}
                info['image'] = "bullet.png"
                info['direction'] = random.choice(['right','left'])
                
                if info['direction'] == 'right':
                    x_coord = self.SCREEN_WIDTH
                    info['speed'] = speed
                if info['direction'] == 'left':
                    x_coord = 0
                    info['speed'] = -speed
            
                for i in range(n_enemies):
                    info['coordinates'] = (x_coord, y_coord + 32*i)
                    Enemy(self,info)

    def create_Enemies_Landers(self):
        now = pg.time.get_ticks()
        
        if now-(self.start_game_timer+SPAWN_DELAY)>LANDER_SPAWN_DELAY:
            if now - self.enemy_lander_timer > LANDER_SPAWN_TIME + random.choice([-1500,-1000,-500,0,500,1000,1500]):

                self.enemy_lander_timer = now
                
                if now-self.start_game_timer>self.increase_time:
                    self.increase_time += self.increase_time*3/4
                    self.MIN_LANDERS += 1
                    self.MAX_LANDERS += 1
                
                n_enemies = random.randint(self.MIN_LANDERS,self.MAX_LANDERS)
                if(n_enemies>MAX_LANDERS_TOT):
                    n_enemies = MAX_LANDERS_TOT

                
                #space = ENEMY_SIZE*n_enemies

                info = {}
                info['image'] = "lander.png"
                info['direction'] = 'bottom'
                left_margin = ENEMY_SIZE
                for i in range(n_enemies):
                    right_margin = int((self.SCREEN_WIDTH)/(n_enemies-i))+left_margin
                    print(left_margin, right_margin)
                    info['coordinates'] = (random.randint(left_margin, right_margin), 0)
                    info['speed'] = random.randint(MIN_SPEED_X+2, MAX_SPEED_X+2)
                    left_margin = int(right_margin+ENEMY_SIZE)
                    Enemy(self,info)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
