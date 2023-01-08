import pygame
RES=(800,600)
class Ammo(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([width,height])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.speed=0
        self.vector=0
    def update(self):
        self.rect.y+=self.vector*self.speed
        if self.rect.y<0 or self.rect.y>RES[1]:
            self.kill()
