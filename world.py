import csv
import pygame as p
from settings import *


# TODO: change image_list to list?


class Tile(p.sprite.Sprite):
    def __init__(self, game, x, y, image, is_wall=False):
        """Assign image and set the position of the top left corner."""
        if is_wall:
            self.groups = game.all_sprites, game.walls
        else:
            self.groups = game.all_sprites
        self._layer = GROUND_LAYER
        super().__init__(self.groups)
        self.image = image
        # self.rect = self.image.get_rect(size=(TILE_SIZE//2, TILE_SIZE//2))
        self.rect = self.image.get_rect().inflate((-TILE_SIZE//3, -TILE_SIZE//3))
        # p.draw.rect(self.image, p.Color('darkgreen'), self.rect)
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class TileMap:
    def __init__(self, game, csv_file, image_file, tile_size, spacing=0):
        """Initialize required variables."""
        self.game = game
        self.csv_file = csv_file
        self.image_file = image_file
        self.tile_size = tile_size
        self.spacing = spacing
        self._load_map()

    def _csv_to_list(self, csv_file):
        """Return a 2D list made from data inside a csv file."""
        map_list = []
        with open(self.csv_file) as f:
            data = csv.reader(f, delimiter=',')
            for row in data:
                map_list.append(row) 
        return map_list

    def _parse_image(self):
        """Return a dictionary with index/surface pairs.

        Also scale surface tiles to the TILE_SIZE."""
        image_list = []
        image = p.image.load(self.image_file)
        # Scaling the whole tileset
        if self.tile_size != TILE_SIZE:
            ratio = int(TILE_SIZE / self.tile_size)
            assert ratio == int(ratio)
            spacing = self.spacing * ratio
            current_size = image.get_rect().size
            target_size = tuple(i * ratio for i in current_size)
            image = p.transform.scale(image, target_size)

        width = image.get_width()
        height = image.get_height()
        index = 0
        for y in range(0, height, TILE_SIZE + self.spacing):
            for x in range(0, width, TILE_SIZE + self.spacing):
                tile = image.subsurface(x, y, TILE_SIZE, TILE_SIZE)
                image_list.append(tile)
                index += 1
        return image_list
    
    def _load_tiles(self, map_list, image_list):
        """Load tile images to the group passed to the class."""
        for i, row in enumerate(map_list):
            for j, index in enumerate(row):
                if int(index) in WALL_LIST:
                    Tile(self.game, j, i, image_list[int(index)],
                         is_wall=True)
                else:
                    Tile(self.game, j, i, image_list[int(index)],
                         is_wall=False)
        
    def _load_map(self):
        """Call class methods to generate the final map."""
        map_list = self._csv_to_list(self.csv_file)
        image_list = self._parse_image()
        tiles = self._load_tiles(map_list, image_list)
        # Getting map size which camera object will use
        self.width = len(map_list[0]) * TILE_SIZE
        self.height = len(map_list) * TILE_SIZE


class Camera:
    def __init__(self, map_width, map_height):
        """Initialize the offset and map size variables."""
        self.offset = (0, 0)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        """Return the offset to which the entity should be shifted."""
        return entity.rect.move(self.offset)
    
    def update(self, target):
        """Calculate the offset of the map in relation to target."""
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2
        # Camera constrains
        x = min(x, 0)   # Left
        y = min(y, 0)   # Top
        x = max(x, -self.map_width + SCREEN_WIDTH)      # Right
        y = max(y, -self.map_height + SCREEN_HEIGHT)    # Bottom
        self.offset = (x, y)
