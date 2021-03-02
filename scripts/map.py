from parameters import TypeBlock
from block import Block
import random
from enemy import Enemy


class Map:
    def __init__(self, surface, file_map, player):
        self.surface = surface
        self.file_map = file_map
        self.player = player
        self.list_enemies = []
        self.list_blocks = []
        self.list_traps_underground = []
        self.list_blocks_portal = []
        self.__conversion_file_to_blocks()
        self.timer = 100
        self.save_timer = self.timer
        self.step = 5
        self.min_timer = 50

    def __conversion_file_to_blocks(self):
        with open(self.file_map, 'r', encoding='utf-8') as file_read:
            lines = file_read.readlines()
            for y in range(len(lines)):
                for x in range(len(lines[y])):
                    type_block = None
                    symbol = lines[y][x].lower()
                    # Блок UP
                    if symbol == 'u':
                        type_block = TypeBlock.BLOCK_UP
                    # Блок RIGHT
                    elif symbol == 'r':
                        type_block = TypeBlock.BLOCK_RIGHT
                    # Блок LEFT
                    elif symbol == 'l':
                        type_block = TypeBlock.BLOCK_LEFT
                    # Блок RIGHT UP
                    elif symbol == '-':
                        type_block = TypeBlock.BLOCK_RIGHT_UP
                    # Блок LEFT UP
                    elif symbol == '+':
                        type_block = TypeBlock.BLOCK_LEFT_UP
                    # Блок BLOCK CENTER
                    elif symbol == '#':
                        type_block = TypeBlock.BLOCK_CENTER
                    # Блок BLOCK DOWN
                    elif symbol == 'd':
                        type_block = TypeBlock.BLOCK_DOWN
                    # Блок BLOCK RIGHT DOWN
                    elif symbol == '}':
                        type_block = TypeBlock.BLOCK_RIGHT_DOWN
                    # Блок BLOCK LEFT DOWN
                    elif symbol == '{':
                        type_block = TypeBlock.BLOCK_LEFT_DOWN
                    # Ловушка
                    elif symbol == 't':
                        type_block = TypeBlock.BLOCK_TRAP
                    # Верхняя часть портала
                    elif symbol == '^':
                        type_block = TypeBlock.PORTAL_UP
                    # Нижняя часть портала
                    elif symbol == '?':
                        type_block = TypeBlock.PORTAL_DOWN

                    if type_block is not None:
                        block = Block(type_block, x=x, y=y)
                        if block.type_block == TypeBlock.BLOCK_TRAP:
                            self.list_traps_underground.append(block)
                        elif block.type_block == TypeBlock.PORTAL_UP:
                            self.list_blocks_portal.append(block)
                        self.list_blocks.append(block)

    # Отрисовка карты
    def draw_map(self, scroll):
        for block in self.list_traps_underground:
            block.move_block()
        if self.timer_create_enemy():
            self.create_enemies()
        for block in self.list_blocks:
            self.surface.blit(block.image, (block.pos_x - scroll[0], block.pos_y - scroll[1]))

    # Таймер создания врагов
    def timer_create_enemy(self):
        self.timer -= 0.5
        if self.timer <= 0:
            if self.save_timer - self.step >= self.min_timer:
                self.save_timer -= self.step
            self.timer = self.save_timer
            return True
        return False

    # Создание врага
    def create_enemies(self):
        for i in range(2):
            number = random.randint(0, len(self.list_blocks_portal) - 1)
            position = self.list_blocks_portal[number]
            new_enemy = Enemy((position.pos_x, position.pos_y), self.player)
            self.list_enemies.append(new_enemy)
