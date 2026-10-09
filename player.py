import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *
from shapes import SHIP_BODY, SHIP_FINS, SHIP_DETAILS

class Player(CircleShape):
    def __init__(self, x, y, shot_cd):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0
        self.invincible_timer = 0

    def to_screen(self, points):
        # Turn unit-space model points into positions on the screen
        return [self.position + point.rotate(self.rotation) * self.radius for point in points]

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

        body = self.to_screen(SHIP_BODY)
        pygame.draw.polygon(screen, "black", body)
        pygame.draw.polygon(screen, color, body, LINE_WIDTH)
        for fin in SHIP_FINS:
            pygame.draw.polygon(screen, color, self.to_screen(fin))
        for points, closed in SHIP_DETAILS:
            pygame.draw.lines(screen, color, closed, self.to_screen(points), 1)

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
        screen_surf = pygame.display.get_surface()
        width = screen_surf.get_width() if screen_surf else SCREEN_WIDTH
        height = screen_surf.get_height() if screen_surf else SCREEN_HEIGHT

        # Wait until the ship is fully off screen, then bring it in from the opposite edge
        if self.position.x < -self.radius:
            self.position.x = width + self.radius
        elif self.position.x > width + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = height + self.radius
        elif self.position.y > height + self.radius:
            self.position.y = -self.radius

    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        shot_velocity = pygame.Vector2(0, 1)
        rotated = shot_velocity.rotate(self.rotation)
        shot_velocity = rotated * PLAYER_SHOOT_SPEED
        bullet.velocity = shot_velocity

