import json
import sys
from src.ingestion.codebase_walker import CodebaseWalker
from src.ingestion.ast_parser import PythonASTParser

def run_ingestion(target_dir: str):
    
    print(f" Scanning directory: {target_dir}")
    walker = CodebaseWalker(target_dir)
    parser = PythonASTParser()

    files = walker.build_file_tree()
    print(f"Found {len(files)} files.")

    parsed_data = []
    for f in files:
        if f["extension"] == "py":
            code = walker.read_file(f["relative_path"])
            ast_meta = parser.parse_code(code, f["relative_path"])
            parsed_data.append(ast_meta)

    print("\n--- Ingestion Output Sample ---")
    print(json.dumps(parsed_data, indent=2))
    
if __name__ == "__main__":
    path = "."
    run_ingestion(path)
    
