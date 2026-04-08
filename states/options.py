import pygame

from config import get_setting_options, reset_settings, save_settings
from ui.text import draw_centered_text


class OptionsState:
    OPTIONS_ITEMS = [
        "Resolution Width",
        "Resolution Height",
        "FPS Limit",
        "Reset to Defaults",
        "Back",
    ]

    def __init__(self, game):
        self.game = game
        self.selected_index = 0

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            current_item = self.OPTIONS_ITEMS[self.selected_index]

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(
                    self.OPTIONS_ITEMS
                )

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(
                    self.OPTIONS_ITEMS
                )

            elif event.key == pygame.K_LEFT:
                if current_item == "Resolution Width":
                    self.adjust_setting("screen_width", -1)
                    self.game.apply_resolution()
                elif current_item == "Resolution Height":
                    self.adjust_setting("screen_height", -1)
                    self.game.apply_resolution()
                elif current_item == "FPS Limit":
                    self.adjust_setting("fps_limit", -1)

                save_settings(self.game.settings)

            elif event.key == pygame.K_RIGHT:
                if current_item == "Resolution Width":
                    self.adjust_setting("screen_width", 1)
                    self.game.apply_resolution()
                elif current_item == "Resolution Height":
                    self.adjust_setting("screen_height", 1)
                    self.game.apply_resolution()
                elif current_item == "FPS Limit":
                    self.adjust_setting("fps_limit", 1)

                save_settings(self.game.settings)

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
            ):
                if current_item == "Reset to Defaults":
                    self.game.settings = reset_settings()
                    self.game.apply_resolution()

                elif current_item == "Back":
                    from states.menu import MenuState

                    self.game.change_state(MenuState(self.game))

            elif event.key == pygame.K_ESCAPE:
                from states.menu import MenuState

                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        pass

    def draw(self, screen):
        draw_centered_text(
            screen,
            self.game.title_font,
            "OPTIONS",
            "white",
            screen.get_height() / 2 - 180,
        )

        for index, item in enumerate(self.OPTIONS_ITEMS):
            color = "yellow" if index == self.selected_index else "white"
            y = screen.get_height() / 2 - 60 + index * 50
            prefix = "> " if index == self.selected_index else "  "

            draw_centered_text(
                screen,
                self.game.menu_font,
                f"{prefix}{self.option_label(item)}",
                color,
                y,
            )

        draw_centered_text(
            screen,
            self.game.info_font,
            "Left/Right changes values, Enter selects, ESC returns",
            "gray",
            screen.get_height() / 2 + 180,
        )

    def adjust_setting(self, key, direction):
        rule = get_setting_options(key)
        new_value = self.game.settings[key] + rule["step"] * direction
        new_value = max(rule["min"], min(rule["max"], new_value))
        self.game.settings[key] = new_value

    def option_label(self, item):
        if item == "Resolution Width":
            return f"Resolution Width: {self.game.settings['screen_width']}"
        if item == "Resolution Height":
            return f"Resolution Height: {self.game.settings['screen_height']}"
        if item == "FPS Limit":
            return f"FPS Limit: {self.game.settings['fps_limit']}"
        return item
