
import ast
from typing import Any

from src.analysis.code_metrics_analyzer import CodeMetricsAnalyzer


class ImportExtractor(ast.NodeVisitor):
    """Extract all imports from a Python file."""

    def __init__(self):
        self.imports = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""

        for alias in node.names:
            name = f"{module}.{alias.name}" if module else alias.name
            self.imports.append(name)

        self.generic_visit(node)

    def extract(self, tree: ast.Module) -> list[str]:
        self.visit(tree)
        return self.imports


class ClassExtractor(ast.NodeVisitor):
    """Extract classes and their nested class hierarchy."""

    def __init__(self):
        self.classes = []
        self.class_stack = []

    def visit_ClassDef(self, node: ast.ClassDef):
        class_info = {
            "name": node.name,
            "lineno": node.lineno,
            "bases": [
                base.id for base in node.bases
                if isinstance(base, ast.Name)
            ],
            "nested_classes": [],
        }

        if self.class_stack:
            self.class_stack[-1]["nested_classes"].append(class_info)
        else:
            self.classes.append(class_info)

        self.class_stack.append(class_info)

        self.generic_visit(node)

        self.class_stack.pop()

    def extract(self, tree: ast.Module) -> list[dict[str, Any]]:
        self.visit(tree)
        return self.classes


class FunctionExtractor(ast.NodeVisitor):
    """Extract functions and methods with their complexity metrics."""

    def __init__(self, metrics_analyzer: CodeMetricsAnalyzer):
        self.metrics_analyzer = metrics_analyzer
        self.functions = []
        self.scope_stack = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope_stack.append(("class", node.name))

        self.generic_visit(node)

        self.scope_stack.pop()

    def _extract_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef
    ):
        parent_scope = self.scope_stack[-1] if self.scope_stack else None

        if parent_scope and parent_scope[0] == "class":
            kind = "method"
        elif parent_scope and parent_scope[0] == "function":
            kind = "nested_function"
        else:
            kind = "function"

        qualified_name = ".".join(
            [name for _, name in self.scope_stack] + [node.name]
        )

        self.functions.append({
            "name": node.name,
            "qualified_name": qualified_name,
            "kind": kind,
            "lineno": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "cyclomatic_complexity": (
                self.metrics_analyzer.calculate_cyclomatic_complexity(node)
            ),
        })

        self.scope_stack.append(("function", node.name))

        self.generic_visit(node)

        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._extract_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._extract_function(node)

    def extract(self, tree: ast.Module) -> list[dict[str, Any]]:
        self.visit(tree)
        return self.functions


class PythonASTParser:
    """Coordinate extraction of information from a Python file."""

    def __init__(self):
        self.metrics_analyzer = CodeMetricsAnalyzer()

    def parse_code(self, code_str: str, file_path: str) -> dict[str, Any]:
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return {"error": f"Syntax error in {file_path}: {e}"}

        import_extractor = ImportExtractor()
        class_extractor = ClassExtractor()
        function_extractor = FunctionExtractor(self.metrics_analyzer)

        return {
            "file_path": file_path,
            "imports": import_extractor.extract(tree),
            "classes": class_extractor.extract(tree),
            "functions": function_extractor.extract(tree),
        }
