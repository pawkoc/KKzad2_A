#!/usr/bin/python

class FunctionTable(object):

    def __init__(self):
        self.dictionary = {}

    def put(self, name, retval, args):
        self.dictionary[name] = [retval, args]

    def get(self, name):
        if name in self.dictionary.keys():
            return self.dictionary[name]
        else:
            return -1

class VariableTable(object):

    def __init__(self, parent):
        self.parentScope = parent
        self.dictionary = {}

    def put(self, name, symbol):
        self.dictionary[name] = symbol

    def collision(self, name):
        return name in self.dictionary.keys()

    def get(self, name):
        if name in self.dictionary.keys():
            return self.dictionary[name]
        elif self.parentScope != None:
            return self.getParentScope().get(name)
        else:
            return -1

    def getParentScope(self):
        return self.parentScope
