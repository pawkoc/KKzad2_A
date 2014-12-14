import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self):
        pass
        # print 'ok'
        # print '|' + AST.BinExpr.left
        # print '|' + AST.BinExpr.right

        # ...

    @addToClass(AST.Program)
    def printTree(self):
        pass

    @addToClass(AST.Const)
    def printTree(self):
        pass
    # @addToClass ...
    # ...

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