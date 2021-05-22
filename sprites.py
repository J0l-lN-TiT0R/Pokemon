import pygame as p
from pygame.math import Vector2
from settings import *


class Spritesheet:
    def __init__(self, image_file, scale_factor=1):
        self.sheet = p.image.load(image_file).convert_alpha()
        if scale_factor != 1:
            self.size = self.sheet.get_rect().size
            self.target_size = tuple(i*scale_factor for i in self.size)
            self.sheet = p.transform.scale(self.sheet, self.target_size)

    def get_image(self, x, y, width, height):
        # image = p.Surface((width, height), p.SRCALPHA)
        # image.blit(self.sheet, (0, 0), (x, y, width, height))
        # Alternative:
        image = self.sheet.subsurface(x, y, width, height)
        return image


class Player(p.sprite.Sprite):
    def __init__(self, spritesheet, pos):
        super().__init__()

        self.image = spritesheet.get_image(0, 0, 64, 64)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.load_images(spritesheet)
        self.animation_cycle = self.walk_up_frames
        self.last_update = 0
        self.frame = 0
        self.velocity = Vector2(0, 0)

    def update(self):
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
        self.animate()

    def load_images(self, spritesheet):
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.walk_up_frames = []
        self.walk_down_frames = []

        for x in range(0, 192, 64):
            self.walk_down_frames.append(spritesheet.get_image(x, 0, 64, 64))
            self.walk_left_frames.append(spritesheet.get_image(x, 64, 64, 64))
            self.walk_right_frames.append(spritesheet.get_image(x, 128, 64, 64))
            self.walk_up_frames.append(spritesheet.get_image(x, 192, 64, 64))

    def animate(self):
        now = p.time.get_ticks()
        if now - self.last_update > 100:
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

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            self.image = self.animation_cycle[self.frame]
