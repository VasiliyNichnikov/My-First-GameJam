from enum import Enum


w, h = 1000, 600
BACKGROUND_COLOR = (189, 147, 84)
FPS = 60
size_block = w // 20
# Гравитация
GRAVITY = 3.5
# Сила прыжка
FORCE_JUMP = 10

# Путь изображения игрока справа
path_player_right = '../static/images/player_right.png'
# Путь изображения игрока слева
path_player_left = '../static/images/player_left.png'
# Путь тестовой карты
path_map_test = '../static/map_locations/map_test.txt'
# Путь до ловушки
path_trap = '../static/images/trap.png'
# Путь до врага (справа)
path_enemy_right = '../static/images/enemy_right.png'
# Путь до врага (слева)
path_enemy_left = '../static/images/enemy_left.png'
# Путь до спрайта пули
path_bullet = '../static/images/bullet.png'
# Путь до спрайта меча (справа)
path_sword_right = '../static/images/sword_right.png'
# Путь до спрайта меча (слева)
path_sword_left = '../static/images/sword_left.png'
# Путь до шрифта
path_font = '../static/fonts/prstart.ttf'
# Путь до нажатой кнопки
path_button_down = '../static/images/buttons/button_down.png'
# Путь до опущенной кнопки
path_button_up = '../static/images/buttons/button_up.png'



# Типы блоков
class TypeBlock(Enum):
    BLOCK_CENTER = 0
    BLOCK_LEFT = 1
    BLOCK_LEFT_UP = 2
    BLOCK_RIGHT = 3
    BLOCK_RIGHT_UP = 4
    BLOCK_UP = 5
    BLOCK_DOWN = 6
    BLOCK_LEFT_DOWN = 7
    BLOCK_RIGHT_DOWN = 8
    BLOCK_TRAP = 9
    PORTAL_UP = 10
    PORTAL_DOWN = 11


# Сторона меча
class SideSwordAndEnemy(Enum):
    RIGHT = 0
    LEFT = 1


# Сторона с которой находится блок, относительно игрока
class SideBlock(Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    UP = 4
