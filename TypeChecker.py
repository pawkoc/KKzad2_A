#!/usr/bin/python

from SymbolTable import SymbolTable
import AST

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.ttype = {'+': {'string': {'string': 'string'},
                            'int': {'float': 'float',
                                    'int': 'int'},
                            'float': {'int': 'float',
                                      'float': 'float'}},
                      '-': {'int': {'int': 'int',
                                    'float': 'float'},
                            'float': {'int': 'float',
                                      'float': 'float'}},
                      '*': {'string': {'int': 'string'},
                            'int': {'int': 'int',
                                    'float': 'float'},
                            'float': {'int:': 'float' ,
                                      'float': 'float'}},
                      '/': {'int': {'int': 'int',
                                    'float': 'float'},
                            'float': {'float': 'float'} },
                      '!=': {'string': {'string': 'int'},
                             'int': {'float': 'int',
                                     'int': 'int'},
                             'float': {'int': 'int',
                                       'float': 'int'}},
                      '<': {'string': {'string': 'int'},
                            'int': {'float': 'int',
                                    'int': 'int'},
                            'float': {'int': 'int',
                                      'float': 'int'}},
                      '<=': {'string': {'string': 'int'},
                             'int': {'float': 'int',
                                     'int': 'int'},
                             'float': {'int': 'int',
                                       'float': 'int'}},
                      '>': {'string': {'string': 'int'},
                            'int': {'float': 'int',
                                    'int': 'int'},
                            'float': {'int': 'int',
                                      'float': 'int'}},
                      '>=': {'string': {'string': 'int'},
                             'int': {'float': 'int',
                                     'int': 'int'},
                             'float': {'int': 'int',
                                       'float': 'int'}},
                      '==': {'string': {'string': 'int'},
                             'int': {'float': 'int',
                                     'int': 'int'},
                             'float': {'int': 'int',
                                       'float': 'int'}},
                      '%': {'int': {'int': 'int'}},
                      '^': {'int': {'int': 'int'}},
                      '&': {'int': {'int': 'int'}},
                      'AND': {'int': {'int': 'int'}},
                      'OR': {'int': {'int': 'int'}},
                      'SHL': {'int': {'int': 'int'}},
                      'SHR': {'int': {'int': 'int'}},
                      'EQ': {'int': {'int': 'int'}},
                      'NEQ': {'int': {'int': 'int'}},
                      'LE': {'int': {'int': 'int'}},
                      'GE': {'int': {'int': 'int'}}
                      }

    def visit_BinExpr(self, node):
        node.left.vars = node.vars
        node.right.vars = node.vars       # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        if type1 == -1 or type2 == -1:
            return -1
        if self.ttype.get(op) != None:
            if self.ttype[op].get(type1) != None:
                if self.ttype[op][type1].get(type2) != None:
                    return self.ttype[op][type1][type2]
        print 'ERROR: Invalid operand\'s type, line ' + str(node.lineno)
        print str(node), type1, type2
        # print node.__class__.__name__
        return -1


    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Program(self, node):
        node.vars = SymbolTable(None)
        node.declarations.vars = node.vars
        node.instructions.vars = node.vars
        node.fundefs.vars = SymbolTable(node.vars)
        self.visit(node.declarations)
        self.visit(node.fundefs)
        self.visit(node.instructions)

    def visit_Const(self, node):
        return node.value
        #print node.value
        #node.value.vars = node.vars
        #return self.visit(node.value)

    def visit_Variable(self, node):
        # print node.name, node.vars.get(node.name)
        return node.vars.get(node.name)

    def visit_Instruction(self, node):
        if node.expr != None:
            node.expr.vars = node.vars
            self.visit(node.expr)

    def visit_Instruction_list(self, node):
        if node.instructions != None:
            for instr in node.instructions:
                instr.vars = node.vars
                self.visit(instr)

    def visit_Expression_list(self, node):
        pass

    def visit_Function(self, node):
        # uzupelnic symbol table
        if node.comp != None:
            node.comp.vars = SymbolTable(node.vars)
            self.visit(node.comp)

    def visit_Function_list(self, node):
        if node.functions != None:
            for func in node.functions:
                func.vars = node.vars
                self.visit(func)

    def visit_Declaration(self, node):
        if node.inits != None:
            for init in node.inits:
                init.vars = node.vars
                name = self.visit(init)
                if name != -1:
                    node.vars.put(name, node.type)
                # print ' ' + name, node.type

    def visit_Declaration_list(self, node):
        if node.declarations != None:
            for dec in node.declarations:
                dec.vars = node.vars
                self.visit(dec)

    def visit_Compound_instr(self, node):
        if node.instruction_list != None:
            node.instruction_list.vars = node.vars
        if node.declaration_list != None:
            node.declaration_list.vars = node.vars
        self.visit(node.declaration_list)
        self.visit(node.instruction_list)

    def visit_Assignment(self, node):
        node.expression.vars = node.vars
        type2 = self.visit(node.expression)
        # print type1, type2
        type1 = node.vars.get(node.name)
        if type1 != -1 and type2 != -1:
            if type1 == type2:
                return type1
        if type1 == -1:
            print 'ERROR: Undeclared variable, line %s' % node.lineno
            return -1
        print 'ERROR: Type mismatch, line %s' % node.lineno
        return -1

    def visit_Init(self, node):
        collision = node.vars.collision(node.name)
        # print node.vars.dictionary
        if collision:
            print 'ERROR: Variable already declared, line ' + str(node.lineno)
            return -1
        return node.name

    #def visit_
