import pygame
import sys
from src.game import Game

def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()

    # Game settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60

    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense Strategy Game")
    clock = pygame.time.Clock()

    # Create game instance
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        # Update game
        game.update()

        # Draw everything
        screen.fill((34, 139, 34))  # Forest green background
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
