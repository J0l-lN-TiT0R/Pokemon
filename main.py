import pygame as p
import sprites as s
from settings import *


p.init()
clock = p.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption(GAME_TITLE)
p.display.set_icon(p.image.load("images/froggy.png"))

player = s.Player(s.Spritesheet('images/sheet.png'),
                  (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
player_group = p.sprite.GroupSingle()
player_group.add(player)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    screen.fill(BLACK)

    player_group.draw(screen)
    player.update()

    p.display.flip()
    clock.tick(FPS)
