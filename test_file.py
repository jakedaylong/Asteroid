import pygame
import pygame_gui


pygame.init()
display = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
GRAY = pygame.Color('gray12')
display_width, display_height = display.get_size()
x = display_width * 0.45
y = display_height * 0.8
x_change = 0
accel_x = 0
max_speed = 6
ui_manager = pygame_gui.UIManager((display_width, display_height))



crashed = False
while not crashed:
    diag_box = pygame_gui.elements.UITextBox(f"x: "
                                             f"<font size=25>{round(x, 2)}</font> | y:"
                                             f"<font size=25>{round(y), 2}</font> | dx:"
                                             f"<font size=25>{round(x_change, 2)}</font> | dy:"
                                             f"accel:"
                                             f"<font size=25>{round(accel_x, 2)}</font>",
                                             relative_rect=pygame.Rect((40, 150), (400, 35)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                crashed = True
        elif event.type == pygame.KEYDOWN:
            # Set the acceleration value.
            if event.key == pygame.K_LEFT:
                accel_x = -.2
            elif event.key == pygame.K_RIGHT:
                accel_x = .2
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                accel_x = 0

    x_change += accel_x  # Accelerate.
    if abs(x_change) >= max_speed:  # If max_speed is exceeded.
        # Normalize the x_change and multiply it with the max_speed.
        x_change = x_change/abs(x_change) * max_speed

    # Decelerate if no key is pressed.
    if accel_x == 0:
        x_change *= 0.92

    x += x_change  # Move the object.

    display.fill(GRAY)
    pygame.draw.rect(display, (0, 120, 250), (x, y, 20, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()