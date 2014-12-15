import sys
import ply.yacc as yacc
import AST
from Cparser import Cparser
import TreePrinter
from TypeChecker import TypeChecker
import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    p = parser.parse(text, lexer=Cparser.scanner)

    TC = TypeChecker()
    TC.visit(p)
    # if not TC.visit(p):
    print p
    intrepreter = Interpreter.Interpreter()
    p.accept(intrepreter)
