#!/usr/bin/python

from SymbolTable import VariableTable
from SymbolTable import FunctionTable
import AST

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
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
        node.left.funcs = node.funcs
        node.right.vars = node.vars
        node.right.funcs = node.funcs
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op    = node.op
        # print str(node), type1, type2
        if type1 == -1 or type2 == -1:
            return -1
        if self.ttype.get(op) != None:
            if self.ttype[op].get(type1) != None:
                if self.ttype[op][type1].get(type2) != None:
                    return self.ttype[op][type1][type2]
        print 'ERROR: Invalid operand\'s type, line ' + str(node.lineno)
        # print str(node), type1, type2
        return -1


    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Program(self, node):
        node.vars = VariableTable(None)
        node.funcs = FunctionTable()

        node.declarations.vars = node.vars
        node.declarations.funcs = node.funcs

        node.instructions.vars = node.vars
        node.instructions.funcs = node.funcs

        node.fundefs.vars = VariableTable(node.vars)
        node.fundefs.funcs = node.funcs

        err_d = self.visit(node.declarations)
        err_f = self.visit(node.fundefs)
        err_i = self.visit(node.instructions)

        return err_d or err_f or err_i

    def visit_Const(self, node):
        return node.value
        #print node.value
        #node.value.vars = node.vars
        #return self.visit(node.value)

    def visit_Variable(self, node):
        # print node.name, node.vars.get(node.name)
        col = node.vars.get(node.name)
        if col == -1:
            print 'ERROR: Undeclared variable, line %s' % node.lineno
            return -1
        return node.vars.get(node.name)

    def visit_Instruction_list(self, node):
        errors = False
        if node.instructions != None:
            for instr in node.instructions:
                instr.vars = node.vars
                instr.funcs = node.funcs
                if hasattr(node, "retType"):
                    instr.retType = node.retType
                if hasattr(node, "inLoop"):
                    instr.inLoop = True
                if self.visit(instr):
                    errors = True
        return errors

    def visit_Expression_list(self, node):
        pass

    def visit_Function(self, node):
        errors = False
        if node.comp != None:
            node.comp.vars = VariableTable(node.vars)
            for type, var in node.arguments:
                col = node.comp.vars.collision(var)
                if not col:
                    node.comp.vars.put(var, type)
                else:
                    print 'ERROR: Variable already declared, line ' + str(node.lineno)
                    errors = True
            node.comp.funcs = node.funcs
            node.comp.isFunction = True
            node.comp.retType = node.type
            if self.visit(node.comp):
                # if not node.comp.hasReturn:
                #     print 'ERROR: Function \'%s\' has no return statement, line %s' % (node.name, str(node.lineno))
                errors = True
        return errors

    def visit_Function_list(self, node):
        errors = False
        if node.functions != None:
            for func in node.functions:
                func.funcs = node.funcs
                func.vars = node.vars
                collision = node.funcs.get(func.name)
                if collision == -1:
                    node.funcs.put(func.name, func.type, func.arguments)
                else:
                    print 'ERROR: Function already declared, line ' + str(func.lineno)
                    errors = True
            for func in node.functions:
                if self.visit(func):
                    errors = True
        return errors

    def visit_Declaration(self, node):
        errors = False
        if node.inits != None:
            for init in node.inits:
                init.vars = node.vars
                init.funcs = node.funcs
                res = self.visit(init)
                if res != -1:
                    if (res[1] == 'string' and node.type == 'string') or (res[1] != 'string' and node.type != 'string'):
                        if node.type == 'int' and res[1] == 'float':
                            print 'WARNING: Implicit conversion, line %s' % (res[0].lineno)

                        node.vars.put(res[0].name, node.type)

                    else:
                        print 'ERROR: Type mismatch while assigning, line %s' % res[0].lineno
                        errors = True
                else:
                    errors = True
        return errors

    def visit_Declaration_list(self, node):
        errors = False
        if node.declarations != None:
            for dec in node.declarations:
                dec.funcs = node.funcs
                dec.vars = node.vars
                if self.visit(dec):
                    errors = True
        return errors

    def visit_Compound_instr(self, node):
        errors = False
        if hasattr(node, "isFunction"):
            vt = node.vars
            # node.hasReturn = False
            # for instr in node.instruction_list.instructions:
            #     if isinstance(instr, AST.ReturnInstruction):
            #         node.hasReturn = True
            #         break
            # if not node.hasReturn:
            #     errors = True

        else:
            vt = VariableTable(node.vars)

        if node.instruction_list != None:
            node.instruction_list.vars = vt
            node.instruction_list.funcs = node.funcs
            if hasattr(node, "retType"):
                node.instruction_list.retType = node.retType
            if hasattr(node, "inLoop"):
                node.instruction_list.inLoop = True
        if node.declaration_list != None:
            node.declaration_list.vars = vt
            node.declaration_list.funcs = node.funcs
        if self.visit(node.declaration_list):
            errors = True
        if self.visit(node.instruction_list):
            errors = True

        return errors

    def visit_Assignment(self, node):
        node.expression.vars = node.vars
        node.expression.funcs = node.funcs
        type2 = self.visit(node.expression)
        type1 = node.vars.get(node.name)
        # print type1, type2
        if type1 != -1 and type2 != -1:
            if (type1 != 'string' and type2 != 'string') or (type1 == 'string' and type2 == 'string'):
                if type1 == 'int' and type2 == 'float':
                    print 'WARNING: Implicit conversion, line %s' % (node.lineno)
                return False

        if type1 == -1:
            print 'ERROR: Undeclared variable, line %s' % node.lineno
            return True
        if type2 == -1:
            return True
        print 'ERROR: Type mismatch in assignment, line %s' % node.lineno
        return True

    def visit_Init(self, node):
        collision = node.vars.collision(node.name)
        # print str(node)
        if collision:
            print 'ERROR: Variable already declared, line ' + str(node.lineno)
            return -1
        node.expression.vars = node.vars
        node.expression.funcs = node.funcs
        type = self.visit(node.expression)
        if type == -1:
            return -1
        return node, type

    def visit_PrintInstruction(self, node):
        node.expression.vars = node.vars
        node.expression.funcs = node.funcs
        t = self.visit(node.expression)
        return t == -1


    def visit_LabeledInstruction(self, node):
        errors = False
        if node.instruction != None:
            node.instruction.vars = node.vars
            node.instruction.funcs = node.funcs
            if hasattr(node, "retType"):
                node.instruction.retType = node.retType
            if hasattr(node, "inLoop"):
                node.instruction.inLoop = True
            errors = self.visit(node.instruction)
            if errors == -1:
                errors = True
        return errors


    def visit_ChoiceInstruction(self, node):
        node.condition.vars = node.vars
        node.condition.funcs = node.funcs
        ret_c = self.visit(node.condition)
        ret_i = False
        ret_e = False
        if node.instruction != None:
            node.instruction.vars = node.vars
            node.instruction.funcs = node.funcs
            if hasattr(node, "retType"):
                node.instruction.retType = node.retType
            if hasattr(node, "inLoop"):
                node.instruction.inLoop = True
            ret_i = self.visit(node.instruction)
        if node.elseinstruction != None:
            node.elseinstruction.vars = node.vars
            node.elseinstruction.funcs = node.funcs
            if hasattr(node, "retType"):
                node.elseinstruction.retType = node.retType
            if hasattr(node, "inLoop"):
                node.elseinstruction.inLoop = True
            ret_e = self.visit(node.elseinstruction)
        if ret_c == 'string':
            print 'ERROR: Condition type must be \'int\', line %s' % node.lineno
            return True
        if ret_c == 'float':
            print 'WARNING: Implicit conversion to \'int\' in condition, line %s' % node.lineno
        if ret_c == -1 or ret_i or ret_e:
            return True
        return False

    def visit_WhileInstruction(self, node):
        node.condition.vars = node.vars
        node.condition.funcs = node.funcs
        ret_c = self.visit(node.condition)
        ret_i = False
        if node.instruction != None:
            node.instruction.vars = node.vars
            node.instruction.funcs = node.funcs
            if hasattr(node, "retType"):
                node.instruction.retType = node.retType
            node.instruction.inLoop = True
            ret_i = self.visit(node.instruction)
        if ret_c == 'string':
            print 'ERROR: Condition type must be \'int\', line %s' % node.lineno
            return True
        if ret_c == 'float':
            print 'WARNING: Implicit conversion to \'int\' in condition, line %s' % node.lineno
        if ret_c == -1 or ret_i:
            return True
        return False


    def visit_RepeatInstruction(self, node):
        node.condition.vars = node.vars
        node.condition.funcs = node.funcs
        ret_c = self.visit(node.condition)
        ret_i = False
        errors = False
        if node.instructions != None:
            for instr in node.instructions:
                instr.vars = node.vars
                instr.funcs = node.funcs
                if hasattr(node, "retType"):
                    instr.retType = node.retType
                instr.inLoop = True
                ret_i = self.visit(instr)
                errors = ret_i or errors
        if ret_c == 'string':
            print 'ERROR: Condition type must be \'int\', line %s' % node.lineno
            return True
        if ret_c == 'float':
            print 'WARNING: Implicit conversion to \'int\' in condition, line %s' % node.lineno
        if ret_c == -1 or ret_i:
            return True
        return False


    def visit_ReturnInstruction(self, node):
        node.expression.vars = node.vars
        node.expression.funcs = node.funcs
        if hasattr(node, "retType"):
            t = self.visit(node.expression)
            if t == node.retType:
                return False
            if node.retType == 'float' and t == 'int':
                return False
            if node.retType == 'int' and t == 'float':
                print 'WARNING: Implicit conversion in return statement, line %s' % node.lineno
                return False
            if t != -1:
                print 'ERROR: Type mismatch in return statement, line %s' % node.lineno
            return True
        else:
            print 'ERROR: Return statement outside of a function, line %s' % node.lineno
            return True



    def visit_ContinueInstruction(self, node):
        if hasattr(node, "inLoop"):
            return False
        print 'ERROR: Continue statement outside of a loop, line %s' % node.lineno
        return True


    def visit_BreakInstruction(self, node):
        if hasattr(node, "inLoop"):
            return False
        print 'ERROR: Break statement outside of a loop, line %s' % node.lineno
        return True


    def visit_Function_call(self, node):
        fun = node.funcs.get(node.name)
        if fun == -1:
            print 'ERROR: Undeclared function, line %s' % node.lineno
            return -1
        if len(node.expressions.expressions) != len(fun[1]):
            print 'ERROR: Wrong number of arguments, line %s' % node.lineno
            return -1
        for i in xrange(len(node.expressions.expressions)):
            type = fun[1][i][0]
            node.expressions.expressions[i].vars = node.vars
            node.expressions.expressions[i].funcs = node.funcs
            match = self.visit(node.expressions.expressions[i])
            if (type != 'string' and match != 'string') or (type == 'string' and match == 'string'):
                if type != match and type == 'int':
                    print 'WARNING: Implicit conversion in argument %s, line %s' % (i,node.lineno)
            else:
                print 'ERROR: Type mismatch in argument %s, line %s' % (i, node.lineno)
                return -1
        return fun[0]