import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event, log_state, set_logging_fps
from player import Player
from settings import (
    get_setting_options,
    load_settings,
    reset_settings,
    save_settings,
)
from shot import Shot


MENU_ITEMS = ["Start Game", "Options", "Quit"]
OPTIONS_ITEMS = [
    "Resolution Width",
    "Resolution Height",
    "FPS Limit",
    "Reset to Defaults",
    "Back",
]


def draw_centered_text(screen, font, text, color, y):
    screen_width = screen.get_width()
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen_width / 2, y))
    screen.blit(surface, rect)


def reset_game(player, asteroids, shots, asteroidfield, screen):
    if player is not None:
        player.kill()

    for asteroid in list(asteroids):
        asteroid.kill()

    for shot in list(shots):
        shot.kill()

    asteroidfield.spawn_timer = 0.0

    player = Player(screen.get_width() / 2, screen.get_height() / 2)
    player.active = False
    player.visible = True
    player.invincible = False

    return {
        "player": player,
        "lives": 3,
        "score": 0,
        "respawn_timer": 0.25,
        "invincibility_timer": 0,
        "game_over_timer": 0,
    }


def apply_resolution(settings):
    return pygame.display.set_mode(
        (settings["screen_width"], settings["screen_height"])
    )


def adjust_setting(settings, key, direction):
    rule = get_setting_options(key)
    new_value = settings[key] + rule["step"] * direction
    new_value = max(rule["min"], min(rule["max"], new_value))
    settings[key] = new_value


def option_label(item, settings):
    if item == "Resolution Width":
        return f"Resolution Width: {settings['screen_width']}"
    if item == "Resolution Height":
        return f"Resolution Height: {settings['screen_height']}"
    if item == "FPS Limit":
        return f"FPS Limit: {settings['fps_limit']}"
    return item


def main():
    pygame.init()

    settings = load_settings()
    set_logging_fps(settings["fps_limit"])

    screen = apply_resolution(settings)
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

    asteroidfield = AsteroidField(screen.get_width(), screen.get_height())
    player = None

    state = "menu"
    selected_menu_index = 0
    selected_options_index = 0

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
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_menu_index = (selected_menu_index - 1) % len(
                            MENU_ITEMS
                        )
                    elif event.key == pygame.K_DOWN:
                        selected_menu_index = (selected_menu_index + 1) % len(
                            MENU_ITEMS
                        )
                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    ):
                        selected_item = MENU_ITEMS[selected_menu_index]

                        if selected_item == "Start Game":
                            game_data = reset_game(
                                player, asteroids, shots, asteroidfield, screen
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
                            save_settings(settings)
                            pygame.quit()
                            sys.exit()

                    elif event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        pygame.quit()
                        sys.exit()

            elif state == "options":
                if event.type == pygame.KEYDOWN:
                    current_item = OPTIONS_ITEMS[selected_options_index]

                    if event.key == pygame.K_UP:
                        selected_options_index = (selected_options_index - 1) % len(
                            OPTIONS_ITEMS
                        )
                    elif event.key == pygame.K_DOWN:
                        selected_options_index = (selected_options_index + 1) % len(
                            OPTIONS_ITEMS
                        )
                    elif event.key == pygame.K_LEFT:
                        if current_item == "Resolution Width":
                            adjust_setting(settings, "screen_width", -1)
                            screen = apply_resolution(settings)
                            asteroidfield.screen_width = screen.get_width()
                        elif current_item == "Resolution Height":
                            adjust_setting(settings, "screen_height", -1)
                            screen = apply_resolution(settings)
                            asteroidfield.screen_height = screen.get_height()
                        elif current_item == "FPS Limit":
                            adjust_setting(settings, "fps_limit", -1)
                            set_logging_fps(settings["fps_limit"])
                        save_settings(settings)

                    elif event.key == pygame.K_RIGHT:
                        if current_item == "Resolution Width":
                            adjust_setting(settings, "screen_width", 1)
                            screen = apply_resolution(settings)
                            asteroidfield.screen_width = screen.get_width()
                        elif current_item == "Resolution Height":
                            adjust_setting(settings, "screen_height", 1)
                            screen = apply_resolution(settings)
                            asteroidfield.screen_height = screen.get_height()
                        elif current_item == "FPS Limit":
                            adjust_setting(settings, "fps_limit", 1)
                            set_logging_fps(settings["fps_limit"])
                        save_settings(settings)

                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    ):
                        if current_item == "Reset to Defaults":
                            settings = reset_settings()
                            set_logging_fps(settings["fps_limit"])
                            screen = apply_resolution(settings)
                            asteroidfield.screen_width = screen.get_width()
                            asteroidfield.screen_height = screen.get_height()
                        elif current_item == "Back":
                            state = "menu"

                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"

            elif state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

            elif state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        pygame.quit()
                        sys.exit()
                    else:
                        state = "menu"

        screen.fill("black")

        if state == "menu":
            draw_centered_text(
                screen, title_font, "ASTEROIDS", "white", screen.get_height() / 2 - 140
            )

            for index, item in enumerate(MENU_ITEMS):
                color = "yellow" if index == selected_menu_index else "white"
                y = screen.get_height() / 2 - 20 + index * 60
                prefix = "> " if index == selected_menu_index else "  "
                draw_centered_text(screen, menu_font, f"{prefix}{item}", color, y)

            draw_centered_text(
                screen,
                info_font,
                "Up/Down to navigate, Enter to select",
                "gray",
                screen.get_height() / 2 + 200,
            )

        elif state == "options":
            draw_centered_text(
                screen, title_font, "OPTIONS", "white", screen.get_height() / 2 - 180
            )

            for index, item in enumerate(OPTIONS_ITEMS):
                color = "yellow" if index == selected_options_index else "white"
                y = screen.get_height() / 2 - 60 + index * 50
                prefix = "> " if index == selected_options_index else "  "
                draw_centered_text(
                    screen,
                    menu_font,
                    f"{prefix}{option_label(item, settings)}",
                    color,
                    y,
                )

            draw_centered_text(
                screen,
                info_font,
                "Left/Right changes values, Enter selects, ESC returns",
                "gray",
                screen.get_height() / 2 + 180,
            )

        elif state == "playing":
            if respawn_timer > 0:
                respawn_timer -= dt
                if respawn_timer <= 0:
                    player.position = pygame.Vector2(
                        screen.get_width() / 2,
                        screen.get_height() / 2,
                    )
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
                screen.get_height() / 2 - 60,
            )
            draw_centered_text(
                screen,
                info_font,
                f"Final Score: {score}",
                "white",
                screen.get_height() / 2 + 10,
            )

            if game_over_timer <= 0:
                draw_centered_text(
                    screen,
                    info_font,
                    "Press any key to return to menu, or ESC to quit",
                    "gray",
                    screen.get_height() / 2 + 70,
                )

        pygame.display.flip()
        dt = clock.tick(settings["fps_limit"]) / 1000


if __name__ == "__main__":
    main()
