from typing import TypedDict, List, Dict, Any

class AuditState(TypedDict):
    target_dir: str
    file_tree: List[Dict[str, str]]
    parsed_ast: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    current_node: str
    
    