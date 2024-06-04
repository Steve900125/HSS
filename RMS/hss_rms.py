class RMSProgram:
    def __init__(self, Bmax, beta):
        self.Bmax = Bmax
        self.beta = beta
        self.instructions = []
        self.memory = {}
        self.id_counter = 0

    def load(self, x, w):
        self.memory[w] = x
        self.instructions.append(('load', self.id_counter, x, w))
        self.id_counter += 1

    def add(self, u, v, w):
        if self.id_counter > max(self._get_instruction_id(u), self._get_instruction_id(v)):
            self.memory[w] = self.memory[u] + self.memory[v]
            self.instructions.append(('add', self.id_counter, u, v, w))
            self.id_counter += 1
        else:
            raise ValueError("Instruction order violated.")

    def mult(self, x, v, w):
        if self.id_counter > self._get_instruction_id(v):
            self.memory[w] = x * self.memory[v]
            self.instructions.append(('mult', self.id_counter, x, v, w))
            self.id_counter += 1
        else:
            raise ValueError("Instruction order violated.")

    def output(self, w):
        value = self.memory[w]
        if abs(value) > self.Bmax:
            return None
        return value % self.beta

    def _get_instruction_id(self, wire):
        for inst in self.instructions:
            if inst[-1] == wire:
                return inst[1]
        return -1

    def execute(self):
        for inst in self.instructions:
            op = inst[0]
            if op == 'load':
                _, _, x, w = inst
                self.memory[w] = x
            elif op == 'add':
                _, _, u, v, w = inst
                self.memory[w] = self.memory[u] + self.memory[v]
            elif op == 'mult':
                _, _, x, v, w = inst
                self.memory[w] = x * self.memory[v]
            elif op == 'out':
                _, _, w = inst
                print(self.output(w))


if __name__ == "__main__":
    Bmax = 10
    beta = 2

    program = RMSProgram(Bmax, beta)
    program.load(1, 'w1')
    program.load(2, 'w2')
    program.add('w1', 'w2', 'w3')
    program.mult(3, 'w3', 'w4')
    print(program.output('w4'))