from pydantic import BaseModel, Field
from typing import List

class RAGResponseSchema(BaseModel):
    answer: str = Field(description="Clear technical explanation answering the user query based on the code context.")
    referenced_files: List[str] = Field(description="List of file paths cited or referenced in the answer.")