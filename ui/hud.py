def draw_gameplay_hud(screen, font, score, lives):
    score_surface = font.render(f"Score: {score}", True, "white")
    lives_surface = font.render(f"Lives: {lives}", True, "white")
    hint_surface = font.render("ESC: Menu", True, "gray")

    screen.blit(score_surface, (10, 10))
    screen.blit(lives_surface, (10, 50))
    screen.blit(hint_surface, (10, 90))
