import pygame as p


class Spritesheet:
    def __init__(self, file):
        self.sheet = p.image.load(file)

    def get_image(self, x, y, width, height):
        image = p.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image


class Player(p.sprite.Sprite):
    def __init__(self, spritesheet, pos):
        super().__init__()

        self.image = spritesheet.get_image(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        keys = p.key.get_pressed()
        if keys[p.K_w]:
            self.rect.y -= 5
        if keys[p.K_s]:
            self.rect.y += 5
        if keys[p.K_a]:
            self.rect.x -= 5
        if keys[p.K_d]:
            self.rect.x += 5
