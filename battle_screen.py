import pygame as p
from settings import *


class BattleScreen:
    def __init__(self, dest_surf, font):
        self.dest_surf = dest_surf
        self.font = font
        self.background = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(BG_COLOR)
        self.actions_box = Container((SCREEN_WIDTH*(2/3), SCREEN_HEIGHT*(3/4)),
                                     (SCREEN_WIDTH/3-10, SCREEN_HEIGHT/4-10),
                                     WHITE, self.font)
        self.output_box = Container((10, SCREEN_HEIGHT*(3/4)),
                                    (SCREEN_WIDTH*(2/3)-20, SCREEN_HEIGHT/4-10),
                                    WHITE, self.font)
        self.fight_button = Button(self.actions_box, 'top-left', 'FIGHT')
        self.pok_button = Button(self.actions_box, 'bottom-left', 'POK')
        self.bag_button = Button(self.actions_box, 'top-right', 'BAG')
        self.run_button = Button(self.actions_box, 'bottom-right', 'RUN')

    
    def draw(self):
        self.dest_surf.blit(self.background, (0, 0))
        # Drawing containers
        self.actions_box.draw(self.dest_surf)
        self.output_box.draw(self.dest_surf)
        # Drawing buttons
        self.fight_button.draw(self.dest_surf)
        self.pok_button.draw(self.dest_surf)
        self.bag_button.draw(self.dest_surf)
        self.run_button.draw(self.dest_surf)

    def process_input(self)


class Container(p.Rect):
    def __init__(self, pos, size, color, font,
                 border_width=10, border_radius=10):
        super().__init__(pos, size)
        self.font = font
        self.color = color
        self.border_width = border_width
        self.border_radius = border_radius

    def draw(self, dest_surf):
        p.draw.rect(dest_surf, self.color, self,
                    self.border_width, self.border_radius)


class Button:
    def __init__(self, container, corner, text):
        if corner == 'top-left':
            pos = container.topleft
        elif corner == 'top-right':
            pos = container.x + container.w/2, container.y
        elif corner == 'bottom-left':
            pos = container.x, container.y + container.h/2
        elif corner == 'bottom-right':
            pos = (container.x + container.w/2,
                   container.y + container.h/2)

        size = container.w//2, container.h//2
        self.surface = p.Surface(size, p.SRCALPHA, 32)
        self.rect = self.surface.get_rect(topleft=pos)
        container.font.render_to(self.surface, (40, 30), text)
    
    def draw(self, dest_surf):
        dest_surf.blit(self.surface, self.rect)
