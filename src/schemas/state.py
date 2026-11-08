from typing import TypedDict, List, Dict, Any, Annotated
import operator
class AuditState(TypedDict):
    target_dir: str
    file_tree: List[Dict[str, str]]
    parsed_ast: List[Dict[str, Any]]
    findings: Annotated[List[Dict[str, Any]], operator.add]
    current_node: str
    
    