import pygame
import player

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Asteroid')

#framerate
clock = pygame.time.Clock()
FPS = 60

#define actions
move_left = False
move_right = False
move_fwd = False
move_bwd = False
speed_boost = False

#BG colors
BG = (0, 0, 0)

def draw_bg():
    screen.fill(BG)

player = player.Player(300, 300, 0.3, 5)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.draw()

    player.move(move_left, move_right, move_fwd, move_bwd, speed_boost)

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


    pygame.display.update()

pygame.quit()