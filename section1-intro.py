import pygame
import os

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize Pygame and create a screen object
pygame.init()
GScreen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game 1")

# Load resources
try:
    PICTURE = pygame.image.load(os.path.join('section1', 'rab2.jpg'))
except pygame.error as e:
    print(f"Error loading image: {e}")
    PICTURE = None

try:
    SONG = os.path.join(os.getcwd(), 'section1', 'piano.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load(SONG)
except pygame.error as e:
    print(f"Error loading music: {e}")

def draw():
    """Draws the picture on the screen."""
    GScreen.fill((255, 255, 255))
    if PICTURE:
        GScreen.blit(PICTURE, (0, 0))
    pygame.display.update()

def main():
    """Main function to run the game loop."""
    if PICTURE is None or SONG is None:
        print("Missing essential resources. Exiting...")
        return

    pygame.mixer.music.play(-1)  # Play music in a loop

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw()

    pygame.quit()

if __name__ == '__main__':
    main()
