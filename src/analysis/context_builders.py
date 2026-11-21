from typing import List, Union
from src.schemas.ast_dto import ParsedFileDTO, ClassDTO, FunctionDTO
from src.schemas.context_dto import (
    QualityContextDTO,
    FileQualityContextDTO,
    FunctionQualityDTO,
    ArchitectureContextDTO,
    FileArchitectureContextDTO,
    ClassArchitectureDTO,
    SecurityContextDTO,
    FileSecurityContextDTO,
)


class QualityContextBuilder:
    """Adapts canonical parsed AST DTOs into the specific context required by Quality Auditor."""

    def build(self, parsed_files: List[Union[ParsedFileDTO, dict]]) -> QualityContextDTO:
        file_contexts: List[FileQualityContextDTO] = []

        for pf in parsed_files:
            if isinstance(pf, dict):
                pf = ParsedFileDTO.model_validate(pf)

            if pf.error:
                continue

            quality_funcs = [
                FunctionQualityDTO(
                    name=func.name,
                    qualified_name=func.qualified_name,
                    kind=func.kind,
                    lineno=func.lineno,
                    args=func.args,
                    docstring=func.docstring,
                    cyclomatic_complexity=func.cyclomatic_complexity,
                )
                for func in pf.functions
            ]

            file_contexts.append(
                FileQualityContextDTO(
                    file_path=pf.file_path,
                    functions=quality_funcs,
                )
            )

        return QualityContextDTO(files=file_contexts)


class ArchitectureContextBuilder:
    """Adapts canonical parsed AST DTOs into the specific context required by Architecture Auditor."""

    def _map_class(self, cls: ClassDTO) -> ClassArchitectureDTO:
        return ClassArchitectureDTO(
            name=cls.name,
            lineno=cls.lineno,
            bases=cls.bases,
            nested_classes=[self._map_class(c) for c in cls.nested_classes],
        )

    def build(self, parsed_files: List[Union[ParsedFileDTO, dict]]) -> ArchitectureContextDTO:
        file_contexts: List[FileArchitectureContextDTO] = []

        for pf in parsed_files:
            if isinstance(pf, dict):
                pf = ParsedFileDTO.model_validate(pf)

            if pf.error:
                continue

            classes = [self._map_class(c) for c in pf.classes]
            function_names = [f.qualified_name for f in pf.functions]

            file_contexts.append(
                FileArchitectureContextDTO(
                    file_path=pf.file_path,
                    imports=pf.imports,
                    classes=classes,
                    function_names=function_names,
                )
            )

        return ArchitectureContextDTO(files=file_contexts)


class SecurityContextBuilder:
    """Adapts canonical parsed AST DTOs into the specific context required by Security Auditor."""

    def build(self, parsed_files: List[Union[ParsedFileDTO, dict]]) -> SecurityContextDTO:
        file_contexts: List[FileSecurityContextDTO] = []

        for pf in parsed_files:
            if isinstance(pf, dict):
                pf = ParsedFileDTO.model_validate(pf)

            if pf.error:
                continue

            function_names = [f.qualified_name for f in pf.functions]

            file_contexts.append(
                FileSecurityContextDTO(
                    file_path=pf.file_path,
                    imports=pf.imports,
                    function_names=function_names,
                )
            )

        return SecurityContextDTO(files=file_contexts)
