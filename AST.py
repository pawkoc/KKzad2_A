
class Node(object):

    def __str__(self):
        return self.printTree(0)
        # return "ALA120"

    def accept(self, visitor):
        return visitor.visit(self)


class BinExpr(Node):

    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

    # def __str__(self):
    #     return '[%s]' % ', '.join(map(str, [self.op, str(self.left), str(self.right)]))

class Program(Node):

    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions

    # def __str__(self):
    #     return str([str(self.declarations), str(self.fundefs), str(self.instructions)]).replace('\\', '')

class Const(Node):

    def __init__(self, value):
        self.value = value

    # def __str__(self):
    #     return self.value

class Integer(Const):
    pass

class Float(Const):
    pass

class String(Const):
    pass


class Variable(Node):

    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

    # def __str__(self):
    #     return str(self.name)


# class Instruction(Node):
#
#     def __init__(self, name, expr):
#         self.name = name
#         self.expr = expr
#
#     # def __str__(self):
#     #     return str([str(self.name), str(self.expr)])


class Instruction_list(Node):

    def __init__(self):
        self.instructions = []

    def addInstruction(self, instruction):
        self.instructions.append(instruction)

    # def __str__(self):
    #     lista = []
    #     for i in self.instructions:
    #         lista.append(str(i))
    #     return ' '.join(lista)


class PrintInstruction(Node):
    def __init__(self,lineno, expression):
        self.lineno = lineno
        self.expression = expression

    # def __str__(self):
    #     return str(('PRINT', str(self.expression)))

class LabeledInstruction(Node):
    def __init__(self,lineno, id, instruction):
        self.lineno = lineno
        self.id = id
        self.instruction = instruction

    # def __str__(self):
    #     return str(('LABELED', str(self.id), str(self.instruction)))


class ChoiceInstruction(Node):
    def __init__(self,lineno, condition, instruction, elseinstruction = None):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction
        self.elseinstruction = elseinstruction

    # def __str__(self):
    #
    #     if(self.elseinstruction == None):
    #         return str(('IF', str(self.condition), str(self.instruction)))
    #
    #     else:
    #         return str(('IF', str(self.condition), str(self.instruction), 'ELSE', str(self.elseinstruction)))

class WhileInstruction(Node):
    def __init__(self,lineno, condition, instruction):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction

    # def __str__(self):
    #     return str(('WHILE', str(self.condition), str(self.instruction)))

class RepeatInstruction(Node):
    def __init__(self,lineno, instructions, condition):
        self.lineno = lineno
        self.instructions = instructions
        self.condition = condition

    # def __str__(self):
    #     return str(('REPEAT', str(self.expression), 'UNTIL', str(self.condition)))

class ReturnInstruction(Node):
    def __init__(self, lineno, expression):
        self.lineno = lineno
        self.expression = expression

    # def __str__(self):
    #     return str(('RETURN', str(self.expression)))

class ContinueInstruction(Node):
    pass
    # def __str__(self):
    #     return 'CONTINUE'

class BreakInstruction(Node):
    pass
    # def __str__(self):
    #     return 'BREAK'



class Expression_list(Node):

    def __init__(self):
        self.expressions = []

    def addExpression(self, expression):
        self.expressions.append(expression)

    # def __str__(self):
    #     # lista = []
    #     # for i in self.expressions:
    #     #     lista.append(str(i))
    #     # return ' '.join(lista)
    #     return '[%s]' % ', '.join(map(str, self.expressions))


class Function(Node):

    def __init__(self, type, name, arguments, comp, lineno):
        self.type = type
        self.name = name
        self.arguments = arguments
        self.comp = comp
        self.lineno = lineno
        # self.instructions = instructions

    # def __str__(self):
    #     return str((self.type, self.name, str(self.arguments), str(self.comp)))

class Function_list(Node):

    def __init__(self):
        self.functions = []

    def addFunction(self, function):
        self.functions.append(function)

    # def __str__(self):
    #     return '[%s]' % ', '.join(map(str, self.functions))


class Assignment(Node):

    def __init__(self, name, expression, lineno):
        self.lineno = lineno
        self.name = name
        self.expression = expression

    # def __str__(self):
    #     return '[=, %s, %s]' % (str(self.name), self.expression.__str__())


class Init(Node):

    def __init__(self, name, expression, lineno):
        self.name = name
        self.expression = expression
        self.lineno = lineno

    # def __str__(self):
    #     return '[=, %s, %s]' % (str(self.name), self.expression.__str__())


# One line of declarations
class Declaration(Node):

    def __init__(self, type):
        self.type = type
        self.inits = []

    def addInit(self, name, val, lineno):
        self.inits.append(Init(name, val, lineno))#BinExpr(left=name, op='=', right=val))

    # def __str__(self):
    #     return str((self.type, '[%s]' % ', '.join(map(str, self.inits))))


class Declaration_list(Node):

    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)

    # def __str__(self):
    #     return '[%s]' % ', '.join(map(str, self.declarations))

class Compound_instr(Node):

    def __init__(self):
        self.declaration_list = Declaration_list()
        self.instruction_list = Instruction_list()

    def addDeclaration(self, declaration):
        self.declaration_list.declarations.append(declaration)

    def addInstruction(self, instruction):
        self.instruction_list.instructions.append(instruction)

    # def __str__(self):
    #     return str((str(self.declaration_list), str(self.instruction_list)))

class Function_call(Node):

    def __init__(self, lineno, name, expressions):
        self.lineno = lineno
        self.name = name
        self.expressions = expressions

    # def __str__(self):
    #
    #     return str((str(self.name), str(self.expressions)))

# class Scope(Node):
#
#     def __init__(self):
#         self.declarations = []
#         self.instructions = []
#         self.symbols = {}
