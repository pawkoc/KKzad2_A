import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import operator

operator_map = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.div,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "%": operator.mod,
    "|": operator.or_,
    "&": operator.and_,
    "^": operator.xor,
    "&&": operator.iand,
    "||": operator.ior,
    "<<": operator.lshift,
    ">>": operator.rshift,
    "==": operator.eq,
    "!=": operator.ne
}


class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack(Memory('main'))
        self.functionMemory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return operator_map[node.op](r1, r2)

    @when(AST.Integer)
    def visit(self, node):
        return node.value

    @when(AST.Float)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Program)
    def visit(self, node):

        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)

    @when(AST.Declaration_list)
    def visit(self, node):
        # print "decl list"
        for decl in node.declarations:
            decl.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        # print 'declaration'

        for init in node.inits:

            initResult = init.accept(self)
            self.globalMemory.insert(initResult[0], initResult[1])

    @when(AST.Init)
    def visit(self, node):
        # print "init"
        name = node.name
        expression = node.expression.accept(self)

        return (name, expression)

    @when(AST.Function_list)
    def visit(self, node):
        # print "fundefs"

        for fundef in node.functions:
            self.globalMemory.insert(fundef.name, fundef)


    @when(AST.ChoiceInstruction)
    def visit(self,node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        else:
            if node.elseinstruction is not None:
                return node.elseinstruction.accept(self)
            else:
                return False

    @when(AST.Function)
    def visit(self, node):
        # print 'fundef'

        try:
            node.comp.accept(self)
        except ReturnValueException as e:
            return e.value

        # tmp_fun = AST.Function(node.type, node.name, node.arguments, node.comp, node.lineno)
        # self.globalMemory.insert(tmp_fun.name, tmp_fun)


    @when(AST.Instruction_list)
    def visit(self, node):

        # print 'instruction list'

        for instr in node.instructions:

            instr.accept(self)


    @when(AST.PrintInstruction)
    def visit(self, node):
        # print "Print instruction"

        print node.expression.accept(self)

    @when(AST.LabeledInstruction)
    def visit(self, node):

        # print "Labeled instruction"
        node.instruction.accept(self)

    @when(AST.Assignment)
    def visit(self, node):

        # print "Assignment"

        value = node.expression.accept(self)

        if not self.functionMemory.set(node.name, value):
            self.globalMemory.set(node.name, value)

        return value



    @when(AST.Variable)
    def visit(self, node):

        # print "Variable"

        value = self.functionMemory.get(node.name)

        if value is None:
            return self.globalMemory.get(node.name)

        return value

    @when(AST.Function_call)
    def visit(self, node):

        # print "Function_call"

        function = self.globalMemory.get(node.name)
        argValues = node.expressions.accept(self)

        self.functionMemory.push(Memory(node.name))

        func = self.globalMemory.get(node.name)

        for i in xrange(len(func.arguments)):
            self.functionMemory.insert(func.arguments[i][1],argValues[i])
        return func.accept(self)

    @when(AST.Expression_list)
    def visit(self, node):

        expressions = []
        for expr in node.expressions:
            expressions.append(expr.accept(self))

        return expressions

    @when(AST.Const)
    def visit(self, node):
        # k = node.value + 1
        # print "Const: %s"%k

        return node.value

    @when(AST.WhileInstruction)
    def visit(self, node):
        r = None
        try:
            while node.condition.accept(self):
                try:
                    r = node.instruction.accept(self)
                except ContinueException:
                    r = None
        except BreakException:
            r = None
        return r

    @when(AST.RepeatInstruction)
    def visit(self,node):
        r = None
        try:
            while True:
                try:
                    for instr in node.instructions:
                        r = instr.accept(self)
                except ContinueException:
                    r = None
                    # continue
                if node.condition.accept(self):
                    break
        except BreakException:
            r = None
        return r

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Compound_instr)
    def visit(self, node):
        self.globalMemory.push(Memory('compound'))
        self.functionMemory.push(Memory('compound'))
        try:
            node.declaration_list.accept(self)
            node.instruction_list.accept(self)
        except Exception as e:
            raise e
        finally:
            self.globalMemory.pop()
            self.functionMemory.pop()

    @when(AST.ReturnInstruction)
    def visit(self,node):
        raise ReturnValueException(node.expression.accept(self))