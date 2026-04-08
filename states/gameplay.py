import pygame

from entities import Player
from ui.hud import draw_gameplay_hud


class GameplayState:
    def __init__(self, game):
        self.game = game
        self.player = None
        self.lives = 3
        self.score = 0
        self.respawn_timer = 0
        self.invincibility_timer = 0

        self.reset_game()

    def cleanup(self):
        for sprite in list(self.game.asteroids):
            sprite.kill()

        for sprite in list(self.game.shots):
            sprite.kill()

        for sprite in list(self.game.drawable):
            if isinstance(sprite, Player):
                sprite.kill()

        self.game.asteroid_field.spawn_timer = 0.0

    def reset_game(self):
        self.cleanup()

        self.player = Player(
            self.game.screen.get_width() / 2,
            self.game.screen.get_height() / 2,
            self.game.sounds,
        )
        self.player.active = False
        self.player.visible = True
        self.player.invincible = False

        self.lives = 3
        self.score = 0
        self.respawn_timer = 0.25
        self.invincibility_timer = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.menu import MenuState

                self.cleanup()
                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.player.position = pygame.Vector2(
                    self.game.screen.get_width() / 2,
                    self.game.screen.get_height() / 2,
                )
                self.player.velocity = pygame.Vector2(0, 0)
                self.player.rotation = 0
                self.player.active = True
                self.player.visible = True
                self.player.invincible = True
                self.invincibility_timer = 2.0

        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
            self.player.invincible = True
            self.player.visible = int(self.invincibility_timer * 10) % 2 == 0

            if self.invincibility_timer <= 0:
                self.player.invincible = False
                self.player.visible = True

        self.game.updatable.update(dt)

        for asteroid in self.game.asteroids:
            if (
                self.player.active
                and self.invincibility_timer <= 0
                and asteroid.collides_with(self.player)
            ):
                self.game.sounds.play_player_destroyed()
                self.lives -= 1

                if self.lives > 0:
                    self.player.active = False
                    self.player.visible = False
                    self.player.invincible = False
                    self.respawn_timer = 1.0
                else:
                    self.player.active = False
                    self.player.visible = False
                    self.player.invincible = False

                    from states.game_over import GameOverState

                    self.game.change_state(GameOverState(self.game, self.score))

                break

        for asteroid in list(self.game.asteroids):
            for shot in list(self.game.shots):
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()
                    self.game.sounds.play_impact()
                    self.score += 10
                    break

    def draw(self, screen):
        for sprite in self.game.drawable:
            sprite.draw(screen)

        draw_gameplay_hud(
            screen,
            self.game.info_font,
            self.score,
            self.lives,
        )
