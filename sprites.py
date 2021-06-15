import pygame as p
from pygame.math import Vector2
from settings import *


class Spritesheet:
    def __init__(self, image_file, scale_factor=1):
        """Load image_file into a self.sheet variable.
         
        Scale it by scale_factor.
        """
        # Using convert_alpha() to make images blit faster on the screen
        self.sheet = p.image.load(image_file).convert_alpha()
        if scale_factor != 1:
            self.size = self.sheet.get_rect().size
            self.target_size = tuple(i*scale_factor for i in self.size)
            self.sheet = p.transform.scale(self.sheet, self.target_size)

    def get_image(self, x, y, width, height):
        """Return an image cut out from the object spritesheet"""
        image = self.sheet.subsurface(x, y, width, height)
        return image


class Player(p.sprite.Sprite):
    def __init__(self, game, spritesheet, pos):
        """Initialize required variables and load images."""
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)

        self.image = spritesheet.get_image(0, 0, 64, 64)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self._load_images(spritesheet)
        self.animation_cycle = self.walk_up_frames
        self.last_update = 0
        self.frame = 0
        self.velocity = Vector2(0, 0)

    def update(self):
        """Move and animate the object."""
        self._move()
        self._animate()

    def _move(self):
        """Move the object based on the current input."""
        self.velocity = Vector2(0, 0)
        keys = p.key.get_pressed()
        if keys[p.K_w]:
            self.velocity.y = -1
        if keys[p.K_s]:
            self.velocity.y = 1
        if keys[p.K_a]:
            self.velocity.x = -1
        if keys[p.K_d]:
            self.velocity.x = 1
        self.rect.center += self.velocity * PLAYER_SPEED 

    def _load_images(self, spritesheet):
        """Load animations from spritesheet into separate lists."""
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.walk_up_frames = []
        self.walk_down_frames = []

        w, h = 64, 64
        for x in range(0, 256, 64):
            self.walk_down_frames.append(spritesheet.get_image(x, 0, w, h))
            self.walk_left_frames.append(spritesheet.get_image(x, 64, w, h))
            self.walk_right_frames.append(spritesheet.get_image(x, 128, w, h))
            self.walk_up_frames.append(spritesheet.get_image(x, 192, w, h))

    def _animate(self, frame_length=100):
        """Go to the next frame of animation.

        Set animation cycle based on the current velocity vector.
        Go to the next frame if more time has passed in ms
        than specified in frame_length parameter.
        """
        now = p.time.get_ticks()
        if now - self.last_update > frame_length:
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
