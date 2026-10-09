import random
import pygame

from collections.abc import Callable
from asteroid import Asteroid
from constants import *

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

        screen_surf = pygame.display.get_surface()
        width = screen_surf.get_width() if screen_surf else SCREEN_WIDTH
        height = screen_surf.get_height() if screen_surf else SCREEN_HEIGHT

        self.edges: list[Edge] = [
            (
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * height),
            ),
            (
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(
                    width + ASTEROID_MAX_RADIUS, y * height
                ),
            ),
            (
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * width, -ASTEROID_MAX_RADIUS),
            ),
            (
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(
                    x * width, height + ASTEROID_MAX_RADIUS
                ),
            ),
        ]

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)