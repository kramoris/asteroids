def draw_centered_text(screen, font, text, color, y):
    screen_width = screen.get_width()
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen_width / 2, y))
    screen.blit(surface, rect)
