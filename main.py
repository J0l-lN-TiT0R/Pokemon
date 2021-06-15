import pygame as p
import sprites as sp
import world
from settings import *


class Game:
    def __init__(self):
        """Create the game window."""
        p.init()
        self.clock = p.time.Clock()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = False
        p.display.set_caption(GAME_TITLE)
        p.display.set_icon(p.image.load("images/froggy.png"))
    
    def new(self):
        """Initialize sprites and load the game map."""
        self.all_sprites = p.sprite.LayeredUpdates()
        self.player = sp.Player(self, sp.Spritesheet('images/sheet.png', 2),
                               (100, 100))
        self.tile_map = world.TileMap(self, 'map.csv', 
                                  'images/rpg_tileset.png', 16)
        self.camera = world.Camera(self.tile_map.width, self.tile_map.height)

    def _events(self):
        """Check for input events."""
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYUP 
                                        and event.key == p.K_ESCAPE):
                self.running = False
    
    def _update(self):
        """Update the screen and all sprites on it."""
        self.all_sprites.update()
        self.camera.update(self.player)
        self.clock.tick(FPS)

    def _draw(self):
        """Draw all the sprites on the screen."""
        self.screen.fill(WHITE)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        p.display.flip()

    def run(self):
        """The game loop."""
        self.running = True 
        while self.running:
            self._events()
            self._update()
            self._draw()


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
