import pygame as p
from settings import *


class BattleScreen:
    def __init__(self, dest_surf, font):
        self.dest_surf = dest_surf
        self.font = font
        self.active_buttons = p.sprite.Group()
        self.inactive_buttons = p.sprite.Group()
        self.background = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(BG_COLOR)
        self.actions_box = Container((SCREEN_WIDTH*(2/3), SCREEN_HEIGHT*(3/4)),
                                     (SCREEN_WIDTH/3-10, SCREEN_HEIGHT/4-10),
                                     WHITE, self.font)
        self.output_box = Container((10, SCREEN_HEIGHT*(3/4)),
                                    (SCREEN_WIDTH*(2/3)-20, SCREEN_HEIGHT/4-10),
                                    WHITE, self.font)
        self.fight_button = Button(self, self.actions_box, 'top-left', 'FIGHT')
        self.pok_button = Button(self, self.actions_box, 'bottom-left', 'POK')
        self.bag_button = Button(self, self.actions_box, 'top-right', 'BAG')
        self.run_button = Button(self, self.actions_box, 'bottom-right', 'RUN')
        self._setup()

    
    def draw(self):
        self.dest_surf.blit(self.background, (0, 0))
        # Drawing containers
        self.actions_box.draw(self.dest_surf)
        self.output_box.draw(self.dest_surf)
        # Drawing buttons
        self.active_buttons.draw(self.dest_surf)

    def _activate_buttons(self, *buttons):
        for button in buttons:
            button.remove(self.inactive_buttons)
            button.add(self.active_buttons)

    def _deactivate_buttons(self, *buttons):
        for button in buttons:
            button.remove(self.active_buttons)
            button.add(self.inactive_buttons)

    def _setup(self):
        self._activate_buttons(self.fight_button, self.bag_button,
                               self.pok_button, self.run_button)


    def process_input(self, event):
        for button in self.active_buttons:
            if button.rect.collidepoint(event.pos):
                self._deactivate_buttons(button)


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


class Button(p.sprite.Sprite):
    def __init__(self, battle_screen, container, corner, text):
        super().__init__(battle_screen.inactive_buttons)
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
        self.image = p.Surface(size, p.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=pos)
        container.font.render_to(self.image, (40, 30), text)
