import pygame
import players
import screen_prop
import enemies
import pygame_gui

pygame.init()

screen = pygame.display.set_mode((screen_prop.SCREEN_WIDTH, screen_prop.SCREEN_HEIGHT))

pygame.display.set_caption('Asteroid')

ui_manager = pygame_gui.UIManager((screen_prop.SCREEN_WIDTH, screen_prop.SCREEN_HEIGHT))

# framerate
clock = pygame.time.Clock()
FPS = 60

# define actions
move_left = False
move_right = False
move_fwd = False
move_bwd = False
speed_boost = False
laser = False
missile = False

# BG colors
BG = (0, 0, 0)

def draw_bg():
    screen.fill(BG)

player = players.Player(500, 200, 0.3, 7, "Player 1")
players.player_group.add(player)

enemies.spawn_enemy(1)

run = True
while run:

    time_delta = clock.tick(FPS)/1000
    draw_bg()
    mouse_pos = pygame.mouse.get_pos()
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    player.shoot_laser(laser)
    player.shoot_missile(missile)
    player.draw()
    player.move(move_left, move_right, move_fwd, move_bwd, speed_boost, time_delta)
    player.update(mouse_pos)

    # score_box = pygame_gui.elements.UITextBox(f"{player.player_name} | Speed: "
    #                                           f"<font size=25>{player.player_score}</font>",
    #                                           relative_rect=pygame.Rect((40, 900), (200, 35)))

    diag_box = pygame_gui.elements.UITextBox(f"{player.player_name} | x: "
                                             f"<font size=25>{round(player.rect.centerx,2)}</font> | y:" 
                                             f"<font size=25>{round(player.rect.centery),2}</font> | dx:"
                                             f"<font size=25>{round(player.dx,2)}</font> | dy:"
                                             f"<font size=25>{round(player.dy,2)}</font> | accel:"
                                             f"<font size=25>{round(player.accel,2)}</font>",
                                             relative_rect=pygame.Rect((40, 900), (500, 35)))
    players.player_bullet_group.update()
    players.player_bullet_group.draw(screen)

    enemies.enemy_group.draw(screen)
    enemies.enemy_group.update(time_delta)

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
                laser = True
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
                laser = False

    pygame.display.update()

pygame.quit()
