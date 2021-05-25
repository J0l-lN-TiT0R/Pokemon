import pygame as p
import sprites as s
from settings import *


class Game:
    def __init__(self):
        p.init()
        self.clock = p.time.Clock()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = False
        p.display.set_caption(GAME_TITLE)
        p.display.set_icon(p.image.load("images/froggy.png"))
    
    def new(self):
        self.all_sprites = p.sprite.LayeredUpdates()
        self.player = s.Player(self, s.Spritesheet('images/sheet.png', 2),
                               (100, 100))
        self.tile_map = s.TileMap(self, 'map.csv', 
                                  'images/rpg_tileset.png', 16)
        self.tile_map.load_map()

    def events(self):
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYUP 
                                        and event.key == p.K_q):
                self.running = False
    
    def update(self):
        self.all_sprites.update()
        self.clock.tick(FPS)
        p.display.flip()

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

    def run(self):
        self.running = True 
        while self.running:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
