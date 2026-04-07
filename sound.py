from pathlib import Path
import random

import pygame
from constants import SHOOT_VOLUME, IMPACT_VOLUME


class GameSounds:
    def __init__(self):
        self.enabled = False
        self.shoot_sounds = []
        self.impact_sounds = []

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
            sound.set_volume(SHOOT_VOLUME)

        self.impact_sounds = [
            pygame.mixer.Sound(str(sounds_dir / f"impact-hit{i}.wav"))
            for i in range(1, 3)
        ]

        for sound in self.impact_sounds:
            sound.set_volume(IMPACT_VOLUME)

    def play_shoot(self):
        if not self.enabled or not self.shoot_sounds:
            return

        random.choice(self.shoot_sounds).play()

    def play_impact(self):
        if not self.enabled or not self.impact_sounds:
            return

        random.choice(self.impact_sounds).play()
