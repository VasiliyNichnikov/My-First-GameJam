from parameters import w, h, BACKGROUND_COLOR, FPS, path_map_test, SideBlock, TypeBlock, SideSwordAndEnemy, path_font
from text import get_text
from weapon import Weapon
from player import Player
from button import Button
from map import Map
import pygame
import sys

runner = True
pygame.init()
pygame.display.set_caption('Game Jam 1')
clock = pygame.time.Clock()
surface = pygame.display.set_mode((w, h))
surface.fill(BACKGROUND_COLOR)

# Создание игрока
player = Player()
player_rect = player.rect
player_rect.x, player_rect.y = w // 2, h // 2
# Создание оружия у игрока
weapon = Weapon(surface)
# Создание карты
map_test = Map(surface, path_map_test, player)
# Движение игрока по оси y
player_y_momentum = 0
# Создание камеры
scroll = [0, 0]
# Цвет текста
COLOR_NAME_GAME_TEXT = (73, 33, 3)
# Цвет рекорда
COLOR_SCORE = (0, 0, 10)
# Рекорд
score = 0
# кнопка начала игры
start_button = Button(surface, w // 2 - 75, h // 2 - 50, 100, 150, text='Start', path_font=path_font, size_font=10)
# запущена игра или нет
start_game = False


# Проверка с какой стороны от игрока находится блок, до которого игрок дотронулся
def check_block_touched_player(list_blocks_touched):
    lock_left, lock_right = False, False
    for block in list_blocks_touched:
        condition_left_right = SideBlock.NONE
        condition_up_down = SideBlock.NONE

        x_pl_center, y_pl_center = player.rect.center

        if block.rect.x < x_pl_center:
            condition_left_right = SideBlock.LEFT

        elif block.rect.x > x_pl_center:
            condition_left_right = SideBlock.RIGHT

        if block.rect.y < y_pl_center:
            condition_up_down = SideBlock.UP

        elif block.rect.y > y_pl_center:
            condition_up_down = SideBlock.DOWN

        if condition_up_down == SideBlock.UP:
            if condition_left_right == SideBlock.RIGHT:
                lock_right = True
            elif condition_left_right == SideBlock.LEFT:
                lock_left = True
            break
    player.lock_right = lock_right
    player.lock_left = lock_left


def collision(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append({'tile': tile, 'condition_block': tile.type_block})
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': {'condition': False, 'blocks': []},
                       'bottom': {'condition': False, 'blocks': []},
                       'right': {'condition': False, 'blocks': []},
                       'left': {'condition': False, 'blocks': []},
                       'trap': {'condition': False, 'blocks': []}}
    rect.x += movement[0]
    dict_collision = collision(rect, tiles)

    for block in dict_collision:
        tile = block['tile']
        condition_block = block['condition_block']
        if movement[0] > 0:
            if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                rect.right = tile.rect.left
                collision_types['right']['condition'] = True
            elif condition_block == TypeBlock.BLOCK_TRAP:
                collision_types['trap']['condition'] = True
                collision_types['trap']['blocks'].append(tile)
        elif movement[0] < 0:
            if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                rect.left = tile.rect.right
                collision_types['left']['condition'] = True
            elif condition_block == TypeBlock.BLOCK_TRAP:
                collision_types['trap']['condition'] = True
                collision_types['trap']['blocks'].append(tile)

    rect.y += movement[1]
    dict_collision = collision(rect, tiles)
    for block in dict_collision:
        tile = block['tile']
        condition_block = block['condition_block']
        if movement[1] > 0:
            if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                rect.bottom = tile.rect.top
                collision_types['bottom']['condition'] = True
            elif condition_block == TypeBlock.BLOCK_TRAP:
                collision_types['trap']['condition'] = True
                collision_types['trap']['blocks'].append(tile)
        elif movement[1] < 0:
            if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                rect.top = tile.rect.bottom
                collision_types['top']['condition'] = True
            elif condition_block == TypeBlock.BLOCK_TRAP:
                collision_types['trap']['condition'] = True
                collision_types['trap']['blocks'].append(tile)
    return rect, collision_types


# Перезагрузка игры
def reload_game():
    global player_y_momentum, scroll, player_rect, player, map_test, score
    player = Player()
    player_rect = player.rect
    player_rect.x, player_rect.y = w // 2, h // 2
    map_test = Map(surface, path_map_test, player)
    player_y_momentum = 0
    score = 0
    scroll = [0, 0]
    start_button.input_btn = False


while runner:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            runner = False

        if start_game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not weapon.attack:
                    weapon.attack = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.onGround is True:
                    player_y_momentum = -6
                    player.onGround = False
                if event.key == pygame.K_d:
                    player.image = player.dict_right_left['right']
                    weapon.side_sword = SideSwordAndEnemy.RIGHT
                    weapon.image = weapon.dict_images_right_left['right']
                    player.right_moving = True
                if event.key == pygame.K_a:
                    player.image = player.dict_right_left['left']
                    weapon.image = weapon.dict_images_right_left['left']
                    weapon.side_sword = SideSwordAndEnemy.LEFT
                    weapon.image = weapon.dict_images_right_left['left']
                    player.left_moving = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.right_moving = False
                if event.key == pygame.K_a:
                    player.left_moving = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_button.check_input_button(event.pos, click=True)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_button.check_input_button(event.pos, click=True):
                    start_game = True

    if start_game is False:
        # Отрисовка кнопки
        start_button.draw_button()
        name_game_text = get_text(path_font, 40, COLOR_NAME_GAME_TEXT, 'GameJam First')
        surface.blit(name_game_text, (w // 2 - name_game_text.get_width() // 2, name_game_text.get_height()))

    if start_game:
        # Отрисовка рекорда
        score_text = get_text(path_font, 15, COLOR_SCORE, f'score {score}')
        surface.blit(score_text, (w - score_text.get_width() - 10, score_text.get_height()))

        scroll[0] += (player_rect.x - scroll[0] - 300) / 10
        scroll[1] += (player_rect.y - scroll[1] - 400) / 10

        if player_rect.y > h:
            player.game_over = True

        player_movement = [0, 0]
        if player.right_moving:
            player_movement[0] += 1 * player.speed_player
        if player.left_moving:
            player_movement[0] -= 1 * player.speed_player

        player_movement[1] += player_y_momentum * 2
        player_y_momentum += 0.2
        if player_y_momentum > 3:
            player_y_momentum = 3

        player_rect, collisions = move(player_rect, player_movement, map_test.list_blocks)
        if collisions['trap']['condition'] and len(collisions['trap']['blocks']) != 0:
            trap_blocks = collisions['trap']['blocks']
            if trap_blocks[0].hide is False:
                player.game_over = True

        if collisions['bottom']['condition']:
            player.onGround = True
            player_y_momentum = 0

        # Отрисовка карты
        map_test.draw_map(scroll)

        # Отрисовка врагов
        for enemy in map_test.list_enemies:
            if weapon.attack and enemy.check_collisions(weapon.position_start, scroll):
                map_test.list_enemies.remove(enemy)
                score += 1
                break

            enemy_rect, collisions_enemy = enemy.move_enemy(map_test.list_blocks)

            enemy.select_side(position_enemy=(enemy_rect.x - scroll[0], enemy_rect.y - scroll[1]),
                              position_player=(player_rect.x - scroll[0], player_rect.y - scroll[1]),
                              collisions=collisions_enemy)

            surface.blit(enemy.image, (enemy_rect.x - scroll[0], enemy_rect.y - scroll[1]))
        # Отрисовка игрока
        surface.blit(player.image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        # Отрисовка оружия
        weapon.animation_weapon()

        if weapon.side_sword == SideSwordAndEnemy.RIGHT:
            weapon.draw_sword((player_rect.x - scroll[0] - weapon.rect.x, player_rect.y - scroll[1] + 35))
            weapon.position_start = (player_rect.x - scroll[0] - weapon.rect.x + weapon.image.get_width(),
                                     player_rect.y - scroll[1] + 35 + weapon.image.get_height() // 2)
        else:
            weapon.draw_sword(
                (player_rect.x - scroll[0] - weapon.rect.x - weapon.image.get_width() // 2, player_rect.y - scroll[1] + 35))
            weapon.position_start = (player_rect.x - scroll[0] - weapon.rect.x - weapon.image.get_width() // 2,
                                     player_rect.y - scroll[1] + 35 + weapon.image.get_height() // 2)

    if player.game_over:
        start_game = False
        reload_game()

    clock.tick(FPS)
    pygame.display.update()
    surface.fill(BACKGROUND_COLOR)

pygame.quit()
sys.exit()
