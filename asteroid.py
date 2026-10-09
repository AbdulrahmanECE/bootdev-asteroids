import math
import pygame
import random
from circleshape import CircleShape
from logger import log_event
from shapes import ASTEROID_MODELS
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_KINDS, ASTEROID_MAX_SPIN

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        # Pick one of the two models for this size
        size = round(radius / ASTEROID_MIN_RADIUS)
        size = max(1, min(size, len(ASTEROID_MODELS)))
        self.model = random.choice(ASTEROID_MODELS[size])
        self.rotation = random.uniform(0, 360)
        self.spin = random.uniform(-ASTEROID_MAX_SPIN, ASTEROID_MAX_SPIN)

    def to_screen(self, point):
        # Turn a unit-space model point into a position on the screen
        return self.position + point.rotate(self.rotation) * self.radius

    def draw(self, screen):
        outline = [self.to_screen(point) for point in self.model["outline"]]
        # Fill black first so the background doesn't show through the rock
        pygame.draw.polygon(screen, "black", outline)
        pygame.draw.polygon(screen, "white", outline, LINE_WIDTH)

        crater_width = 1 if self.radius <= ASTEROID_MIN_RADIUS else LINE_WIDTH
        for x, y, size, has_rim in self.model["craters"]:
            center = self.to_screen(pygame.Vector2(x, y))
            crater_radius = size * self.radius
            pygame.draw.circle(screen, "white", center, crater_radius, crater_width)
            if has_rim:
                self.draw_crater_rim(screen, center, crater_radius)

    def draw_crater_rim(self, screen, center, crater_radius):
        # A crescent line inside the crater, turning with the asteroid
        rim_radius = crater_radius * 0.85
        if rim_radius < 3:
            return
        direction = pygame.Vector2(-1, -1).normalize().rotate(self.rotation)
        # Shift the rim circle away from the side we draw on, so the arc sits
        # inside the crater and its ends meet the crater edge
        rim_center = center - direction * crater_radius * 0.3
        rect = pygame.Rect(0, 0, rim_radius * 2, rim_radius * 2)
        rect.center = (round(rim_center.x), round(rim_center.y))
        # pygame arcs measure angles counterclockwise with y pointing up
        angle = math.atan2(-direction.y, direction.x)
        rim_width = 1 if self.radius <= ASTEROID_MIN_RADIUS else LINE_WIDTH
        pygame.draw.arc(screen, "white", rect, angle - 1.3, angle + 1.3, rim_width)

    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.rotation += self.spin * delta_time

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return None

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        split_vector1 = self.velocity.rotate(angle)
        split_vector2 = self.velocity.rotate(-angle)

        split_radius = self.radius - ASTEROID_MIN_RADIUS

        split_asteroid1 = Asteroid(self.position.x, self.position.y, split_radius)
        split_asteroid1.velocity = split_vector1 * 1.2
        split_asteroid2 = Asteroid(self.position.x, self.position.y, split_radius)
        split_asteroid2.velocity = split_vector2 * 1.2