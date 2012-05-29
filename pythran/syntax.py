'''This module performs a few early syntax check on the input AST.'''
import ast
import tables

class PythranSyntaxError(SyntaxError):
    def __init__(self, msg, node):
        SyntaxError.__init__(self,msg)
        self.lineno=node.lineno
        self.offset=node.col_offset

class SyntaxChecker(ast.NodeVisitor):
    def visit_Module(self, node):
        for n in node.body:
            if not any(map(lambda t:isinstance(n,t),(ast.FunctionDef, ast.Import, ast.ImportFrom))):
                raise PythranSyntaxError("Top level statements can only be functions or imports", n)

    def visit_Interactive(self, node):
        raise PythranSyntaxError("Interactive session are not supported", node)

    def visit_Expression(self, node):
        raise PythranSyntaxError("Top-Level expressions are not supported", node)

    def visit_Suite(self, node):
        raise PythranSyntaxError("Suite are specific to Jython and not supported", node)

    def visit_ClassDef(self, node):
        raise PythranSyntaxError("Classes not supported")

    def visit_Print(self, node):
        if node.dest: raise PythranSyntaxError("Printing to a specific stream", node.dest)

    def visit_Import(self, node):
        for alias in node.names:
            name, asname=(alias.name, alias.asname)
            if asname:
                PythranSyntaxError("Renaming using the 'as' keyword in an import", node)
            elif name not in modules:
                PythranSyntaxError("Module '{0}'".format(name), node)

    def visit_ImportFrom(self, node):
        if node.level != 0: raise PythranSyntaxError("Specifying a level in an import", node)
        if not node.module: raise PythranSyntaxError("The import from syntax without module", node)
        module = node.module
        if module not in tables.modules: raise PythranSyntaxError("Module '{0}'".format(module), node)

        names = node.names
        if [ alias for alias in names if alias.asname ]: raise PythranSyntaxError("Renaming using the 'as' keyword in an import", node)

    def visit_Dict(self, node):
        raise PythranSyntaxError("Dictionaries are not supported", node)

    def visit_Set(self, node):
        raise PythranSyntaxError("Sets are not supported", node)

    def visit_SetComp(self, node):
        raise PythranSyntaxError("Set comprehension are not supported", node)

    def visit_DictComp(self, node):
        raise PythranSyntaxError("Dictionary comprehension are not supported", node)

    def visit_GeneratorExp(self, node):
        raise PythranSyntaxError("Generator expression are not supported", node)

    def visit_Yield(self, node):
        raise PythranSyntaxError("yield keyword is not supported", node)


def check_syntax(node):
    '''Does nothing but raising exception when pythran syntax is not respected'''
    SyntaxChecker().visit(node)