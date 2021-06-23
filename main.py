import pygame as p
import pygame.freetype
import sprites as sp
import world
from battle_screen import BattleScreen
from settings import *


class Game:
    def __init__(self):
        """Create the game window."""
        p.init()
        self.clock = p.time.Clock()
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = False
        self.state = 'in_battle'
        p.display.set_caption(GAME_TITLE)
        p.display.set_icon(p.image.load("images/froggy.png"))
    
    def new(self):
        """Initialize sprites and load the game map."""
        self.main_font = p.freetype.Font(None, 24)
        self.all_sprites = p.sprite.LayeredUpdates()
        self.battle_screen = BattleScreen(self.screen, self.main_font)
        self.walls = p.sprite.Group()
        self.player = sp.Player(self, sp.Spritesheet('images/sheet.png', 4),
                                (100, 100))
        self.tile_map = world.TileMap(self, 'map/map.csv', 
                                  'map/rpg_tileset.png', 16)
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

    def _draw(self):
        """Draw all the sprites on the screen."""
        if self.state == 'walking':
            self.screen.fill(WHITE)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        elif self.state == 'in_battle':
            self.battle_screen.draw()
        p.display.flip()

    def run(self):
        """The game loop."""
        self.running = True 
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self._events()
            self._update()
            self._draw()


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
