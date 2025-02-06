import pygame.sprite
import pygame
import enemies
import screen_prop

#Group to house players
player_group = pygame.sprite.Group()
#Group to house player projectiles
player_bullet_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    """
    Player class that represents a player in the game
    Sets default values for players
    """
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
        self.accel = 0.0
        self.accel_y = 0.0
        self.decel = .95
        self.dx = 0.0
        self.dy = 0.0
        self.x_float = 0.0
        self.y_float = 0.0

    def move(self, move_left, move_right, move_fwd, move_bwd, speed_boost, time_delta):
        """
        Moves the player
        :param move_left: -0.5
        :param move_right: 0.5
        :param move_fwd: -0.5
        :param move_bwd: 0.5
        :param speed_boost: 10
        :param time_delta: unused
        """
        if move_left:
            self.accel = -0.5
        if move_right:
            self.accel = 0.5
        if move_fwd:
            self.accel_y = -0.5
        if move_bwd:
            self.accel_y = 0.5
        if speed_boost:
            self.speed = 10
        else:
            self.speed = 5

        self.dx += self.accel

        if abs(self.dx) >= self.max_speed:
            self.dx = self.dx / abs(self.dx) * self.max_speed

        self.dy += self.accel_y

        if abs(self.dy) >= self.max_speed:
            self.dy = self.dy / abs(self.dy) * self.max_speed

        if not move_left and not move_right:
            self.accel = 0

        if not move_fwd and not move_bwd:
            self.accel_y = 0

        if self.accel == 0:
            self.dx *= self.decel

        if self.accel_y == 0:
            self.dy *= self.decel

        #Truncates the floats for self.dx and self.dy into ints prior to assignment to the player's rect.x and rect.x
        # position. This prevents floating and short stopping depending on the direction of travel.
        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

    def shoot_laser(self, shoot):
        """
        shoots the laser
        :param shoot:
        """
        if shoot:
            if self.cooldown == 0:
                self.cooldown = 10
                bullet = Laser(self.rect.centerx, self.rect.centery)
                player_bullet_group.add(bullet)

    def shoot_missile(self, missile):
        """
        shoots the missile
        :param missile:
        """
        if missile:
            if self.cooldown == 0:
                self.cooldown = 20
                missile = Missile(self.rect.centerx, self.rect.centery)
                player_bullet_group.add(missile)

    def update(self):
        """
        Updates the player's movement and score on enemy hit
        """
        if self.cooldown > 0:
            self.cooldown -= 1
        for target in enemies.enemy_group:
            self.player_score = 10 * target.hit_count

    def draw(self):
        """
        Draws the player on screen
        """
        screen_prop.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Laser(pygame.sprite.Sprite):
    """
    Laser class that represents a laser in the game
    """
    def __init__(self, x, y):
        """
        Laser class that represents a laser in the game
        :param x:
        :param y:
        """
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
        """
        Updates the laser position
        Checks the laser position and checks it against the screen boundaries. Laser outside boundaries is killed.
        Checks the laser position and checks it against enemy rect, if inside enemy rect, decrements enemy health, kills the laser
        """
        self.rect.y -= self.speed
        if self.rect.top < screen_prop.SCREEN_HEIGHT - screen_prop.SCREEN_HEIGHT + 10:
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
    """
    Missile class that represents a missile in the game
    """
    def __init__(self, x, y):
        """
        Missile class that represents a missile in the game
        :param x:
        :param y:
        """
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
        """
        Updates the missile position
        Checks the missile position and checks it against the screen boundaries. Missile outside boundaries is killed.
        Checks the missile position and checks it against enemy rect, if inside enemy rect, decrements enemy health, kills the missile
        """
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




