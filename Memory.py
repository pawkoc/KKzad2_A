

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.values = {}

    def has_key(self, name):  # variable name
        return name in self.values

    def get(self, name):         # get from memory current value of variable <name>
        return self.values.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.values[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        stack = []
        if memory != None:
            stack.append(memory)

    def get(self, name):             # get from memory stack current value of variable <name>
        for i in reversed(xrange(len(stack))):
            if stack[i].has_key(name):
                return stack[i].get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for i in reversed(xrange(len(stack))):
            if stack[i].has_key(name):
                stack[i].put(name, value)
                return

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()

