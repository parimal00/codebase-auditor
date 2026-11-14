
# src/nodes/router.py
from typing import Literal
from pydantic import BaseModel, Field
from src.schemas.state import AuditState
from src.config.llm import get_llm
from langchain_core.messages import HumanMessage
class RouteDecision(BaseModel):
    intent: Literal["rag_search", "code_audit", "off_topic"] = Field(
        description="Classify intent: 'rag_search' for codebase questions, 'code_audit' for repository reviews, or 'off_topic' for non-code interactions."
    )
    reasoning: str = Field(description="Short rationale for the classification.")
