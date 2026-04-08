import pygame

from ui.text import draw_centered_text


class GameOverState:
    def __init__(self, game, final_score):
        self.game = game
        self.final_score = final_score
        self.game_over_timer = 0.5

    def handle_events(self, events):
        if self.game_over_timer > 0:
            return

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.game.quit()
            else:
                from states.menu import MenuState

                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        if self.game_over_timer > 0:
            self.game_over_timer -= dt

    def draw(self, screen):
        for sprite in self.game.drawable:
            sprite.draw(screen)

        draw_centered_text(
            screen,
            self.game.title_font,
            "GAME OVER",
            "red",
            screen.get_height() / 2 - 60,
        )
        draw_centered_text(
            screen,
            self.game.info_font,
            f"Final Score: {self.final_score}",
            "white",
            screen.get_height() / 2 + 10,
        )

        if self.game_over_timer <= 0:
            draw_centered_text(
                screen,
                self.game.info_font,
                "Press any key to return to menu, or ESC to quit",
                "gray",
                screen.get_height() / 2 + 70,
            )
