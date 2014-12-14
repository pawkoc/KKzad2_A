import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def addIndent(indent):
    result = ""
    i = 0
    while i < indent:
        result += "| "
        i += 1
    return result

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Node)
    def printTree(self, indent):

        result = addIndent(indent)
        return result


    @addToClass(AST.BinExpr)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent)
        result += str(self.op) + "\n"
        result += self.left.printTree(indent+1)
        result += self.right.printTree(indent+1)

        return result

    @addToClass(AST.Program)
    def printTree(self, indent):

        result = ""
        if self.declarations != None:
            # result += "DECL\n"
            result += self.declarations.printTree(indent)

        if self.fundefs != None:
            result += "FUNDEFS\n"
            result += self.fundefs.printTree(indent)

        if self.instructions != None:
            # result += "INSTRUCTIONS\n"
            result += self.instructions.printTree(indent)

        return result

    @addToClass(AST.Declaration_list)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent)
        result += "DECL\n"

        for decl in self.declarations:
            result += decl.printTree(indent+1)

        return result

    @addToClass(AST.Declaration)
    def printTree(self, indent):
        result = ""

        for init in self.inits:
            result += addIndent(indent)
            result += "=\n"
            result += init.printTree(indent+1)

        return result

    @addToClass(AST.Init)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent)
        result += str(self.name) + '\n'
        result += self.expression.printTree(indent)

        return result

    @addToClass(AST.Const)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent)
        result += str(self.value) + "\n"

        return result

    @addToClass(AST.Instruction_list)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent)
        result += "INSTRUCTIONS\n"

        for instr in self.instructions:
            result += instr.printTree(indent+1)

        return result

    # @addToClass(AST.Instruction)
    # def printTree(self, indent):
    #     result = ""
    #
    #     for init in self.inits:
    #         result += addIndent(indent)
    #         result += "=\n"
    #         result += init.printTree(indent+1)
    #
    #     return "foobar"

    @addToClass(AST.Expression_list)
    def printTree(self, indent):
        result = ""

        for expr in self.expressions:
            result += expr.printTree(indent+1)

        return result

    @addToClass(AST.Function_list)
    def printTree(self, indent):
        result = ""

        for fun in self.functions:
            # result += addIndent(indent) + "\n"
            result += fun.printTree(indent+1)

        return result

    @addToClass(AST.Function)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + str(self.name) + "\n"
        result += addIndent(indent) + "RET " + str(self.type) + "\n"

        for arg in self.arguments:
            result += addIndent(indent) + "ARG " + arg[1] + "\n"

        result += self.comp.printTree(indent+1)

        return result

    @addToClass(AST.Variable)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + str(self.name) + "\n"

        return result

    @addToClass(AST.Compound_instr)
    def printTree(self, indent):
        result = ""

        declarations = self.declaration_list
        instructions = self.instruction_list

        result += declarations.printTree(indent)
        result += instructions.printTree(indent)

        return result

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "PRINT\n"
        result += self.expression.printTree(indent+1)

        return result

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + ":\n"
        result += addIndent(indent) + str(self.id) + "\n"
        result += self.instruction.printTree(indent+1)

        return result

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "IF\n"
        result += self.condition.printTree(indent+1)
        result += self.instruction.printTree(indent+1)

        if(self.elseinstruction != None):
            result += addIndent(indent) + "ELSE\n"
            result += self.elseinstruction.printTree(indent+1)

        return result

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "WHILE\n"
        result += self.condition.printTree(indent+1)
        result += self.instruction.printTree(indent+1)

        return result

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "REPEAT\n"
        result += self.instructions.printTree(indent+1)
        result += addIndent(indent) + "UNTIL\n"
        result += self.condition.printTree(indent+1)

        return result

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "return\n"
        result += self.expression.printTree(indent+1)

        return result

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent):
        return addIndent(indent) + "continue\n"

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent):
        return addIndent(indent) + "break\n"

    @addToClass(AST.Function_call)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + "FUNCALL" + "\n"
        result += addIndent(indent+1) + str(self.name) + "\n"
        result += self.expressions.printTree(indent+1)

        return result


    @addToClass(AST.Assignment)
    def printTree(self, indent):
        result = ""

        result += addIndent(indent) + ":=\n"
        result += addIndent(indent+1) + str(self.name) + "\n"
        result += self.expression.printTree(indent+1)

        return result
