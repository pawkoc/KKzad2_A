#!/usr/bin/python
from AST import *

from scanner import Scanner
import AST

declarations = Declaration_list()
instructions = Instruction_list()
fundefs = Function_list()
fundefs = []

# scopes = []
#
# def push_scope(scope):
#     global scopes
#     scopes.append(scope)
#
# def pop_scope():
#     global scopes
#     last = scopes.pop()
#     return last
#
#
# global_scope = Scope()
# push_scope(global_scope)

class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    symbol_table = {}

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')

    def p_program(self, p):
        """program : declarations fundefs instructions"""
        dec = Declaration_list()

        for dec1 in p[1]:
            dec.addDeclaration(dec1)

        funs = Function_list()

        for fun1 in p[2]:
            funs.addFunction(fun1)

        instr = Instruction_list()

        for instr1 in p[3]:
            instr.addInstruction(instr1)


        p[0] = Program(dec, funs, instr)


    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """

        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        dec = Declaration(p[1])
        for decl in p[2]:
            dec.addInit(decl[0], decl[1], p.lineno(1))

        p[0] = dec

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """

        if len(p) == 4:
            p[0] = p[1] + [p[3]]

        else:
            p[0] = [p[1]]

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = (p[1], p[3])

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            # instructions.addInstruction(p[2])
            p[0] = p[1] + [p[2]]

        else:
            # instructions.addInstruction(p[1])
            p[0] = [p[1]]

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""

        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """

        p[0] = PrintInstruction(p.lineno(1), p[2])


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """

        p[0] = LabeledInstruction(p.lineno(1), p[1], p[3])


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """

        p[0] = Assignment(p[1], p[3], p.lineno(1))


    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

        if len(p) == 6:
            p[0] = ChoiceInstruction(p.lineno(1), p[3], p[5])
        else:
            p[0] = ChoiceInstruction(p.lineno(1), p[3], p[5], p[7])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """

        p[0] = WhileInstruction(p.lineno(1), p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """

        p[0] = RepeatInstruction(p.lineno(1), p[2], p[4])


    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """

        p[0] = ReturnInstruction(p.lineno(1), p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """

        p[0] = ContinueInstructoion()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """

        p[0] = BreakInstruction()

    def p_compound_instr(self, p):
        """compound_instr : '{' new_scope declarations instructions '}' """

        comp = Compound_instr()
        for dec in p[3]:
            comp.addDeclaration(dec)

        for instr in p[4]:
            comp.addInstruction(instr)

        c = Instruction('comp', comp)

        p[0] = c

        # pop_scope()

    def p_new_scope(self, p):
        """new_scope :"""
        # s = Scope()
        # push_scope(s)
        pass


    def p_condition(self, p):
        """condition : expression"""

        p[0] = p[1]

    def p_integer(self, p):
        """integer : INTEGER"""
        p[0] = Integer(p[1])

    def p_float(self, p):
        """float : FLOAT"""
        p[0] = Float(p[1])

    def p_string(self, p):
        """string : STRING"""
        p[0] = String(p[1])

    def p_const(self, p):
        """const : integer
                 | float
                 | string """
        p[0] = p[1]

    def p_expression_const(self, p):
        """expression : const """
        p[0] = p[1]

    def p_expression_ID(self, p):
        """expression : ID """
        p[0] = Variable(p[1], p.lineno(1))

    def p_expression_bin(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression """

        p[0] = BinExpr(op=p[2], left=p[1], right=p[3], lineno=p.lineno(1))

    def p_expression(self, p):
        """expression : '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """

        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = (p[1], p[2])

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        p[0] = p[1]


    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """

        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """

        if len(p) == 3:
            p[0] = [p[1]] + p[2]

        else:
            p[0] = []

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """

        fun = Function(p[1], p[2], p[4], p[6], p.lineno(0))
        p[0] = fun

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
            # print '[%s]' % ', '.join(map(str, p[0]))
        else:
            p[0] = [p[1]]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = (p[1], p[2])


    
