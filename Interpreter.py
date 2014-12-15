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
        self.mainMemory = MemoryStack(Memory('main'))
        self.functionMemory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        print "binary expr"
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
        print "decl list"
        for decl in node.declarations:
            decl.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        print 'declaration'

        # declarationList = []
        for init in node.inits:
            # declarationList.append(init.accept(self))

            initResult = init.accept(self)
            # print initResult[1]
            self.mainMemory.insert(initResult[0], initResult[1])

            # return declarationList

    @when(AST.Init)
    def visit(self, node):
        print "init"
        name = node.name
        expression = node.expression.accept(self)

        return (name, expression)

    # @when(AST.Assignment)
    # def visit(self, node):



    @when(AST.Function_list)
    def visit(self, node):
        print "fundefs"

        for fundef in node.functions:
            fundef.accept(self)


    @when(AST.Function)
    def visit(self, node):
        print 'fundef'

        # tmp_fun = AST.Function(node.type, node.name, node.arguments, node.comp, node.lineno)
        # self.mainMemory.insert(tmp_fun.name, tmp_fun)


    @when(AST.Instruction_list)
    def visit(self, node):

        print 'instruction list'

        for instr in node.instructions:
            instr.accept(self)


    @when(AST.PrintInstruction)
    def visit(self, node):
        print "Print instruction"

        node.expression.accept(self)

    @when(AST.LabeledInstruction)
    def visit(self, node):

        print "Labeled instruction"
        node.instruction.accept(self)

    @when(AST.Assignment)
    def visit(self, node):

        print "Assignment"

        value = node.expression.accept(self)

        if not self.functionMemory.set(node.name, value):
            self.mainMemory.set(node.name, value)

        return value

    @when(AST.Variable)
    def visit(self, node):

        print "Variable"

        value = self.functionMemory.get(node.name)

        if value is None:
            return self.mainMemory.get(node.name)

        return value

    @when(AST.Function_call)
    def visit(self, node):

        print "Function_call"

        function = self.mainMemory.get(node.name)
        argValues = node.expressions.accept(self)

        self.functionMemory.push(Memory(node.name))



        value = 0

        return value

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

    #
    # # simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()