from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class FunctionDTO(BaseModel):
    """Canonical DTO representing a function or method extracted from AST."""

    name: str
    qualified_name: str
    kind: str = "function"  # "function", "method", "nested_function"
    lineno: int = 1
    args: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    cyclomatic_complexity: int = 1


class ClassDTO(BaseModel):
    """Canonical DTO representing a class and its nested hierarchy extracted from AST."""

    name: str
    lineno: int = 1
    bases: List[str] = Field(default_factory=list)
    nested_classes: List[ClassDTO] = Field(default_factory=list)
    docstring: Optional[str] = None


class ParsedFileDTO(BaseModel):
    """Canonical DTO representing a parsed Python source file."""

    file_path: str
    imports: List[str] = Field(default_factory=list)
    classes: List[ClassDTO] = Field(default_factory=list)
    functions: List[FunctionDTO] = Field(default_factory=list)
    error: Optional[str] = None
