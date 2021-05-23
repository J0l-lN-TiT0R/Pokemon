import pygame as p
import sprites as s
from settings import *


p.init()
clock = p.time.Clock()

screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption(GAME_TITLE)
p.display.set_icon(p.image.load("images/froggy.png"))

player = s.Player(s.Spritesheet('images/sheet.png', 2), (100, 100))
player_group = p.sprite.GroupSingle()
player_group.add(player)

map_group = p.sprite.Group()

tile_map = s.TileMap(map_group, 'map.csv', 'images/rpg_tileset.png', 16)
tile_map.load_map()

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYUP 
                                    and event.key == p.K_q):
            running = False

    screen.fill(WHITE)

    map_group.draw(screen)
    player_group.draw(screen)
    player.update()

    p.display.flip()
    clock.tick(FPS)
