import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node: ast.If):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return

    def visit_ClassDef(self, node: ast.ClassDef):
        return

    def visit_Lambda(self, node: ast.Lambda):
        return


class CodeMetricsAnalyzer:
    def calculate_cyclomatic_complexity(
        self,
        function_node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> int:

        visitor = ComplexityVisitor()

        for statement in function_node.body:
            visitor.visit(statement)

        return visitor.complexity