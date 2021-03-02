import pygame


# Загрузка изображений
def load_image(image, size_x=0, size_y=0):
    res_image = pygame.image.load(image)
    if size_x != 0 and size_y != 0:
        res_image = pygame.transform.scale(res_image, (size_x, size_y))
    return res_image
