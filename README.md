# CPU Emulator & Game Assembler

## Project Overview

This project demonstrates a complete toolchain for a simple game powered by a custom CPU emulator and assembler implemented in Python. The system consists of three main components:

- Assembler (assembler.py):
  Converts game assembly code (from `game.asm`) into binary machine code (`game.bin`).

- CPU Emulator (cpu_emulator.py): 
  Simulates a CPU with basic instructions such as LOAD, STORE, arithmetic operations, jumps, and comparisons. It loads the machine code, processes instructions, and manages registers and memory.

- Graphics & Game Integration (graphics.py):  
  Uses Pygame to create a game window where game elements are drawn and controlled via the CPU emulator.

> **Note:** This project is still under development. Some features may be incomplete or subject to change.



## Features

- Assembler: 
  Reads assembly instructions from `game.asm`, resolves labels, and outputs machine code to `game.bin`.

- CPU Emulator:
  Supports a small instruction set including LOAD, STORE, ADD, SUB, CMP, jumps, and HALT. It maintains registers, memory, a program counter, and flags.

- Graphics & Game Integration:  
  Renders the game window using Pygame. The game uses CPU memory values (e.g., snake position, food position, score) to control and display game elements.

## Technical Explanation
Assembler (assembler.py):

Uses regular expressions and simple parsing techniques to convert assembly into machine code.

Resolves labels for jump instructions and supports a basic instruction set (LOAD, STORE, ADD, SUB, JUMP, CMP, JEQ, JNE, HALT).

CPU Emulator (cpu_emulator.py):

Implements a basic CPU with four general-purpose registers and 256 bytes of memory.

Executes instructions by performing fetch–decode–execute cycles.

Handles errors like division by zero and out-of-bounds memory access.

Graphics & Game Integration (graphics.py):

Creates a game window with Pygame.

Uses CPU memory to control game behavior (e.g., snake movement, food placement, score tracking).

Integrates keyboard input to control game variables.

Modular Design & Future Improvements:

The project is split into distinct components to enhance maintainability and clarity.

Future work will include adding more instructions, refining game logic, and improving error handling.

**Under Development
This project is still under development. Expect additional features, refinements, and potential changes in the near future.**

