import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override in subclass
        pass

    def update(self, delta_time: float) -> None:
        # must override in subclass
        pass

    def collides_with(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        return distance <= self.radius + other.radius