from turtle import width
from Player import GameState
import pygame
BLACK=(0,0,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
RED=(255,0,0)
ALIEN_SIZE=(30,40)
ALIEN_SPACER=20
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('F:/invaders/Spaceship16.png').convert()
        self.image.set_colorkey(WHITE)

        self.size=(ALIEN_SIZE)
        self.image=pygame.Surface(ALIEN_SIZE)
        self.rect=self.image.get_rect()
        self.has_moved=[0,0]
        self.vector=[1,1]
        self.travel=[(ALIEN_SIZE[0]-7),ALIEN_SPACER]
        self.speed=7
        self.time=pygame.time.get_ticks()
    def update(self):
        if GameState.alien_time-self.time>self.speed:
            if self.has_moved[0]<12:
                self.rect.x+=self.vector[0]*self.travel[0]
                self.has_moved[0]+=1
            else:
                if not self.has_moved[1]:
                    self.rect.y+=self.vector[1]*self.travel[0]
                self.vector[0]*=-1
                self.has_moved=[0,0]
                self.speed-=20
                if self.speed<=200:
                    self.speed=200
            self.time=GameState.alien_time
        self.image=pygame.image.load('F:/invaders/Spaceship16.png').convert()
        self.image.set_colorkey(WHITE)
