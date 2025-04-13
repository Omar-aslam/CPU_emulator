# -------------------------
# Snake Game Assembly Code
# -------------------------

# Define NOP (No Operation)
NOP: LOAD R0, R0  # No operation

# Initialize the game state
INIT:
    LOAD R0, 1         # Set game state to running
    STORE R0, 0xFB     # Save game state to memory
    LOAD R0, 5         # Initialize snake head Y-coordinate
    STORE R0, 0xF1     # Snake head Y
    LOAD R0, 5         # Initialize snake head X-coordinate
    STORE R0, 0xF2     # Snake head X
    LOAD R0, 10        # Initialize food Y-coordinate
    STORE R0, 0xF3     # Food Y
    LOAD R0, 15        # Initialize food X-coordinate
    STORE R0, 0xF4     # Food X
    LOAD R0, 0         # Initialize score
    STORE R0, 0xFA     # Score
    LOAD R0, 0         # Initialize input direction
    STORE R0, 0xF0     # Input Direction
    JUMP MAIN_LOOP     # Start the game loop

# Main game loop
MAIN_LOOP:
    STORE R0, 0xFC    # Save current input direction (for debugging)
    STORE R1, 0xFD    # Save snake Y-coordinate (for debugging)
    STORE R2, 0xFE    # Save snake X-coordinate (for debugging)
    LOAD R0, 0xF0      # Read input direction (R0 = Memory[0xF0])
    CMP R0, 0x01       # Check if UP
    JEQ MOVE_UP
    CMP R0, 0x02       # Check if DOWN
    JEQ MOVE_DOWN
    CMP R0, 0x03       # Check if LEFT
    JEQ MOVE_LEFT
    CMP R0, 0x04       # Check if RIGHT
    JEQ MOVE_RIGHT
    JUMP MAIN_LOOP     # No valid input, repeat loop

# Move UP
MOVE_UP:
    LOAD R1, 0xF1      # Load snake Y-coordinate
    SUB R1, 0x01       # Decrement Y-coordinate
    CMP R1, 0x00       # Compare R1 with 0 (top boundary)
    JNE MOVE_UP_OK     # Valid move
    JUMP GAME_OVER     # Hit boundary, game over
MOVE_UP_OK:
    STORE R1, 0xF1     # Save updated Y-coordinate
    LOAD R0, 0         # Reset input direction
    STORE R0, 0xF0
    JUMP CHECK_FOOD

# Move DOWN
MOVE_DOWN:
    LOAD R1, 0xF1      # Load snake Y-coordinate
    ADD R1, 0x01       # Increment Y-coordinate
    CMP R1, 0x14       # Compare R1 with grid height (20)
    JNE MOVE_DOWN_OK   # Valid move
    JUMP GAME_OVER     # Hit boundary, game over
MOVE_DOWN_OK:
    STORE R1, 0xF1     # Save updated Y-coordinate
    LOAD R0, 0         # Reset input direction
    STORE R0, 0xF0
    JUMP CHECK_FOOD

# Move LEFT
MOVE_LEFT:
    LOAD R1, 0xF2      # Load snake X-coordinate
    SUB R1, 0x01       # Decrement X-coordinate
    CMP R1, 0x00       # Compare R1 with 0 (left boundary)
    JNE MOVE_LEFT_OK   # Valid move
    JUMP GAME_OVER     # Hit boundary, game over
MOVE_LEFT_OK:
    STORE R1, 0xF2     # Save updated X-coordinate
    LOAD R0, 0         # Reset input direction
    STORE R0, 0xF0
    JUMP CHECK_FOOD

# Move RIGHT
MOVE_RIGHT:
    LOAD R1, 0xF2      # Load snake X-coordinate
    ADD R1, 0x01       # Increment X-coordinate
    CMP R1, 0x14       # Compare R1 with grid width (20)
    JNE MOVE_RIGHT_OK  # Valid move
    JUMP GAME_OVER     # Hit boundary, game over
MOVE_RIGHT_OK:
    STORE R1, 0xF2     # Save updated X-coordinate
    LOAD R0, 0         # Reset input direction
    STORE R0, 0xF0
    JUMP CHECK_FOOD

# Check if food is eaten
CHECK_FOOD:
    LOAD R1, 0xF1      # Load snake Y-coordinate
    LOAD R2, 0xF3      # Load food Y-coordinate
    CMP R1, R2         # Compare Y-coordinates
    JNE MAIN_LOOP      # Not aligned in Y, continue
    LOAD R1, 0xF2      # Load snake X-coordinate
    LOAD R2, 0xF4      # Load food X-coordinate
    CMP R1, R2         # Compare X-coordinates
    JNE MAIN_LOOP      # Not aligned in X, continue
    # Food eaten, update score and reposition food
    LOAD R1, 0xFA      # Load score
    ADD R1, 0x01       # Increment score
    STORE R1, 0xFA     # Save updated score
    LOAD R1, 0x05      # New Y-coordinate for food
    STORE R1, 0xF3     # Save food Y
    LOAD R1, 0x0A      # New X-coordinate for food
    STORE R1, 0xF4     # Save food X
    JUMP MAIN_LOOP

# Handle game over state
GAME_OVER:
    LOAD R0, 0x00      # Set game state to 0 (Game Over)
    STORE R0, 0xFB     # Save game state

# Wait for restart
WAIT_RESTART:
    LOAD R0, 0xF0      # Check for restart input
    CMP R0, 0x05       # Check if input equals restart signal (5)
    JNE WAIT_RESTART   # Loop until restart signal detected
    LOAD R0, 0         # Reset input direction
    STORE R0, 0xF0
    JUMP INIT          # Restart the game
