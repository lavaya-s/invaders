import pygame
class GameState():
    pass
RES=(800,600)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size=(60,55)
        self.rect=self.image.get_rect()
        self.rect.x=(RES[0]/2)-(self.size[0]/2)
        self.rect.y=520
        self.travel=7
        self.speed=350
        self.time=pygame.time.get_ticks()
    def update(self):
        self.rect.x+= GameState.vector*self.travel
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x>RES[0]-self.size[0]:
            self.rect.x=RES[0]-self.size[0]