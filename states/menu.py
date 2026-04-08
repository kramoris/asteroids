import pygame

from ui.text import draw_centered_text


class MenuState:
    MENU_ITEMS = ["Start Game", "Options", "Quit"]

    def __init__(self, game):
        self.game = game
        self.selected_index = 0

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.MENU_ITEMS)

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.MENU_ITEMS)

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
            ):
                selected_item = self.MENU_ITEMS[self.selected_index]

                if selected_item == "Start Game":
                    from states.gameplay import GameplayState

                    self.game.change_state(GameplayState(self.game))

                elif selected_item == "Options":
                    from states.options import OptionsState

                    self.game.change_state(OptionsState(self.game))

                elif selected_item == "Quit":
                    self.game.quit()

            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        draw_centered_text(
            screen,
            self.game.title_font,
            "ASTEROIDS",
            "white",
            screen.get_height() / 2 - 140,
        )

        for index, item in enumerate(self.MENU_ITEMS):
            color = "yellow" if index == self.selected_index else "white"
            y = screen.get_height() / 2 - 20 + index * 60
            prefix = "> " if index == self.selected_index else "  "

            draw_centered_text(
                screen,
                self.game.menu_font,
                f"{prefix}{item}",
                color,
                y,
            )

        draw_centered_text(
            screen,
            self.game.info_font,
            "Up/Down to navigate, Enter to select",
            "gray",
            screen.get_height() / 2 + 200,
        )
