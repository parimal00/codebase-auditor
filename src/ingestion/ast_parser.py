import ast
from typing import List

from src.analysis.code_metrics_analyzer import CodeMetricsAnalyzer
from src.schemas.ast_dto import ParsedFileDTO, ClassDTO, FunctionDTO


class ImportExtractor(ast.NodeVisitor):
    """Extract all imports from a Python file."""

    def __init__(self):
        self.imports: List[str] = []

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

    def extract(self, tree: ast.Module) -> List[str]:
        self.visit(tree)
        return self.imports


class ClassExtractor(ast.NodeVisitor):
    """Extract classes and their nested class hierarchy as ClassDTOs."""

    def __init__(self):
        self.classes: List[ClassDTO] = []
        self.class_stack: List[ClassDTO] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [
            base.id for base in node.bases
            if isinstance(base, ast.Name)
        ]
        docstring = ast.get_docstring(node)

        class_dto = ClassDTO(
            name=node.name,
            lineno=node.lineno,
            bases=bases,
            nested_classes=[],
            docstring=docstring,
        )

        if self.class_stack:
            self.class_stack[-1].nested_classes.append(class_dto)
        else:
            self.classes.append(class_dto)

        self.class_stack.append(class_dto)

        self.generic_visit(node)

        self.class_stack.pop()

    def extract(self, tree: ast.Module) -> List[ClassDTO]:
        self.visit(tree)
        return self.classes


class FunctionExtractor(ast.NodeVisitor):
    """Extract functions and methods with their complexity metrics as FunctionDTOs."""

    def __init__(self, metrics_analyzer: CodeMetricsAnalyzer):
        self.metrics_analyzer = metrics_analyzer
        self.functions: List[FunctionDTO] = []
        self.scope_stack: List[tuple[str, str]] = []

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
        docstring = ast.get_docstring(node)
        complexity = self.metrics_analyzer.calculate_cyclomatic_complexity(node)

        self.functions.append(FunctionDTO(
            name=node.name,
            qualified_name=qualified_name,
            kind=kind,
            lineno=node.lineno,
            args=[arg.arg for arg in node.args.args],
            docstring=docstring,
            cyclomatic_complexity=complexity,
        ))

        self.scope_stack.append(("function", node.name))

        self.generic_visit(node)

        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._extract_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._extract_function(node)

    def extract(self, tree: ast.Module) -> List[FunctionDTO]:
        self.visit(tree)
        return self.functions


class PythonASTParser:
    """Coordinate extraction of information from a Python file into a ParsedFileDTO."""

    def __init__(self):
        self.metrics_analyzer = CodeMetricsAnalyzer()

    def parse_code(self, code_str: str, file_path: str) -> ParsedFileDTO:
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return ParsedFileDTO(
                file_path=file_path,
                error=f"Syntax error in {file_path}: {e}",
            )

        import_extractor = ImportExtractor()
        class_extractor = ClassExtractor()
        function_extractor = FunctionExtractor(self.metrics_analyzer)

        return ParsedFileDTO(
            file_path=file_path,
            imports=import_extractor.extract(tree),
            classes=class_extractor.extract(tree),
            functions=function_extractor.extract(tree),
        )
