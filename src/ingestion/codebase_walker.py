import os
from pathlib import Path
from typing import Dict, List, Set

DEFAULT_IGNORE_DIRS = {
    ".git", "venv", ".venv", "__pycache__", "node_modules",
    "vendor", ".idea", ".vscode", "dist", "build"
}

class CodebaseWalker:
    def __init__(self, root_dir: str, ignore_dirs: Set[str] = None):
        self.root_dir = Path(root_dir).resolve()
        self.ignore_dirs = ignore_dirs if ignore_dirs is not None else DEFAULT_IGNORE_DIRS  
        
    def build_file_tree(self) -> List[Dict[str, str]]:
        file_list = []
        
        for root, dirs, files in os.walk(self.root_dir):
            filtered_dirs = []
            for d in dirs:
                if d not in self.ignore_dirs:
                    filtered_dirs.append(d)
            
            dirs[:] = filtered_dirs
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.root_dir)
                
                file_list.append({
                    "relative_path": str(relative_path),
                    "absolute_path": str(file_path),
                    "extension": file_path.suffix.lstrip(".")
                })
            
        return file_list
        
    def read_file(self, relative_path: str) -> str:
        full_path = self.root_dir / relative_path
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()