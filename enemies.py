import pygame
import projectiles
import screen_prop
from screen_prop import screen
import time

enemy_group = pygame.sprite.Group()

def spawn_enemy(enemy_count):
    while enemy_count > 0:
        enemy = Enemy(1000, 500, 0.3, 3, 100)
        enemy_group.add(enemy)
        enemy_count -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 0
        self.flip = False
        player_img = pygame.image.load('assets/player/player_ship.png')
        self.image = pygame.transform.scale(player_img, (int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.death_explosion = pygame.mixer.Sound('assets/player/large-underwater-explosion-short.wav')
        self.death_img = pygame.image.load('assets/player/exp2_0.png')
        self.death_img_size = self.death_img.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cooldown = 0
        self.health = health
        self.hit_count = 0


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
        if self.health <= 0:
            self.enemy_death()
            self.kill()
            self.remove()

    def enemy_death(self):
        x_cell = 4
        y_cell = 4
        cell_width = int(self.death_img_size[0] / x_cell)
        cell_height = int(self.death_img_size[1] / y_cell)

        cell_list = []
        cell_pos = 0
        frame_count = 0

        for y in range(0, self.death_img_size[1], cell_height):
            for x in range(0, self.death_img_size[0], cell_width):
                surface = pygame.Surface((cell_width, cell_height))
                surface.blit(self.death_img, (0, 0),
                             (x, y, cell_width, cell_height))
                cell_list.append(surface)

        self.death_explosion.set_volume(0.4)
        self.death_explosion.play()

        while cell_pos < len(cell_list) - 1:
            screen.blit(cell_list[cell_pos], (self.rect.centerx - 32, self.rect.centery - 32))
            explosion_rect = pygame.Rect(self.rect.centerx - 32, self.rect.centery - 32, cell_width, cell_height)
            pygame.display.update(explosion_rect)
            frame_count += 1
            print(frame_count)
            if frame_count % 1000 == 0:
                cell_pos += 1
            else:
                cell_pos = cell_pos

    def draw(self):
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)