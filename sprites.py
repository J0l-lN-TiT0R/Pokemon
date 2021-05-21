import pygame as p
from pygame.math import Vector2


class Spritesheet:
    def __init__(self, image_file):
        self.sheet = p.image.load(image_file).convert_alpha()

    def get_image(self, x, y, width, height):
        image = p.Surface((width, height), p.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image


class Player(p.sprite.Sprite):
    def __init__(self, spritesheet, pos):
        super().__init__()

        self.image = spritesheet.get_image(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.load_images(spritesheet)
        self.animation_cycle = self.walk_frames_up
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

        self.rect.center += self.velocity * 5
        self.animate()

    def load_images(self, spritesheet):
        self.walk_frames_right = []
        self.walk_frames_left = []
        self.walk_frames_up = []
        self.walk_frames_down = []

        x = 0
        for _ in range(4):
            self.walk_frames_down.append(spritesheet.get_image(x, 0, 32, 32))
            self.walk_frames_left.append(spritesheet.get_image(x, 32, 32, 32))
            self.walk_frames_right.append(spritesheet.get_image(x, 64, 32, 32))
            self.walk_frames_up.append(spritesheet.get_image(x, 96, 32, 32))
            x += 32

    def animate(self):
        now = p.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now

            if self.velocity == Vector2(0, 0):
                self.frame = -1
            elif self.velocity.y > 0:
                self.animation_cycle = self.walk_frames_down
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_frames_left
            elif self.velocity.x > 0:
                self.animation_cycle = self.walk_frames_right
            elif self.velocity.y < 0:
                self.animation_cycle = self.walk_frames_up

            self.frame = (self.frame + 1) % len(self.animation_cycle)
            self.image = self.animation_cycle[self.frame]
