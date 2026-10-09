import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y, shot_cd):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0
        self.invincible_timer = 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def is_invincible(self):
        return self.invincible_timer > 0

    def make_invincible(self):
        self.invincible_timer = PLAYER_INVINCIBLE_SECONDS

    def draw(self, screen):
        color = "white"
        if self.is_invincible():
            # Swap colors every blink interval
            blink_step = int(self.invincible_timer / PLAYER_BLINK_INTERVAL_SECONDS)
            if blink_step % 2 == 0:
                color = PLAYER_BLINK_COLOR
        pygame.draw.polygon(screen, color, self.triangle(), LINE_WIDTH)

    def rotate(self, delta_time):
        self.rotation += delta_time * PLAYER_TURN_SPEED

    def update(self, delta_time: float) -> None:
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-delta_time)

        if keys[pygame.K_d]:
            self.rotate(delta_time)

        if keys[pygame.K_w]:
            self.move(delta_time)

        if keys[pygame.K_s]:
            self.move(-delta_time)

        if keys[pygame.K_SPACE]:
            if self.shot_cd > 0:
                self.shot_cd -= delta_time
            else: 
                self.shot_cd = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
            

    def move(self, delta_time):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * delta_time
        self.position += rotated_with_speed_vector
        self.wrap_around_screen()

    def wrap_around_screen(self):
        # Wait until the ship is fully off screen, then bring it in from the opposite edge
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        shot_velocity = pygame.Vector2(0, 1)
        rotated = shot_velocity.rotate(self.rotation)
        shot_velocity = rotated * PLAYER_SHOOT_SPEED
        bullet.velocity = shot_velocity

