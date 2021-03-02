from parameters import path_enemy_right, path_enemy_left, TypeBlock, SideSwordAndEnemy
from image import load_image
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, target):
        pygame.sprite.Sprite.__init__(self)
        self.__dict_images_right_left = {
            'right': load_image(path_enemy_right),
            'left': load_image(path_enemy_left)
        }
        self.image = self.__dict_images_right_left['right']
        self.rect = pygame.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())
        self.target = target
        self.select_side_number = 1
        self.enemy_speed = 2
        self.enemy_y_momentum = 0
        self.onGround = False
        self.enemy_movement = [0, 0]

    def select_side(self, position_enemy, position_player, collisions):
        x_enemy, y_enemy = position_enemy
        x_player, y_player = position_player

        dis_between_player_and_enemy_x = x_enemy - x_player
        dis_between_player_and_enemy_y = y_enemy - y_player

        if collisions['right'] or collisions['left'] or dis_between_player_and_enemy_y > 200:
            self.enemy_y_momentum = -4.5
            self.onGround = False

        if y_enemy != y_player or abs(dis_between_player_and_enemy_x) > 45:
            if dis_between_player_and_enemy_x > self.image.get_width():
                self.image = self.__dict_images_right_left['left']
                self.select_side_number = -1

            elif dis_between_player_and_enemy_x < -self.image.get_width():
                self.image = self.__dict_images_right_left['right']
                self.select_side_number = 1
        elif y_enemy == y_player and abs(dis_between_player_and_enemy_x) <= 45:
            self.select_side_number = 0
            self.target.game_over = True

    def move_enemy(self, list_blocks):
        self.enemy_movement = [0, 0]
        self.enemy_movement[1] += self.enemy_y_momentum * 2

        self.enemy_movement[0] += self.select_side_number * self.enemy_speed

        self.enemy_y_momentum += 0.2
        if self.enemy_y_momentum > 3:
            self.enemy_y_momentum = 3

        return self.__move(self.rect, list_blocks)

    def __collision(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append({'tile': tile, 'condition_block': tile.type_block})
        return hit_list

    def __move(self, rect, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += self.enemy_movement[0]
        dict_collision = self.__collision(rect, tiles)

        for block in dict_collision:
            tile = block['tile']
            condition_block = block['condition_block']
            if self.enemy_movement[0] > 0:
                if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                    rect.right = tile.rect.left
                    collision_types['right'] = True
            elif self.enemy_movement[0] < 0:
                if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                    rect.left = tile.rect.right
                    collision_types['left'] = True

        rect.y += self.enemy_movement[1]
        dict_collision = self.__collision(rect, tiles)
        for block in dict_collision:
            tile = block['tile']
            condition_block = block['condition_block']
            if self.enemy_movement[1] > 0:
                if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                    rect.bottom = tile.rect.top
                    collision_types['bottom'] = True
                    self.onGround = True
            elif self.enemy_movement[1] < 0:
                if condition_block not in [TypeBlock.BLOCK_TRAP, TypeBlock.PORTAL_UP, TypeBlock.PORTAL_DOWN]:
                    rect.top = tile.rect.bottom
                    collision_types['top'] = True
        return rect, collision_types

    def check_collisions(self, obj, scroll):
        if self.rect.topleft[0] - scroll[0] < obj[0] < self.rect.bottomright[0] - scroll[0] \
                and self.rect.topleft[1] - scroll[1] < obj[1] < self.rect.bottomright[1] - scroll[1]:
            return True
        return False

