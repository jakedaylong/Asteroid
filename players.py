import pygame.sprite
import pygame
import enemies
import screen_prop
import math

player_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()

hit_flag = False

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, player_name):
        pygame.sprite.Sprite.__init__(self)
        self.player_name = player_name
        self.max_speed = speed
        self.direction = 0
        self.flip = False
        player_img = pygame.image.load('assets/player/player_ship.png').convert_alpha()
        self.image = pygame.transform.scale(player_img, (int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cooldown = 0
        self.player_score = 0
        self.current_time = 0
        self.animation_time = 0.02
        self.accel = 0
        self.decel = .92
        self.dx = 0
        self.dy = 0

    def move(self, move_left, move_right, move_fwd, move_bwd, speed_boost, time_delta):

        #self.current_time += time_delta

        if move_left:
            self.accel = -0.2
        if move_right:
            self.accel = 0.2
        # if move_fwd:
        #     dy = -self.speed
        # if move_bwd:
        #     dy = self.speed
        # if speed_boost:
        #     self.speed = 10
        # else:
        #     self.speed = 5

        self.dx += self.accel
        if abs(self.dx) >= self.max_speed:
            self.dx = self.dx / abs(self.dx) * self.max_speed

        if not move_left and not move_right:
            self.accel = 0

        if self.accel == 0:
            self.dx *= self.decel
            if -0.01 <= self.dx <= 0.001:
                self.dx = 0.0

        self.rect.x += self.dx
        # self.rect.y += dy

    def shoot_laser(self, shoot):
        if shoot:
            if self.cooldown == 0:
                self.cooldown = 10
                bullet = Laser(self.rect.centerx, self.rect.centery)
                player_bullet_group.add(bullet)

    def shoot_missile(self, missile):
        if missile:
            if self.cooldown == 0:
                self.cooldown = 20
                missile = Missile(self.rect.centerx, self.rect.centery)
                player_bullet_group.add(missile)

    def update(self, mouse_pos):
        if self.cooldown > 0:
            self.cooldown -= 1
        for target in enemies.enemy_group:
            self.player_score = 10 * target.hit_count

    def draw(self):
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/projectiles/laser_14.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        laser_sound = pygame.mixer.Sound('assets/projectiles/tir.mp3')
        laser_sound.set_volume(0.3)
        laser_sound.play()
        self.laser_hit = pygame.image.load('assets/projectiles/laser_hit.png').convert_alpha()
        self.laser_hit_rect = self.laser_hit.get_rect()
        self.laser_hit_sound = pygame.mixer.Sound('assets/projectiles/explosion.wav')
        self.laser_hit_sound.set_volume(0.2)
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < screen_prop.SCREEN_HEIGHT - screen_prop.SCREEN_HEIGHT + 10:
            self.kill()
        for target in enemies.enemy_group:
            if target.rect.top < self.rect.centery < target.rect.bottom and target.rect.left < self.rect.centerx < target.rect.right:
                screen_prop.screen.blit(self.laser_hit, (
                self.rect.centerx - self.laser_hit_rect.centerx, self.rect.centery - self.laser_hit_rect.centery))
                self.laser_hit_sound.play()
                target.health -= 10
                target.hit_count += 1
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
        self.speed = 3
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.image.get_height() / 2))
        self.direction = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < screen_prop.SCREEN_HEIGHT - screen_prop.SCREEN_HEIGHT + 10:
            self.kill()
        for target in enemies.enemy_group:
            if target.rect.top < self.rect.centery < target.rect.bottom and target.rect.left < self.rect.centerx < target.rect.right:
                screen_prop.screen.blit(self.laser_hit, (
                    self.rect.centerx - self.laser_hit_rect.centerx,
                    self.rect.centery - self.laser_hit_rect.centery))
                self.laser_hit_sound.play()
                target.health -= 30
                target.hit_count += 3
                self.kill()




