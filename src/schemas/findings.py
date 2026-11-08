from pydantic import BaseModel, Field
from typing import List, Literal

class Finding(BaseModel):
    category: Literal["architecture", "quality", "security"] = Field(description="The category of the finding")
    severity: Literal["low", "medium", "high", "critical"] = Field(description="Severity level of the issue.")
    file_path: str = Field(description="Relative path of the file where the issue was found.")
    title: str = Field(description="Short, descriptive title of the issue.")
    description: str = Field(description="Detailed explanation of why this is an issue and how to fix it.")
    
class AgentFindingReport(BaseModel):
    findings: List[Finding] = Field(description="List of detected codebase findings.")