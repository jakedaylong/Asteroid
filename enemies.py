import pygame
import projectiles
import screen_prop
from screen_prop import screen

enemy_group = pygame.sprite.Group()
BLACK = (0,0,0)

def spawn_enemy(enemy_count):
    while enemy_count > 0:
        enemy = Enemy(1000, 500, 0.3, 2, 100)
        enemy_group.add(enemy)
        enemy_count -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.speed_fwd = 1
        self.direction = 0
        self.flip = False
        player_img = pygame.image.load('assets/player/player_ship.png').convert_alpha()
        self.image = pygame.transform.scale(player_img, (int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.death_explosion = pygame.mixer.Sound('assets/player/large-underwater-explosion-short.wav')
        self.death_img = pygame.image.load('assets/player/exp2_0_new.png').convert_alpha()
        self.death_img_size = self.death_img.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cooldown = 0
        self.move_cooldown = 0
        self.health = health
        self.hit_count = 0
        self.animation_time = 0.01
        self.current_time = 0
        self.cell_pos = 0
        self.enemy_move_time = 3


    def enemy_move(self):
        dx = 0.0
        dy = 0.0

        enemy_move_left = False
        enemy_move_right = False
        enemy_move_fwd = False
        enemy_move_bwd = False

        # for player in players.player_group:
        #     if player.rect.centerx > self.rect.centerx:
        #         enemy_move_right = True
        #     if player.rect.centerx < self.rect.centerx:
        #         enemy_move_left = True
        #     if player.rect.centery > self.rect.centery:
        #         enemy_move_fwd = True
        #     if player.rect.centery < self.rect.centery:
        #         enemy_move_bwd = True

        if enemy_move_left:
            dx += self.accel
            if abs(dx) >= self.speed:
                dx = dx/abs(dx) * self.speed
        if enemy_move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if enemy_move_fwd:
            dy = self.speed
        if enemy_move_bwd:
            dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self, shoot):
        if shoot:
            if self.cooldown == 0:
                self.cooldown = 10
                bullet = projectiles.Laser(self.rect.centerx, self.rect.centery)
                projectiles.bullet_group.add(bullet)

    def update(self):
        # self.enemy_move()
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.health <= 0:
            self.enemy_death()
        if self.cell_pos >= 15:
            self.kill()
            self.remove()


    def enemy_death(self):
        x_cell = 4
        y_cell = 4
        cell_width = int(self.death_img_size[0] / x_cell)
        cell_height = int(self.death_img_size[1] / y_cell)

        cell_list = []

        if self.cell_pos == 0:
            self.death_explosion.set_volume(0.4)
            self.death_explosion.play()

        for y in range(0, self.death_img_size[1], cell_height):
            for x in range(0, self.death_img_size[0], cell_width):
                surface = pygame.Surface((cell_width, cell_height), pygame.SRCALPHA)
                surface.blit(self.death_img, (0, 0),
                             (x, y, cell_width, cell_height))
                cell_list.append(surface)

        self.current_time = 0
        screen.blit(cell_list[self.cell_pos], (self.rect.centerx - 32, self.rect.centery - 32))
        self.cell_pos = (self.cell_pos + 1) % len(cell_list)
        # explosion_rect = pygame.Rect(self.rect.centerx - 32, self.rect.centery - 32, cell_width, cell_height)
        # pygame.display.update(explosion_rect)
        print(self.cell_pos)

    def draw(self):
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)