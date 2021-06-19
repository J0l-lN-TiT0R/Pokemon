import pygame as p
from pygame.math import Vector2
from settings import *


class Spritesheet:
    def __init__(self, image_file, animation_len, scale_factor=1):
        """Load image_file into a self.sheet variable.
         
        Image will be scaled to the scale_factor if given.
        Otherwise it will be scaled to match the TILE_SIZE.
        """
        # Using convert_alpha() to make images blit faster on the screen
        self.sheet = p.image.load(image_file).convert_alpha()
        self.animation_len = animation_len
        self.size = Vector2(self.sheet.get_rect().size)
        sprite_size = self.size / animation_len
        if scale_factor != 1:
            ratio = scale_factor
        else:
            ratio = TILE_SIZE / sprite_size.x

        target_size = self.size * ratio
        self.sprite_size = sprite_size * ratio
        self.sheet = p.transform.scale(self.sheet, (int(target_size.x),
                                                    int(target_size.y)))
        self.size = Vector2(self.sheet.get_rect().size)
        

    def get_image(self, x, y, width, height):
        """Return an image cut out from the spritesheet."""
        image = self.sheet.subsurface(x, y, width, height)
        return image


class Player(p.sprite.Sprite):
    def __init__(self, game, sheet, pos):
        """Initialize required variables and load images."""
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)

        self.image = sheet.get_image(0, 0, *sheet.sprite_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self._load_images(sheet)
        self.animation_cycle = self.walk_up_frames
        self.last_update = 0
        self.frame = 0
        self.velocity = Vector2(0, 0)

    def update(self):
        """Move and animate the player."""
        self._move()
        self._animate()

    def _move(self):
        """Move the object based on the current input."""
        self.velocity = Vector2(0, 0)
        keys = p.key.get_pressed()
        if keys[p.K_w]:
            self.velocity.y = -1
        elif keys[p.K_s]:
            self.velocity.y = 1
        elif keys[p.K_a]:
            self.velocity.x = -1
        elif keys[p.K_d]:
            self.velocity.x = 1
        self.rect.center += self.velocity * PLAYER_SPEED * self.game.dt

    def _load_images(self, sheet):
        """Load animations from sheet into separate lists."""
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.walk_up_frames = []
        self.walk_down_frames = []

        w, h = sheet.sprite_size
        for x in range(0, int(sheet.size.x), int(sheet.sprite_size.x)):
            self.walk_down_frames.append(sheet.get_image(x, 0, w, h))
            self.walk_left_frames.append(sheet.get_image(x, h*1, w, h))
            self.walk_right_frames.append(sheet.get_image(x, h*2, w, h))
            self.walk_up_frames.append(sheet.get_image(x, h*3, w, h))

    def _animate(self, frame_length=100):
        """Go to the next frame of animation.

        Set animation cycle based on the current velocity vector.
        Go to the next frame if more time has passed in ms
        than specified in frame_length parameter.
        """
        now = p.time.get_ticks()
        if now - self.last_update > frame_length * self.game.dt * FPS:
            self.last_update = now

            if self.velocity == Vector2(0, 0):
                self.frame = -1
            elif self.velocity.y > 0:
                self.animation_cycle = self.walk_down_frames
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_left_frames
            elif self.velocity.x > 0:
                self.animation_cycle = self.walk_right_frames
            elif self.velocity.y < 0:
                self.animation_cycle = self.walk_up_frames

            # Cycling through frames and restraining ourselves
            # by the size of the current animation
            self.frame = (self.frame + 1) % len(self.animation_cycle)
            self.image = self.animation_cycle[self.frame]
