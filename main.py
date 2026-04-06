import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


MENU_ITEMS = ["Start Game", "Options", "Quit"]


def draw_centered_text(screen, font, text, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH / 2, y))
    screen.blit(surface, rect)


def reset_game(player, asteroids, shots, asteroidfield):
    if player is not None:
        player.kill()

    for asteroid in list(asteroids):
        asteroid.kill()

    for shot in list(shots):
        shot.kill()

    asteroidfield.spawn_timer = 0.0

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    return {
        "player": player,
        "lives": 3,
        "score": 0,
        "respawn_timer": 0,
        "invincibility_timer": 0,
        "game_over_timer": 0,
    }


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(None, 72)
    menu_font = pygame.font.SysFont(None, 48)
    info_font = pygame.font.SysFont(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    asteroidfield = AsteroidField()
    player = None

    state = "menu"
    selected_menu_index = 0

    lives = 3
    score = 0
    respawn_timer = 0
    invincibility_timer = 0
    game_over_timer = 0

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_menu_index = (selected_menu_index - 1) % len(MENU_ITEMS)
                    elif event.key == pygame.K_DOWN:
                        selected_menu_index = (selected_menu_index + 1) % len(MENU_ITEMS)
                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    ):
                        selected_item = MENU_ITEMS[selected_menu_index]

                        if selected_item == "Start Game":
                            game_data = reset_game(
                                player, asteroids, shots, asteroidfield
                            )
                            player = game_data["player"]
                            lives = game_data["lives"]
                            score = game_data["score"]
                            respawn_timer = game_data["respawn_timer"]
                            invincibility_timer = game_data["invincibility_timer"]
                            game_over_timer = game_data["game_over_timer"]
                            state = "playing"

                        elif selected_item == "Options":
                            state = "options"

                        elif selected_item == "Quit":
                            pygame.quit()
                            sys.exit()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            elif state == "options":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"

            elif state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

            elif state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        state = "menu"

        screen.fill("black")

        if state == "menu":
            draw_centered_text(
                screen, title_font, "ASTEROIDS", "white", SCREEN_HEIGHT / 2 - 140
            )

            for index, item in enumerate(MENU_ITEMS):
                color = "yellow" if index == selected_menu_index else "white"
                y = SCREEN_HEIGHT / 2 - 20 + index * 60
                prefix = "> " if index == selected_menu_index else "  "
                draw_centered_text(screen, menu_font, f"{prefix}{item}", color, y)

            draw_centered_text(
                screen,
                info_font,
                "Up/Down to navigate, Enter to select",
                "gray",
                SCREEN_HEIGHT / 2 + 200,
            )

        elif state == "options":
            draw_centered_text(
                screen, title_font, "OPTIONS", "white", SCREEN_HEIGHT / 2 - 80
            )
            draw_centered_text(
                screen,
                info_font,
                "Options coming soon.",
                "white",
                SCREEN_HEIGHT / 2,
            )
            draw_centered_text(
                screen,
                info_font,
                "Press ESC to return to menu.",
                "gray",
                SCREEN_HEIGHT / 2 + 60,
            )

        elif state == "playing":
            if respawn_timer > 0:
                respawn_timer -= dt
                if respawn_timer <= 0:
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)
                    player.rotation = 0
                    player.active = True
                    player.visible = True
                    player.invincible = True
                    invincibility_timer = 2.0

            if invincibility_timer > 0:
                invincibility_timer -= dt
                player.invincible = True
                player.visible = int(invincibility_timer * 10) % 2 == 0
                if invincibility_timer <= 0:
                    player.invincible = False
                    player.visible = True

            updatable.update(dt)

            for asteroid in asteroids:
                if (
                    player.active
                    and invincibility_timer <= 0
                    and asteroid.collides_with(player)
                ):
                    log_event("player_hit")
                    lives -= 1

                    if lives > 0:
                        player.active = False
                        player.visible = False
                        player.invincible = False
                        respawn_timer = 1.0
                    else:
                        player.active = False
                        player.visible = False
                        player.invincible = False
                        state = "game_over"
                        game_over_timer = 0.5

                    break

            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score += 10
                        break

            for sprite in drawable:
                sprite.draw(screen)

            score_surface = info_font.render(f"Score: {score}", True, "white")
            lives_surface = info_font.render(f"Lives: {lives}", True, "white")
            hint_surface = info_font.render("ESC: Menu", True, "gray")

            screen.blit(score_surface, (10, 10))
            screen.blit(lives_surface, (10, 50))
            screen.blit(hint_surface, (10, 90))

        elif state == "game_over":
            if game_over_timer > 0:
                game_over_timer -= dt

            for sprite in drawable:
                sprite.draw(screen)

            draw_centered_text(
                screen,
                title_font,
                "GAME OVER",
                "red",
                SCREEN_HEIGHT / 2 - 60,
            )
            draw_centered_text(
                screen,
                info_font,
                f"Final Score: {score}",
                "white",
                SCREEN_HEIGHT / 2 + 10,
            )

            if game_over_timer <= 0:
                draw_centered_text(
                    screen,
                    info_font,
                    "Press any key to return to menu, or ESC to quit",
                    "gray",
                    SCREEN_HEIGHT / 2 + 70,
                )

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
