import pygame
import projectiles
import screen_prop

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 0
        self.flip = False
        player_img = pygame.image.load('assets/player/player_ship.png')
        self.image = pygame.transform.scale(player_img, (int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cooldown = 0

    def move(self, move_left, move_right, move_fwd, move_bwd, speed_boost):
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if move_fwd:
            dy = -self.speed
        if move_bwd:
            dy = self.speed
        if speed_boost:
            self.speed = 10
        else:
            self.speed = 5

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self, shoot):
        if shoot:
            if self.cooldown == 0:
                self.cooldown = 10
                bullet = projectiles.Laser(self.rect.centerx, self.rect.centery)
                projectiles.bullet_group.add(bullet)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self):
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)