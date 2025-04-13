class CPU:
    def __init__(self):
        """
        Initialize the CPU with:
        - 4 general-purpose registers (R0, R1, R2, R3).
        - 256 bytes of memory.
        - A program counter (PC) to track the current instruction.
        - A running state to determine if the CPU should continue execution.
        - Flags for comparison results (e.g., EQ, NE).
        """
        self.registers = [0] * 4  # Registers: R0, R1, R2, R3
        self.memory = [0] * 256  # Memory: 256 bytes initialized to 0
        self.pc = 0              # Program Counter (starts at 0)
        self.running = True      # CPU running state
        self.flags = {"EQ": False, "NE": False}  # Flags for comparisons

    def load_program(self, program):
        """
        Load a program (list of bytes) into memory.
        The program starts at memory address 0.

        :param program: List of byte instructions to load.
        """
        if len(program) > len(self.memory):
            raise ValueError("Program size exceeds memory size.")
        self.memory[:len(program)] = program  # Copy program into memory
        print(f"Program loaded into memory: {self.memory[:len(program)]}")

    def reset(self):
        """
        Reset the CPU state for continuous execution.
        """
        self.pc = 0
        self.running = True
        self.registers = [0] * 4
        self.flags = {"EQ": False, "NE": False}
        self.memory = [0] * 256
        print("CPU reset for continuous execution.")

    def fetch(self):
        """
        Fetch the next instruction from memory based on the Program Counter (PC).
        Halt the CPU if PC is out of bounds.

        :return: The instruction byte.
        """
        if self.pc >= len(self.memory):
            print(f"Error: PC={self.pc} out of bounds. Halting CPU.")
            self.running = False
            return 0xFF  # HALT instruction on error
        instruction = self.memory[self.pc]
        print(f"Fetching instruction at PC={self.pc}: {instruction}")
        self.pc += 1
        return instruction

    def decode_and_execute(self, instruction):
        """
        Decode and execute the fetched instruction.
        """
        print(f"Executing instruction: {instruction}")
        try:
            if instruction == 0x01:  # LOAD Rx, Addr
                reg = self.fetch()
                addr = self.fetch()
                if addr >= len(self.memory):
                    raise ValueError(f"LOAD error: Address {addr} out of bounds.")
                self.registers[reg] = self.memory[addr]
                print(f"LOAD: R{reg} = {self.memory[addr]} from address {addr}")
            elif instruction == 0x02:  # STORE Rx, Addr
                reg = self.fetch()
                addr = self.fetch()
                if addr >= len(self.memory):
                    raise ValueError(f"STORE error: Address {addr} out of bounds.")
                self.memory[addr] = self.registers[reg]
                print(f"STORE: Memory[{addr}] = {self.registers[reg]}")
            elif instruction == 0x03:  # ADD Rx, Ry
                reg1 = self.fetch()
                reg2 = self.fetch()
                self.registers[reg1] += self.registers[reg2]
                print(f"ADD: R{reg1} = {self.registers[reg1]}")
            elif instruction == 0x04:  # SUB Rx, Ry
                reg1 = self.fetch()
                reg2 = self.fetch()
                self.registers[reg1] -= self.registers[reg2]
                print(f"SUB: R{reg1} = {self.registers[reg1]}")
            elif instruction == 0x05:  # JUMP Addr
                addr = self.fetch()
                if addr >= len(self.memory):
                    raise ValueError(f"JUMP error: Address {addr} out of bounds.")
                self.pc = addr
                print(f"JUMP: PC = {addr}")
            elif instruction == 0x07:  # CMP Rx, Ry
                reg1 = self.fetch()
                reg2 = self.fetch()
                self.flags["EQ"] = self.registers[reg1] == self.registers[reg2]
                self.flags["NE"] = self.registers[reg1] != self.registers[reg2]
                print(f"CMP: EQ={self.flags['EQ']}, NE={self.flags['NE']}")
            elif instruction == 0x08:  # JEQ Addr
                addr = self.fetch()
                if self.flags["EQ"]:
                    if addr >= len(self.memory):
                        raise ValueError(f"JEQ error: Address {addr} out of bounds.")
                    self.pc = addr
                    print(f"JEQ: PC = {addr}")
            elif instruction == 0x09:  # JNE Addr
                addr = self.fetch()
                if self.flags["NE"]:
                    if addr >= len(self.memory):
                        raise ValueError(f"JNE error: Address {addr} out of bounds.")
                    self.pc = addr
                    print(f"JNE: PC = {addr}")
            elif instruction == 0x00:  # NOP (No Operation)
                    print("NOP: No operation executed.")
            elif instruction == 0xFF:  # HALT
                self.running = False
                print("HALT: CPU Stopped")
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
        except Exception as e:
            print(f"Error during execution: {e}")
            self.running = False

    def run(self, max_cycles=1000):
        """
        Run the CPU until a HALT (0xFF) instruction is encountered or an error occurs.
        """
        cycle_count = 0
        while self.running and cycle_count < max_cycles:
            try:
                instruction = self.fetch()
                self.decode_and_execute(instruction)
                cycle_count += 1
            except Exception as e:
                print(f"Execution error: {e}")
                self.running = False
        if cycle_count >= max_cycles:
            print("Max cycles reached. Halting CPU.")

# Example usage
if __name__ == "__main__":
    cpu = CPU()
    program = [
        0x01, 0x00, 0x10,  # LOAD R0, 0x10
        0x01, 0x01, 0x11,  # LOAD R1, 0x11
        0x07, 0x00, 0x01,  # CMP R0, R1
        0x08, 0x12,        # JEQ 0x12
        0x05, 0x00,        # JUMP to 0x00
        0xFF               # HALT
    ]
    cpu.load_program(program)
    cpu.memory[0x10] = 42
    cpu.memory[0x11] = 42
    cpu.run(max_cycles=100)
    print(f"Final Registers: {cpu.registers}")
    print(f"Final Flags: {cpu.flags}")
