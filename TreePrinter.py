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
    def printTree(self):
        pass

    @addToClass(AST.Program)
    def printTree(self, indent):
        result = ""
        if self.declarations != None:
            result += "DECL\n"
            result += addIndent(indent)
            result += self.declarations.printTree(indent)
        result += addIndent(indent)
        result += self.fundefs.printTree(indent)
        result += addIndent(indent)
        result += self.instructions.printTree(indent)
        return result

    @addToClass(AST.Declaration_list)
    def printTree(self, indent):
        result = ""
        if self.declarations != None:
            result += self.declarations.printTree(indent)
        if self.declaration != None:
            result += self.declaration.printTree(indent)
        return result

    @addToClass(AST.Declaration)
    def printTree(self, indent):
        result = ""
        if self.inits is None:
            result =+ self.type
        result += self.inits.printTree(indent)
        return result

    @addToClass(AST.Const)
    def printTree(self):
        pass

    @addToClass(AST.Instruction_list)
    def printTree(self):
        pass

    @addToClass(AST.Instruction)
    def printTree(self):
        pass

    @addToClass(AST.Expression_list)
    def printTree(self):
        pass

    @addToClass(AST.Function_list)
    def printTree(self):
        pass

    @addToClass(AST.Function)
    def printTree(self):
        pass

    @addToClass(AST.PrintInstruction)
    def printTree(self):
        pass

    @addToClass(AST.LabeledInstruction)
    def printTree(self):
        pass

    @addToClass(AST.ChoiceInstruction)
    def printTree(self):
        pass

    @addToClass(AST.WhileInstruction)
    def printTree(self):
        pass

    @addToClass(AST.RepeatInstruction)
    def printTree(self):
        pass

    @addToClass(AST.ReturnInstruction)
    def printTree(self):
        pass

    @addToClass(AST.ContinueInstruction)
    def printTree(self):
        pass

    @addToClass(AST.BreakInstruction)
    def printTree(self):
        pass

