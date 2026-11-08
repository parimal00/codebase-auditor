import ast
from typing import Dict, List, Any

class PythonASTParser:
    def parse_code(self, code_str: str, file_path: str)->Dict[str, Any]:
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return {"error": f"Syntax error in {file_path}: {e}"}
        imports=[]
        classes=[]
        functions=[]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                    "methods": [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                })
            elif isinstance(node, ast.FunctionDef) and not getattr(node, "_in_class", False):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args]
                })
                
        return {
            "file_path": file_path,
            "imports": imports,
            "classes": classes,
            "functions": functions
        }