import pygame
from image import load_image
from parameters import path_button_down, path_button_up


class Button(pygame.sprite.Sprite):
    def __init__(self, surface, pos_x, pos_y, height, width, color_btn=(0, 0, 0), text='None',
                 color_text=(255, 255, 255), path_font='None', size_font=30):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.__dict_select_btn = {'up': load_image(path_button_up),
                                  'down': load_image(path_button_down)}

        self.image = self.__dict_select_btn['up']

        self.height = height
        self.width = width
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        self.color_btn = color_btn
        self.text = text
        self.color_text = color_text
        self.path_font = path_font
        self.size_font = size_font
        self.input_btn = False

    def draw_button(self):
        if self.input_btn:
            self.image = self.__dict_select_btn['down']
            pos_text_y = 5
        else:
            self.image = self.__dict_select_btn['up']
            pos_text_y = -5
        self.surface.blit(self.image, (self.pos_x, self.pos_y, self.width, self.height))
        text_btn = self.__draw_text()
        self.surface.blit(text_btn, (
            self.pos_x + (self.width - text_btn.get_width()) // 2 + pos_text_y,
            self.pos_y + (self.height - text_btn.get_height()) // 2 + pos_text_y))

    def check_input_button(self, mouse, click=False):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1] and click:
            self.input_btn = True
        else:
            self.input_btn = False
        return self.input_btn

    def __draw_text(self):
        font = pygame.font.Font(self.path_font, self.size_font)
        text = font.render(self.text, True, self.color_text)
        return text
