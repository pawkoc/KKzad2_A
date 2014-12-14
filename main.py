import sys
import ply.yacc as yacc
import AST
from Cparser import Cparser
import TreePrinter


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

    # print p
    print p
        # t = TreePrinter.TreePrinter()
        # t.printTree()