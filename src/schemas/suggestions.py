from pydantic import BaseModel
from typing import List, Literal

class FindingSuggestion(BaseModel):
    category: Literal["architecture", "quality", "security"]
    file_path: str
    title: str
    suggestion: str


class ImprovementSuggestionReport(BaseModel):
    suggestions: List[FindingSuggestion]