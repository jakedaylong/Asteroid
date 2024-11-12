import pygame
import projectiles
import screen_prop
from screen_prop import screen

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
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cooldown = 0
        self.health = health


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

    def enemy_death(self):
        death_img = pygame.image.load('assets/player/exp2_0.png')
        image_size = death_img.get_size()
        x_cell = 4
        y_cell = 4
        cell_width = int(image_size[0] / x_cell)
        cell_height = int(image_size[1] / y_cell)

        cell_list = []
        cell_pos = 0

        for y in range(0, image_size[1], cell_height):
            for x in range(0, image_size[0], cell_width):
                surface = pygame.Surface((cell_width, cell_height))
                surface.blit(death_img, (0, 0),
                             (x, y, cell_width, cell_height))
                cell_list.append(surface)

        while cell_pos < len(cell_list) - 1:
            screen.blit(cell_list[cell_pos], (self.rect.centerx - 32, self.rect.centery - 32))
            cell_pos += 1
            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(12)


    def draw(self):
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)