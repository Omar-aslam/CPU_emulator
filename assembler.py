import re

# Instruction mapping
INSTRUCTIONS = {
    "LOAD": 0x01,
    "STORE": 0x02,
    "ADD": 0x03,
    "SUB": 0x04,
    "CMP": 0x07,
    "JEQ": 0x08,
    "JUMP": 0x05,
    "JNE": 0x09,
    "HALT": 0xFF
}

# Register mapping
REGISTERS = {
    "R0": 0, "R1": 1, "R2": 2, "R3": 3
}

def assemble(file_path):
    """
    Convert an assembly file into machine code.

    :param file_path: Path to the assembly file (e.g., 'game.asm').
    :return: List of machine code instructions.
    """
    machine_code = []  # Store the resulting machine code
    labels = {}        # Store label addresses for jumps
    lines_cleaned = [] # Store cleaned lines for processing

    # Open and read the assembly file
    with open(file_path, "r") as asm_file:
        lines = asm_file.readlines()

    # First pass: Identify labels and their memory addresses
    address = 0
    for line in lines:
        # Clean up line: remove comments and whitespace
        line = line.split("#")[0].strip()
        if not line:  # Skip empty lines
            continue
        if ":" in line:  # Label definition
            label = line.replace(":", "").strip()
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")
            labels[label] = address  # Map label to the current address
            continue
        lines_cleaned.append(line)  # Save cleaned line for second pass
        # Increment address based on instruction and operand count
        address += 1 + len(line.split()) - 1

    # Debug: Print identified labels
    print(f"Labels identified: {labels}")

    # Second pass: Translate instructions to machine code
    for line in lines_cleaned:
        parts = line.split()
        instruction = parts[0]
        opcode = INSTRUCTIONS.get(instruction)
        if opcode is None:
            raise ValueError(f"Unknown instruction: {instruction}")
        machine_code.append(opcode)  # Add opcode to machine code

        # Process operands
        for part in parts[1:]:
            part = part.strip(",")  # Remove trailing commas
            print(f"Processing operand: {part}")  # Debugging line
            if part in REGISTERS:  # Check if operand is a register
                machine_code.append(REGISTERS[part])
            elif part.startswith("0x"):  # Hexadecimal literal
                machine_code.append(int(part, 16))
            elif part.isdigit():  # Decimal literal
                machine_code.append(int(part))
            elif part in labels:  # Label reference
                machine_code.append(labels[part])
            else:
                raise ValueError(f"Unknown operand: {part}")

    return machine_code

if __name__ == "__main__":
    """
    Assemble the 'game.asm' file into machine code and save it as 'game.bin'.
    """
    try:
        machine_code = assemble("game.asm")
        print(f"Machine Code: {machine_code}")
        with open("game.bin", "wb") as bin_file:
            bin_file.write(bytearray(machine_code))
        print("Assembly successful! Machine code saved to 'game.bin'.")
    except Exception as e:
        print(f"Error during assembly: {e}")
