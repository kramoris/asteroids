import sys

import pygame

from audio import GameSounds
from config import load_settings, save_settings
from entities import Asteroid, AsteroidField, Player, Shot


class Game:
    def __init__(self):
        pygame.init()

        self.settings = load_settings()

        self.screen = pygame.display.set_mode(
            (self.settings["screen_width"], self.settings["screen_height"])
        )
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(None, 72)
        self.menu_font = pygame.font.SysFont(None, 48)
        self.info_font = pygame.font.SysFont(None, 36)

        self.sounds = GameSounds()
        self.sounds.initialize()

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.shots, self.updatable, self.drawable)

        self.asteroid_field = AsteroidField(
            self.screen.get_width(),
            self.screen.get_height(),
        )

        from states.menu import MenuState

        self.state = MenuState(self)

        self.running = True

    def change_state(self, new_state):
        self.state = new_state

    def apply_resolution(self):
        self.screen = pygame.display.set_mode(
            (self.settings["screen_width"], self.settings["screen_height"])
        )

        if self.asteroid_field is not None:
            self.asteroid_field.screen_width = self.screen.get_width()
            self.asteroid_field.screen_height = self.screen.get_height()

    def quit(self):
        save_settings(self.settings)
        pygame.quit()
        sys.exit()

    def run(self):
        dt = 0

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

            self.state.handle_events(events)
            self.state.update(dt)

            self.screen.fill("black")
            self.state.draw(self.screen)

            pygame.display.flip()
            dt = self.clock.tick(self.settings["fps_limit"]) / 1000
