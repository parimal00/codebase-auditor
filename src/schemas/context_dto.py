from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


# --- Quality Auditor Context DTOs ---

class FunctionQualityDTO(BaseModel):
    """Function metadata specifically needed for code quality analysis."""

    name: str
    qualified_name: str
    kind: str = "function"
    lineno: int = 1
    args: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    cyclomatic_complexity: int = 1


class FileQualityContextDTO(BaseModel):
    """File-level code quality context."""

    file_path: str
    functions: List[FunctionQualityDTO] = Field(default_factory=list)


class QualityContextDTO(BaseModel):
    """Aggregated context consumed by the Quality Auditor."""

    files: List[FileQualityContextDTO] = Field(default_factory=list)


# --- Architecture Auditor Context DTOs ---

class ClassArchitectureDTO(BaseModel):
    """Class metadata specifically needed for architecture analysis."""

    name: str
    lineno: int = 1
    bases: List[str] = Field(default_factory=list)
    nested_classes: List[ClassArchitectureDTO] = Field(default_factory=list)


class FileArchitectureContextDTO(BaseModel):
    """File-level architecture context containing imports, classes, and function names."""

    file_path: str
    imports: List[str] = Field(default_factory=list)
    classes: List[ClassArchitectureDTO] = Field(default_factory=list)
    function_names: List[str] = Field(default_factory=list)


class ArchitectureContextDTO(BaseModel):
    """Aggregated context consumed by the Architecture Auditor."""

    files: List[FileArchitectureContextDTO] = Field(default_factory=list)


# --- Security Auditor Context DTOs ---

class FileSecurityContextDTO(BaseModel):
    """File-level security context containing imports and function names."""

    file_path: str
    imports: List[str] = Field(default_factory=list)
    function_names: List[str] = Field(default_factory=list)


class SecurityContextDTO(BaseModel):
    """Aggregated context consumed by the Security Auditor."""

    files: List[FileSecurityContextDTO] = Field(default_factory=list)
