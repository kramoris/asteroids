from pathlib import Path
import random

import pygame


class GameSounds:
    def __init__(self):
        self.enabled = False
        self.shoot_sounds = []

    def initialize(self):
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False
            return

        sounds_dir = Path(__file__).resolve().parent / "sounds"

        self.shoot_sounds = [
            pygame.mixer.Sound(str(sounds_dir / f"shoot{i}.wav")) for i in range(1, 6)
        ]

        for sound in self.shoot_sounds:
            sound.set_volume(0.3)

    def play_shoot(self):
        if not self.enabled or not self.shoot_sounds:
            return

        random.choice(self.shoot_sounds).play()
