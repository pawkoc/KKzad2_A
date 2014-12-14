
class Node(object):

    def __str__(self):
        return self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return '[%s]' % ', '.join(map(str, [self.op, str(self.left), str(self.right)]))

class Program(Node):

    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions

    def __str__(self):
        # return [self.declarations, self.fundefs, self.instructions]
        return str([str(self.declarations), str(self.fundefs), str(self.instructions)])

class Const(Node):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Integer(Const):
    pass
    #...


class Float(Const):
    pass
    #...


class String(Const):
    pass
    #...


class Variable(Node):
    pass
    #...

class Instruction(Node):

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __str__(self):
        return str([str(self.name), str(self.expr)])


class Instruction_list(Node):

    def __init__(self):
        self.instructions = []

    def addInstruction(self, instruction):
        self.instructions = self.instructions + [instruction]

    def __str__(self):
        lista = []
        for i in self.instructions:
            lista.append(str(i))
        return ' '.join(lista)


class Expression_list(Node):

    def __init__(self):
        self.expressions = []

    def addExpression(self, expression):
        self.expressions.append(expression)

    def __str__(self):
        lista = []
        for i in self.expressions:
            lista.append(str(i))
        return ' '.join(lista)

# ...

class Function(Node):

    def __init__(self, type, name, arguments):
        self.type = type
        self.name = name
        self.arguments = arguments
        # self.instructions = instructions

    def __str__(self):
        return str((self.type, self.name, str(self.arguments)))

class Function_list(Node):

    def __init__(self):
        self.functions = []

    def addFunction(self, function):
        self.functions.append(function)

    def __str__(self):
        return '[%s]' % ', '.join(map(str, self.functions))


# One line of declarations
class Declaration(Node):

    def __init__(self, type):
        self.type = type
        self.inits = []

    def addInit(self, name, val):
        self.inits.append(BinExpr(left=name, op='=', right=val))

    def __str__(self):
        return str((self.type, '[%s]' % ', '.join(map(str, self.inits))))


class Declaration_list(Node):

    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)

    def __str__(self):
        return '[%s]' % ', '.join(map(str, self.declarations))

class Compound_instr(Node):

    def __init__(self):
        self.declaration_list = Declaration_list()
        self.instruction_list = Instruction_list()

    def addDeclaration(self, declaration):
        self.declaration_list.declarations.append(declaration)

    def addInstruction(self, instruction):
        self.instruction_list.instructions.append(instruction)

    def __str__(self):
        return str((str(self.declaration_list), str(self.instruction_list)))

# class Scope(Node):
#
#     def __init__(self):
#         self.declarations = []
#         self.instructions = []
#         self.symbols = {}
