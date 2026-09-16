import pygame
import random
from circleshape import CircleShape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_KINDS

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, delta_time):
        self.position += self.velocity * delta_time

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