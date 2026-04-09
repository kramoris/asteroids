import pygame

from config.constants import LINE_WIDTH, SHOT_RADIUS
from entities.circle_shape import CircleShape


class Shot(CircleShape):
    SCREEN_MARGIN = 50

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

        screen = pygame.display.get_surface()
        if screen is None:
            return

        width = screen.get_width()
        height = screen.get_height()
        margin = self.SCREEN_MARGIN

        if (
            self.position.x < -margin
            or self.position.x > width + margin
            or self.position.y < -margin
            or self.position.y > height + margin
        ):
            self.kill()
