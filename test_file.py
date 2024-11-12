# import sys
#
# import pygame
# from pygame.sprite import Sprite
#
#
# from screen_prop import screen
#
# img = pygame.image.load('assets/player/exp2_0.png')
# imageSize = img.get_size()
# x_cell = 4
# y_cell = 4
# cell_width = int(imageSize[0]/x_cell)
# cell_height = int(imageSize[1]/y_cell)
#
# cell_list = []
# cell_pos = 0
#
# clock=pygame.time.Clock()
# fps = 12
#
# for y in range(0, imageSize[1], cell_height):
#     for x in range(0, imageSize[0], cell_width):
#         surface = pygame.Surface((cell_width, cell_height))
#         surface.blit(img, (0, 0),
#                      (x, y, cell_width, cell_height))
#         cell_list.append(surface)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     if cell_pos < len(cell_list) - 1:
#         cell_pos += 1
#     else:
#         cell_pos = 0
#     screen.blit(cell_list[cell_pos], (300, 200))
#     pygame.display.update()
#     pygame.display.set_caption("Python - Pygame Simple SpriteSheet Animation")
#     clock.tick(fps)