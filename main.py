import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    lives = 3
    respawn_timer = 0
    invincibility_timer = 0
    game_over = False
    restart_timer = 0

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    asteroidfield = AsteroidField()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    font = pygame.font.SysFont(None, 36)

    while True:
        log_state()

        if restart_timer > 0:
            restart_timer -= dt

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys

                sys.exit()

            if game_over and restart_timer <= 0 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    import sys

                    sys.exit()
                else:
                    return

        screen.fill("black")

        if not game_over:
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
                        game_over = True
                        restart_timer = 1.0

                    break

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score += 10

            for sprite in drawable:
                sprite.draw(screen)

            score_surface = font.render(f"Score: {score}", True, "white")
            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(score_surface, (10, 10))
            screen.blit(lives_surface, (10, 50))

        else:
            for sprite in drawable:
                sprite.draw(screen)

            over_text = "GAME OVER - Press Any Key to Restart or ESC to Exit"
            over_surface = font.render(over_text, True, "red")
            final_score_text = f"Final Score: {score}"
            final_score_surface = font.render(final_score_text, True, "white")

            over_rect = over_surface.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            score_rect = final_score_surface.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )

            screen.blit(over_surface, over_rect)
            screen.blit(final_score_surface, score_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    while True:
        main()
