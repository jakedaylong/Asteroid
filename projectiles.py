#Projectiles
import pygame
import screen_prop
from enemies import enemy_group

bullet_group = pygame.sprite.Group()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/laser_14.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        laser_sound = pygame.mixer.Sound('assets/projectiles/tir.mp3')
        laser_sound.play()
        self.laser_hit = pygame.image.load('assets/projectiles/laser_hit.png').convert_alpha()
        self.laser_hit_rect = self.laser_hit.get_rect()
        self.laser_hit_sound = pygame.mixer.Sound('assets/projectiles/explosion.wav')
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < screen_prop.SCREEN_HEIGHT - screen_prop.SCREEN_HEIGHT + 10:
            self.kill()
        for target in enemy_group:
            if target.rect.top < self.rect.centery < target.rect.bottom and target.rect.left < self.rect.centerx < target.rect.right:
                screen_prop.screen.blit(self.laser_hit, (self.rect.centerx - self.laser_hit_rect.centerx, self.rect.centery - self.laser_hit_rect.centery))
                self.laser_hit_sound.play()
                self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/missile00.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 0)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()), int(self.image.get_height())))
        laser_sound = pygame.mixer.Sound('assets/projectiles/tir.mp3')
        laser_sound.play()
        self.laser_hit = pygame.image.load('assets/projectiles/laser_hit.png').convert_alpha()
        self.laser_hit_rect = self.laser_hit.get_rect()
        self.laser_hit_sound = pygame.mixer.Sound('assets/projectiles/explosion.wav')
        self.speed = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        while self.speed < 7:
            self.speed += 0.07
        self.rect.y -= self.speed
        if self.rect.bottom < screen_prop.SCREEN_HEIGHT - screen_prop.SCREEN_HEIGHT + 10:
            self.kill()
        for target in enemy_group:
            if target.rect.top < self.rect.centery < target.rect.bottom and target.rect.left < self.rect.centerx < target.rect.right:
                screen_prop.screen.blit(self.laser_hit, (
                self.rect.centerx - self.laser_hit_rect.centerx, self.rect.centery - self.laser_hit_rect.centery))
                self.laser_hit_sound.play()
                self.kill()