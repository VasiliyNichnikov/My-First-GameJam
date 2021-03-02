from parameters import size_block
from image import load_image
from parameters import TypeBlock
import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, type_block, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Номер блока по оси x и y
        self.x = x
        self.y = y
        # Позиция блока по оси x и y
        self.pos_x = self.x * size_block
        self.pos_y = self.y * size_block
        # Тип блока
        self.type_block = type_block
        # Состояние ловушки
        self.hide = True
        # Скорость движения ловушки
        self.speed_traffic_trap = 0.3
        # Путь до папки где находятся блоки
        self.path_blocks = '../static/images/blocks_location/'
        # Словарь с путями блоков
        self.dict_paths_blocks = {
            TypeBlock.BLOCK_CENTER: 'block_center.png',
            TypeBlock.BLOCK_LEFT: 'block_left.png',
            TypeBlock.BLOCK_LEFT_UP: 'block_left_up.png',
            TypeBlock.BLOCK_RIGHT: 'block_right.png',
            TypeBlock.BLOCK_RIGHT_UP: 'block_right_up.png',
            TypeBlock.BLOCK_UP: 'block_up.png',
            TypeBlock.BLOCK_DOWN: 'block_down.png',
            TypeBlock.BLOCK_RIGHT_DOWN: 'block_right_down.png',
            TypeBlock.BLOCK_LEFT_DOWN: 'block_left_down.png',
            TypeBlock.BLOCK_TRAP: 'trap.png',
            TypeBlock.PORTAL_DOWN: 'portal_down.png',
            TypeBlock.PORTAL_UP: 'portal_up.png'
        }
        self.ready_path_block = self.path_blocks + self.dict_paths_blocks.get(self.type_block)
        self.image = load_image(self.ready_path_block, size_x=size_block, size_y=size_block)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, size_block, size_block)

    # Движение блока
    def move_block(self):
        if self.pos_y < self.y * size_block + size_block and self.hide:
            self.pos_y += self.speed_traffic_trap
        else:
            self.hide = False

        if self.pos_y > self.y * size_block and not self.hide:
            self.pos_y -= self.speed_traffic_trap
        else:
            self.hide = True


