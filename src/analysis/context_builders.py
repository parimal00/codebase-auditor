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

from src.analysis.complexity_severity import ComplexitySeverityEvaluator


class QualityContextBuilder:
    """Adapts parsed AST DTOs into the context required by Quality Auditor."""

    def __init__(self):
        self.severity_evaluator = ComplexitySeverityEvaluator()

    def build(
        self,
        parsed_files: list[ParsedFileDTO],
    ) -> QualityContextDTO:
        file_contexts = []
        
        for parsed_file in parsed_files:
            if parsed_file.error:
                continue

            quality_functions = [
                FunctionQualityDTO(
                    name=function.name,
                    qualified_name=function.qualified_name,
                    kind=function.kind,
                    lineno=function.lineno,
                    args=function.args,
                    docstring=function.docstring,
                    cyclomatic_complexity=function.cyclomatic_complexity,
                    complexity_severity=self.severity_evaluator.evaluate(function.cyclomatic_complexity),
                )
                for function in parsed_file.functions
            ]

            file_contexts.append(
                FileQualityContextDTO(
                    file_path=parsed_file.file_path,
                    functions=quality_functions,
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
