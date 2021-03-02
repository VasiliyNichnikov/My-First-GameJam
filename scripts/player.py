from image import load_image
from parameters import path_player_right, path_player_left
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Скорость по оси X
        self.__speed_player_x = 5
        # Скорость по оси Y
        self.__speed_player_y = 2
        # Скорость движения игрока
        self.speed_player = 5
        # Словарь с двумя состояниями игрока
        self.dict_right_left = {
            'right': load_image(path_player_right),
            'left': load_image(path_player_left)
        }

        # Загрузка изображения игрока
        self.image = self.dict_right_left['right']
        # Блокировка вправо
        self.lock_right = False
        # Блокировка влево
        self.lock_left = False
        self.rect = self.image.get_rect()
        # В какую сторону двигается персонаж
        self.right_moving = False
        self.left_moving = False
        # Находится ли игрока на земле или нет
        self.onGround = False
        # Поражение
        self.game_over = False

