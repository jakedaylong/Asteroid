'''Projectiles'''
import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


bullet_group = pygame.sprite.Group()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/laser_14.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
