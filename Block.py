import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([10,10])
        self.image.fill(color)
        self.rect=self.image.get_rect()
