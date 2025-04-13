import pygame
from cpu_emulator import CPU

# Pygame initialization
pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with CPU Emulator")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Initialize CPU
cpu = CPU()

def reset_cpu(cpu):
    """
    Resets the CPU state and initializes game-specific memory.
    """
    cpu.reset()  # Reset CPU state
    # Initialize game-specific memory
    cpu.memory[0xF1] = 5  # Snake head Y-coordinate
    cpu.memory[0xF2] = 5  # Snake head X-coordinate
    cpu.memory[0xF3] = 10  # Food Y-coordinate
    cpu.memory[0xF4] = 15  # Food X-coordinate
    cpu.memory[0xFA] = 0   # Initial score
    cpu.memory[0xF0] = 0   # No movement initially
    print("CPU reset and memory initialized.")

# Load the game program
try:
    with open("game.bin", "rb") as bin_file:
        program = list(bin_file.read())
        cpu.load_program(program)
except FileNotFoundError:
    print("Error: game.bin not found. Ensure the file is in the same directory.")
    pygame.quit()
    exit()

# Initialize memory
reset_cpu(cpu)

# Main game loop
running = True
while running:
    try:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capture input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cpu.memory[0xF0] = 1  # UP
        elif keys[pygame.K_DOWN]:
            cpu.memory[0xF0] = 2  # DOWN
        elif keys[pygame.K_LEFT]:
            cpu.memory[0xF0] = 3  # LEFT
        elif keys[pygame.K_RIGHT]:
            cpu.memory[0xF0] = 4  # RIGHT
        elif keys[pygame.K_r]:  # Restart
            print("Restarting game...")
            reset_cpu(cpu)
            cpu.load_program(program)  # Reload program after reset
            continue
        else:
            cpu.memory[0xF0] = 0  # No movement

        # Run the CPU for a fixed number of cycles
        for _ in range(10):  # Limit execution cycles per frame to avoid infinite loops
            if cpu.running:
                cpu.run(max_cycles=1000)  # Run up to 1000 cycles
            else:
                print("CPU halted; resetting for the next cycle.")
                reset_cpu(cpu)
                cpu.load_program(program)  # Reload program after reset
                break

        # Render the screen
        screen.fill(BLACK)

        # Draw snake
        snake_x = cpu.memory[0xF2] * GRID_SIZE
        snake_y = cpu.memory[0xF1] * GRID_SIZE
        pygame.draw.rect(screen, GREEN, (snake_x, snake_y, GRID_SIZE, GRID_SIZE))

        # Draw food
        food_x = cpu.memory[0xF4] * GRID_SIZE
        food_y = cpu.memory[0xF3] * GRID_SIZE
        pygame.draw.rect(screen, RED, (food_x, food_y, GRID_SIZE, GRID_SIZE))

        # Display score
        score = cpu.memory[0xFA]
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(10)

    except Exception as e:
        print(f"Error: {e}")
        running = False

# Quit the game
pygame.quit()
