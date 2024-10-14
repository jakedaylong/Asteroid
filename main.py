import pygame
import player
import screen_prop
import enemies
from random import randint

import projectiles

pygame.init()

screen = pygame.display.set_mode((screen_prop.SCREEN_WIDTH, screen_prop.SCREEN_HEIGHT))

pygame.display.set_caption('Asteroid')

# framerate
clock = pygame.time.Clock()
FPS = 60

# define actions
move_left = False
move_right = False
move_fwd = False
move_bwd = False
speed_boost = False
shooting = False
missile = False

# BG colors
BG = (0, 0, 0)


def draw_bg():
    screen.fill(BG)


player = player.Player(300, 300, 0.3, 5)
enemy = enemies.Enemy(1000, 500, 0.3, 3)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.draw()
    player.move(move_left, move_right, move_fwd, move_bwd, speed_boost)
    player.shoot_laser(shooting)
    player.shoot_missile(missile)
    player.update()

    enemy.draw()
    enemy.update()

    projectiles.bullet_group.update()
    projectiles.bullet_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_fwd = True
            if event.key == pygame.K_s:
                move_bwd = True
            if event.key == pygame.K_LSHIFT:
                speed_boost = True
            if event.key == pygame.K_SPACE:
                shooting = True
            if event.key == pygame.K_f:
                missile = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_fwd = False
            if event.key == pygame.K_s:
                move_bwd = False
            if event.key == pygame.K_LSHIFT:
                speed_boost = False
            if event.key == pygame.K_f:
                missile = False
            if event.key == pygame.K_SPACE:
                shooting = False

    pygame.display.update()

pygame.quit()
