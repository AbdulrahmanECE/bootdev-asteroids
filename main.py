import math
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_LIVES,
    RESPAWN_SAFE_RADIUS,
    GAME_OVER_SECONDS,
)
from logger import log_state, log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField


def draw_text(screen, font, text, position):
    screen.blit(font.render(text, True, "white"), position)


def draw_centered_text(screen, font, text, y_offset):
    rendered = font.render(text, True, "white")
    rect = rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(rendered, rect)


def respawn(player, asteroids):
    # Put the ship back in the middle and clear any asteroids around it
    center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.position = center.copy()
    player.rotation = 0
    for asteroid in asteroids:
        if asteroid.position.distance_to(center) <= RESPAWN_SAFE_RADIUS + asteroid.radius:
            asteroid.kill()


def game_over_screen(screen, clock):
    # Returns True to restart, False to quit
    title_font = pygame.font.Font(None, 120)
    info_font = pygame.font.Font(None, 48)
    time_left = GAME_OVER_SECONDS

    while time_left > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True

        screen.fill("black")
        draw_centered_text(screen, title_font, "GAME OVER", -60)
        draw_centered_text(screen, info_font, "Press R to restart or Q to quit", 30)
        draw_centered_text(screen, info_font, f"Quitting in {math.ceil(time_left)}...", 90)
        pygame.display.flip()

        time_left -= clock.tick(60) / 1000

    return False


def main(screen):
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    delta_time = 0.0
    lives = PLAYER_LIVES
    hud_font = pygame.font.Font(None, 48)


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_SHOOT_COOLDOWN_SECONDS)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    asteroidfield = pygame.sprite.Group()
    AsteroidField.containers = updatable

    asteroidfield = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)

    while True:
        log_state()
        
        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen)
        draw_text(screen, hud_font, f"Lives: {lives}", (20, 20))
        pygame.display.flip()
        updatable.update(delta_time)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    log_event("game_over")
                    return game_over_screen(screen, clock)
                respawn(player, asteroids)
                break

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True

        delta_time = clock.tick(60) / 1000

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while main(screen):
        pass
