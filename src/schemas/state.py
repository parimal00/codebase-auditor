from typing import TypedDict, List, Dict, Any
from src.schemas.ast_dto import ParsedFileDTO


class AuditState(TypedDict):
    target_dir: str
    file_tree: List[Dict[str, str]]
    parsed_ast: List[ParsedFileDTO]
    architecture_findings: List[Dict[str, Any]]
    quality_findings: List[Dict[str, Any]]
    security_findings: List[Dict[str, Any]]
    current_node: str
    # fields for Router
    route: str
    router_reasoning: str
    # fields for rag search
    user_query: str
    rag_response: str
    retrieved_matches: List[Dict[str, Any]]
    #fields for aggregated findings
    findings: List[Dict[str, Any]]
