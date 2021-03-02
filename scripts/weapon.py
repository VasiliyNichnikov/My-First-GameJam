from parameters import path_sword_right, path_sword_left, SideSwordAndEnemy
from image import load_image
import math
import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)

        self.dict_images_right_left = {
            'right': load_image(path_sword_right),
            'left': load_image(path_sword_left)
        }
        self.side_sword = SideSwordAndEnemy.RIGHT
        # Атакует игрок или нет
        self.attack = False
        self.image = self.dict_images_right_left['right']
        self.surface = surface
        self.rect = pygame.Rect(5, 0, self.image.get_width(), self.image.get_height())
        self.__pos_x_max = 5
        self.__pos_x_min = -10
        self.position_start = (0, 0)
        self.speed_move_sword = 2.5

    def animation_weapon(self):
        if self.side_sword == SideSwordAndEnemy.LEFT:
            # Левая сторона
            if self.attack:
                if self.rect.x < self.__pos_x_max - self.__pos_x_min:
                    self.rect.x += self.speed_move_sword
                else:
                    self.attack = False
            else:
                if self.rect.x > self.__pos_x_max:
                    self.rect.x -= self.speed_move_sword
        else:
            # Правая сторона
            if self.attack:
                if self.rect.x > self.__pos_x_min:
                    self.rect.x -= self.speed_move_sword
                else:
                    self.attack = False
            else:
                if self.rect.x < self.__pos_x_max:
                    self.rect.x += self.speed_move_sword

    def draw_sword(self, pos):
        self.surface.blit(self.image, pos)
