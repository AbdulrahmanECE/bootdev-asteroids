import random
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOR,
    BACKGROUND_STAR_COUNT,
    BACKGROUND_NEBULA_COUNT,
)

NEBULA_COLORS = [(90, 40, 140), (30, 70, 150), (130, 40, 100)]


def draw_nebula(background, width: int, height: int):
    # A soft glow made of many faint, stacked circles
    color = random.choice(NEBULA_COLORS)
    max_radius = random.randint(250, 500)
    center_x = random.randint(0, width)
    center_y = random.randint(0, height)

    for radius in range(max_radius, 0, -20):
        layer = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(layer, (*color, 3), (radius, radius), radius)
        background.blit(layer, (center_x - radius, center_y - radius))


def draw_stars(background, width: int, height: int):
    for _ in range(BACKGROUND_STAR_COUNT):
        position = (random.randint(0, width), random.randint(0, height))
        brightness = random.randint(60, 200)
        color = (brightness, brightness, min(255, brightness + 30))
        # Most stars are tiny, a few are a little larger
        radius = 1 if random.random() < 0.9 else 2
        pygame.draw.circle(background, color, position, radius)


def create_background(width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
    background = pygame.Surface((width, height))
    background.fill(BACKGROUND_COLOR)
    for _ in range(BACKGROUND_NEBULA_COUNT):
        draw_nebula(background, width, height)
    draw_stars(background, width, height)
    return background

