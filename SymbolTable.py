#!/usr/bin/python


# class VariableSymbol(Symbol):

    # def __init__(self, name, type):
    #
    #


class SymbolTable(object):

    def __init__(self, parent, name=None):
        self.parentScope = parent
        self.dictionary = {}

    def put(self, name, symbol):
    # sprawdzam czy inny nie posiada takiej nazwy
        if name in self.dictionary.keys():
            self.dictionary[name] = symbol
            return -1
        else:
            self.dictionary[name] = symbol
            return 0

    def collision(self, name):
        return name in self.dictionary.keys()

    def get(self, name):
    # sprawdzam czy istnieje juz o takiej nazwie
        if name in self.dictionary.keys():
            return self.dictionary[name]
        elif self.parentScope != None:
            return self.getParentScope().get(name)
        else:
            return -1

    def getParentScope(self):
        return self.parentScope
