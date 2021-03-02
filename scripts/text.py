import pygame


def get_text(path_font, size_font, color_text, text):
    font = pygame.font.Font(path_font, size_font)
    res_text = font.render(text, True, color_text)
    return res_text
