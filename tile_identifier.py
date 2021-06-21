import pygame as p
import pygame.freetype


pygame.init()
screen = p.display.set_mode((544, 256))

font = pygame.freetype.Font(None, 16)
image = p.image.load("map/rpg_tileset.png")
image = p.transform.scale(image, (544, 256))
index = 0
for y in range(0, 256, 32):
    for x in range(0, 544, 32):
        font.render_to(image, (x+10, y+10), str(index), (0, 0, 0))
        index += 1

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN
                                    and event.key == p.K_ESCAPE):
            running = False
    screen.blit(image, (0, 0))
    p.display.flip()
