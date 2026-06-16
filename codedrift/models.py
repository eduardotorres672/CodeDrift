"""Data models for CodeDrift"""

from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class DriftSeverity(str, Enum):
    """Severity levels for detected drifts"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DriftType(str, Enum):
    """Types of drifts that can be detected"""
    FUNCTION_SIGNATURE_MISMATCH = "function_signature_mismatch"
    TYPE_MISMATCH = "type_mismatch"
    PARAMETER_MISMATCH = "parameter_mismatch"
    RETURN_TYPE_MISMATCH = "return_type_mismatch"
    MISSING_DOCSTRING = "missing_docstring"
    OUTDATED_EXAMPLE = "outdated_example"
    OPENAPI_MISMATCH = "openapi_mismatch"
    README_OUTDATED = "readme_outdated"
    ENDPOINT_MISSING = "endpoint_missing"
    DEPRECATED_MARKER_MISSING = "deprecated_marker_missing"


@dataclass
class DriftLocation:
    """Location of a drift in the codebase"""
    file_path: str
    line_start: int
    line_end: int
    column_start: int = 0
    column_end: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "column_start": self.column_start,
            "column_end": self.column_end,
        }


@dataclass
class Drift:
    """Represents a single code/documentation drift"""
    drift_id: str
    drift_type: DriftType
    severity: DriftSeverity
    title: str
    description: str
    location: DriftLocation
    current_value: str
    expected_value: str
    suggested_fix: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.drift_id,
            "type": self.drift_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "location": self.location.to_dict(),
            "current": self.current_value,
            "expected": self.expected_value,
            "suggested_fix": self.suggested_fix,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class AnalysisResult:
    """Result of code analysis"""
    drifts: List[Drift] = field(default_factory=list)
    files_analyzed: int = 0
    total_issues: int = 0
    health_score: float = 100.0
    
    def add_drift(self, drift: Drift) -> None:
        """Add a drift to the results"""
        self.drifts.append(drift)
        self.total_issues += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the analysis"""
        severity_counts = {
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }
        
        for drift in self.drifts:
            severity_counts[drift.severity.value] += 1
        
        return {
            "files_analyzed": self.files_analyzed,
            "total_drifts": len(self.drifts),
            "health_score": self.health_score,
            "by_severity": severity_counts,
            "by_type": self._count_by_type(),
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count drifts by type"""
        counts: Dict[str, int] = {}
        for drift in self.drifts:
            drift_type = drift.drift_type.value
            counts[drift_type] = counts.get(drift_type, 0) + 1
        return counts


@dataclass
class FunctionSignature:
    """Represents a function signature"""
    name: str
    parameters: Dict[str, str]  # param_name -> type
    return_type: str
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    is_deprecated: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "parameters": self.parameters,
            "return_type": self.return_type,
            "docstring": self.docstring,
            "decorators": self.decorators,
            "is_deprecated": self.is_deprecated,
        }
