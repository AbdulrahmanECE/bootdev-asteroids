import math
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAX_SCREEN_WIDTH,
    MAX_SCREEN_HEIGHT,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_LIVES,
    RESPAWN_SAFE_RADIUS,
    GAME_OVER_SECONDS,
    BASE_SCORE_SMALL,
    SCORE_MULTIPLIER_INCREMENT,
    MAX_SCORE_MULTIPLIER,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
)
from logger import log_state, log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from background import create_background


def draw_text(screen, font, text, position):
    screen.blit(font.render(text, True, "white"), position)


def draw_centered_text(screen, font, text, y_offset):
    rendered = font.render(text, True, "white")
    width, height = screen.get_size()
    rect = rendered.get_rect(center=(width / 2, height / 2 + y_offset))
    screen.blit(rendered, rect)


def respawn(player, asteroids):
    # Put the ship back in the middle and clear any asteroids around it
    screen_surf = pygame.display.get_surface()
    width = screen_surf.get_width() if screen_surf else SCREEN_WIDTH
    height = screen_surf.get_height() if screen_surf else SCREEN_HEIGHT

    center = pygame.Vector2(width / 2, height / 2)
    player.position = center.copy()
    player.rotation = 0
    player.make_invincible()
    for asteroid in asteroids:
        if asteroid.position.distance_to(center) <= RESPAWN_SAFE_RADIUS + asteroid.radius:
            asteroid.kill()


def get_asteroid_score(radius):
    if radius >= ASTEROID_MAX_RADIUS:
        return int(BASE_SCORE_SMALL * 2.0)
    elif radius <= ASTEROID_MIN_RADIUS:
        return BASE_SCORE_SMALL
    else:
        return int(BASE_SCORE_SMALL * 1.5)


def game_over_screen(screen, clock, background, final_score):
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

        screen.blit(background, (0, 0))
        draw_centered_text(screen, title_font, "GAME OVER", -80)
        draw_centered_text(screen, info_font, f"Final Score: {final_score}", -10)
        draw_centered_text(screen, info_font, "Press R to restart or Q to quit", 50)
        draw_centered_text(screen, info_font, f"Quitting in {math.ceil(time_left)}...", 110)
        pygame.display.flip()

        time_left -= clock.tick(60) / 1000

    return False


def get_display_resolution():
    info = pygame.display.Info()
    # If display info detects a valid desktop monitor size, fit up to 2K
    if info.current_w > 0 and info.current_h > 0:
        width = min(info.current_w, MAX_SCREEN_WIDTH)
        height = min(info.current_h, MAX_SCREEN_HEIGHT)
        return width, height
    return SCREEN_WIDTH, SCREEN_HEIGHT


def main(screen, background):
    width, height = screen.get_size()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {width} \nScreen height: {height}")

    clock = pygame.time.Clock()
    delta_time = 0.0
    lives = PLAYER_LIVES
    score = 0
    multiplier = 1.0
    hud_font = pygame.font.Font(None, 48)


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    
    player = Player(width / 2, height / 2, PLAYER_SHOOT_COOLDOWN_SECONDS)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    asteroidfield = pygame.sprite.Group()
    AsteroidField.containers = updatable

    asteroidfield = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)

    while True:
        log_state()
        
        screen.blit(background, (0, 0))
        for drawing in drawable:
            drawing.draw(screen)
        draw_text(screen, hud_font, f"Lives: {lives}", (20, 20))
        draw_text(screen, hud_font, f"Score: {score}", (20, 65))
        draw_text(screen, hud_font, f"Multiplier: {multiplier:.1f}x", (20, 110))
        pygame.display.flip()
        updatable.update(delta_time)

        for asteroid in asteroids:
            if not player.is_invincible() and player.collides_with(asteroid):
                log_event("player_hit")
                lives -= 1
                multiplier = 1.0
                if lives <= 0:
                    print("Game Over!")
                    log_event("game_over")
                    return game_over_screen(screen, clock, background, score)
                respawn(player, asteroids)
                break

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    base_pts = get_asteroid_score(asteroid.radius)
                    score += int(round(base_pts * multiplier))
                    multiplier = min(MAX_SCORE_MULTIPLIER, round(multiplier + SCORE_MULTIPLIER_INCREMENT, 2))
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
    width, height = get_display_resolution()
    screen = pygame.display.set_mode((width, height))
    background = create_background(width, height)
    while main(screen, background):
        pass
