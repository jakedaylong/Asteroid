'''Projectiles'''
import pygame
import screen_prop

bullet_group = pygame.sprite.Group()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/laser_14.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        laser_sound = pygame.mixer.Sound('assets/projectiles/tir.mp3')
        laser_sound.play()
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom > screen_prop.SCREEN_HEIGHT:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/missile00.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()), int(self.image.get_height())))
        laser_sound = pygame.mixer.Sound('assets/projectiles/tir.mp3')
        laser_sound.play()
        self.speed = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        while self.speed < 7:
            self.speed += 1
        self.rect.y -= self.speed
        if self.rect.bottom > screen_prop.SCREEN_HEIGHT:
            self.kill()