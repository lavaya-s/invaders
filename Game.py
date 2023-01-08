
import pygame
import random
from Ammo import Ammo
from Block import Block
from Player import Player,GameState
from Alien import Alien
#regular global variable at the top
BLACK=(0,0,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
RED=(255,0,0)
ALIEN_SIZE=(30,40)
ALIEN_SPACER=20
BARRIER_ROW=10
BARRIER_COLUMN=4
BULLET_SIZE=(5,10)
MISSILE_SIZE=(5,5)
BLOCK_SIZE=(10,10)
RES=(800,600)
class Game(object):
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.font.init()
        self.clock=pygame.time.Clock()
        self.game_font=pygame.font.Font('F:/invaders/Orbitracer.ttf',28)
        self.intro_font=pygame.font.Font('F:/invaders/Orbitracer.ttf',72)
        self.screen=pygame.display.set_mode([RES[0],RES[1]])
        self.time=pygame.time.get_ticks()
        self.refresh_rate=20
        self.rounds_won=0
        self.level_up=50
        self.score=0
        self.lives=2
        self.player_group=pygame.sprite.Group()
        self.alien_group=pygame.sprite.Group()
        self.bullet_group=pygame.sprite.Group()
        self.missile_group=pygame.sprite.Group()
        self.barrier_group=pygame.sprite.Group()
        self.all_sprite_list=pygame.sprite.Group()
        self.intro_screen=pygame.image.load('F:/invaders/start_screen.jpg').convert()
        self.background=pygame.image.load('F:/invaders/Space-Background.jpg').convert()
        pygame.display.set_caption('Invaders-ESC to Exit')
        pygame.mouse.set_visible(False)
        self.ani_pos=5#scale from 1-11
        self.ship_sheet=pygame.image.load('F:/invaders/Ship_sheet_final.png').convert_alpha()
        Player.image=self.ship_sheet.subsurface(self.ani_pos*64,0,64,61)
        self.animate_right=False
        self.animate_left=False
        self.explosion_sheet=pygame.image.load('F:/invaders/explosion_new1.png').convert_alpha()
        self.explosion_image=self.explosion_sheet.subsurface(0,0,79,96)
        self.alien_explosion_sheet=pygame.image.load('F:/invaders/alien_explosion.png')
        self.alien_explosion_graphics=self.alien_explosion_sheet.subsurface(0,0,94,96)
        self.explode=False
        self.explode_pos=0
        self.alienexplode=False
        self.alien_explode_pos=0
        #current sound code is commented out due to issues with pygame
        #pygame.mixer.music.load('F:\invaders\Dead_city.mp3')
        #pygame.mixer.music.play(-1)
        #pygame.mixer.music.set_volume(0.7)
        #self.bullet_f=pygame.mixer.Sound('F:\invaders\pivaders_data_sound_._medetix__pc-bitcrushed-lazer-beam.ogg')
        #self.explosion_fx=pygame.mixer.Sound('F:\invaders\pivaders_data_sound_._timgormly__8-bit-explosion.ogg')
        #self.explosion_fx.set_volume(0.5)
        self.explodey_alien=[]

        #Alien.image=pygame.image.load('F:/invaders/Spaceship16.png').convert()
        #Alien.image.set_colorkey(WHITE)
        #self.alien=pygame.image.load('F:/invaders/Spaceship16.png').convert()
        GameState.end_game=False
        GameState.start_screen=True
        GameState.vector=0
        GameState.shoot_bullet=False
    def control(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                GameState.start_screen=False
                GameState.end_game=True
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                if GameState.start_screen:
                    GameState.start_screen=False
                    GameState.end_game=True
                    self.kill_all()
                else:
                    GameState.start_screen=True
            self.keys=pygame.key.get_pressed()
            if self.keys[pygame.K_LEFT]:
                GameState.vector=-1
                self.animate_left=True
                self.animate_right=False
            elif self.keys[pygame.K_RIGHT]:
                GameState.vector=1
                self.animate_right=True
                self.animate_left=False
            else:
                GameState.vector=0
                self.animate_right=False
                self.animate_left=False
            if self.keys[pygame.K_SPACE]:
                if GameState.start_screen:
                    GameState.start_screen=False
                    self.lives=2
                    self.score=0
                    self.make_player()
                    self.make_defenses()
                    self.alien_wave(0)
                else:
                    GameState.shoot_bullet=True
                    #self.bullet_f.play()
    def animate_player(self):
        if self.animate_right:
            if self.ani_pos<10:
                Player.image=self.ship_sheet.subsurface(self.ani_pos*64,0,64,61)
                self.ani_pos+=1
        else:
            if self.ani_pos>5:
                self.ani_pos-=1
                Player.image=self.ship_sheet.subsurface(self.ani_pos*64,0,64,61)
        if self.animate_left:
            if self.ani_pos>0:
                self.ani_pos-=1
                Player.image=self.ship_sheet.subsurface(self.ani_pos*64,0,64,61)
        else:
            if self.ani_pos<5:
                Player.image=self.ship_sheet.subsurface(self.ani_pos*64,0,64,61)
                self.ani_pos+=1
    def player_explosion(self):
        if self.explode:
            if self.explode_pos<8:
                self.explosion_image=self.explosion_sheet.subsurface(0,self.explode_pos*96,79,96)
                self.explode_pos+=1
                self.screen.blit(self.explosion_image,[self.player.rect.x-10,self.player.rect.y-30])
            else:
                self.explode=False
                self.explode_pos=0
    def alien_explosion(self):
        if self.alienexplode:
            if self.alien_explode_pos<9:
                self.alien_explosion_graphics=self.alien_explosion_sheet.subsurface(0,self.alien_explode_pos*96,94,96)
                self.alien_explode_pos+=1
                self.screen.blit(self.alien_explosion_graphics,[int(self.explodey_alien[0])-50,int(self.explodey_alien[1])-60])
            else:
                self.alienexplode=False
                self.alien_explode_pos=0
                self.explodey_alien=[]
    def splash_screen(self):
        while GameState.start_screen:
            self.kill_all()
            self.screen.blit(self.intro_screen,[0,0])
            self.screen.blit(self.intro_font.render('invaders',1,WHITE),(265,120))
            self.screen.blit(self.game_font.render('PRESS SPACE TO PLAY',1,WHITE),(274,191))
#I'm not sure if this continues here
            pygame.display.flip()
            self.control()
    def make_player(self):
        self.player=Player()
        self.player_group.add(self.player)
        self.all_sprite_list.add(self.player)
    def refresh_screen(self):
        self.all_sprite_list.draw(self.screen)
        self.animate_player()
        self.player_explosion()
        self.alien_explosion()
        self.refresh_scores()
        pygame.display.flip()
        self.screen.blit(self.background,[0,0])
        self.clock.tick(self.refresh_rate)
    def refresh_scores(self):
        self.screen.blit(self.game_font.render('SCORE'+str(self.score),1,WHITE),(10,8))
        self.screen.blit(self.game_font.render('LIVES'+str(self.lives+1),1,RED),(355,575))
    def alien_wave(self,speed):
        for column in range(BARRIER_COLUMN):
            for row in range(BARRIER_ROW):
                alien=Alien()
                alien.rect.y=65+(column*(ALIEN_SIZE[1]+ALIEN_SPACER))
                alien.rect.x=ALIEN_SPACER+(row*(ALIEN_SIZE[0]+ALIEN_SPACER))
                self.alien_group.add(alien)
                self.all_sprite_list.add(alien)
                alien.speed-=speed-1000
    def make_bullet(self):
        if GameState.game_time-self.player.time>self.player.speed:
            bullet=Ammo(BLUE,5,10)
            bullet.vector=-1
            bullet.speed=26
            bullet.rect.x=self.player.rect.x+28
            bullet.rect.y=self.player.rect.y
            self.bullet_group.add(bullet)
            self.all_sprite_list.add(bullet)
            self.player.time=GameState.game_time
        GameState.shoot_bullet=False
    def make_missile(self):
        if len(self.alien_group):
            shoot=random.random()
            if shoot<=0.05:
                shooter=random.choice([alien for alien in self.alien_group])
                missile=Ammo(RED,5,5)
                missile.vector=1
                missile.rect.x=shooter.rect.x+15
                missile.rect.y=shooter.rect.y+40
                missile.speed=10
                self.missile_group.add(missile)
                self.all_sprite_list.add(missile)
    def make_barrier(self,columns,rows,spacer):
        for column in range(columns):
            for row in range(rows):
                barrier=Block(WHITE,BLOCK_SIZE,BLOCK_SIZE)
                barrier.rect.x=55+(200*spacer)+(row*10)
                barrier.rect.y=450+(column*10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)
    def make_defenses(self):
        for spacing, spacing in enumerate(range(4)):
            self.make_barrier(3,9,spacing)
    def kill_all(self):
        for items in [self.bullet_group,self.player_group,self.alien_group,self.missile_group,self.barrier_group]:
            for i in items:
                i.kill()
    def is_dead(self):
        if self.lives<0:
            self.screen.blit(self.game_font.render('the war has been lost! you scored:'+str(self.score),1,RED),(250,15))
            self.rounds_won=0
            self.refresh_screen()
            self.level_up=50
            self.explode=False
            self.alienexplode=False
            pygame.time.delay(3000)
            return True
    def win_round(self):
        if len(self.alien_group)<1:
            self.rounds_won+=1
            self.screen.blit(self.game_font.render('You won the round'+str(self.rounds_won)+'but the battle rages on!',1,RED),(200,15))
            self.refresh_screen()
            pygame.time.delay(3000)
            return True
    def defenses_breached(self):
        for alien in self.alien_group:
            if alien.rect.y>410:
                self.screen.blit(self.game_font.render("The Aliens have breached Earth's defenses!",1,RED),(200,15))
                self.refresh_screen()
                self.level_up=50
                self.explode=False
                self.alienexplode=False
                pygame.time.delay(3000)
                return True
    def calc_collisions(self):
        pygame.sprite.groupcollide(self.missile_group,self.barrier_group,True,True)
        pygame.sprite.groupcollide(self.bullet_group,self.barrier_group,True,True)
        for z in pygame.sprite.groupcollide(self.bullet_group,self.alien_group,True,True):
            self.alienexplode=True
            self.explodey_alien.append(z.rect.x)
            self.explodey_alien.append(z.rect.y)
            self.score+=10
            #self.explosion_fx.play()
        if pygame.sprite.groupcollide(self.player_group,self.missile_group,False,True):
            self.lives-=1
            self.explode=True
            #self.explosion_fx.play()
    def next_round(self):
        self.explode=False
        self.alienexplode=False
        for actor in [self.missile_group,self.barrier_group,self.bullet_group]:
            for i in actor:
                i.kill()
        self.alien_wave(self.level_up)
        self.make_defenses()
        self.level_up+=50
    def main_loop(self):
        while not GameState.end_game:
            while not GameState.start_screen:
                GameState.game_time=pygame.time.get_ticks()
                GameState.alien_time=pygame.time.get_ticks()
                self.control()
                self.make_missile()
                self.calc_collisions()
                self.refresh_screen()
                for actor in [self.player_group,self.bullet_group,self.alien_group,self.missile_group]:
                    for i in actor:
                        i.update()
                if GameState.shoot_bullet:
                    self.make_bullet()
                if self.is_dead() or self.defenses_breached():
                    GameState.start_screen=True
                if self.win_round():
                    self.next_round()
            self.splash_screen()
        pygame.quit()
    
if __name__=='__main__':
    pv=Game()
    pv.main_loop()
