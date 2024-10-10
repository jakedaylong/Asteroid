'''Projectiles'''
import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.laserImg = pygame.image.load('/assets/projectiles/laser_14.png').convert_alpha()
        self.laserImg = self.laserImg.convert()
