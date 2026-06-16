"""Drift detection module"""

import uuid
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from codedrift.analyzer import CodeAnalyzer
from codedrift.models import (
    Drift,
    DriftType,
    DriftSeverity,
    DriftLocation,
    AnalysisResult,
)
from codedrift.config import CodeDriftConfig


class DriftDetector:
    """Main class for detecting code/documentation drifts"""
    
    def __init__(self, config: Optional[CodeDriftConfig] = None):
        self.config = config or CodeDriftConfig()
        self.analyzer = CodeAnalyzer(language="python")
        self.results = AnalysisResult()
    
    def scan_project(self, project_path: Optional[Path] = None) -> AnalysisResult:
        """Scan entire project for drifts"""
        if project_path is None:
            project_path = self.config.project_root
        
        self.results = AnalysisResult()
        
        # Find all Python files
        python_files = list(project_path.glob("**/*.py"))
        
        # Filter by include/exclude patterns
        python_files = self._filter_files(python_files)
        
        self.results.files_analyzed = len(python_files)
        
        # Analyze each file
        for py_file in python_files:
            self._analyze_file(py_file)
        
        # Calculate health score
        self.results.health_score = self._calculate_health_score()
        
        return self.results
    
    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single file for drifts"""
        # Extract function signatures
        functions = self.analyzer.extract_function_signatures(file_path)
        
        for func in functions:
            # Check docstring completeness
            docstring_issues = self.analyzer.check_docstring_completeness(func)
            
            for issue in docstring_issues:
                drift = self._create_drift(
                    drift_type=DriftType.MISSING_DOCSTRING,
                    severity=DriftSeverity.WARNING,
                    title=issue,
                    description=f"Function '{func['name']}' has documentation issues",
                    location=DriftLocation(
                        file_path=str(file_path),
                        line_start=func["line"],
                        line_end=func["line"],
                    ),
                    current_value=func.get("docstring", ""),
                    expected_value=f"Docstring covering all parameters: {list(func.get('parameters', {}).keys())}"
                )
                self.results.add_drift(drift)
            
            # Check parameter consistency
            if func.get("docstring"):
                param_drift = self._check_parameter_consistency(func, file_path)
                if param_drift:
                    self.results.add_drift(param_drift)
    
    def _check_parameter_consistency(self, func: Dict, file_path: Path) -> Optional[Drift]:
        """Check if documented parameters match function signature"""
        docstring_info = self.analyzer.extract_docstring_info(func.get("docstring", ""))
        documented_params = docstring_info["parameters"]
        actual_params = func.get("parameters", {})
        
        if set(documented_params.keys()) != set(actual_params.keys()):
            missing = set(actual_params.keys()) - set(documented_params.keys())
            extra = set(documented_params.keys()) - set(actual_params.keys())
            
            description = f"Parameter mismatch in '{func['name']}':\n"
            if missing:
                description += f"Missing docs: {missing}\n"
            if extra:
                description += f"Extra docs: {extra}"
            
            return self._create_drift(
                drift_type=DriftType.PARAMETER_MISMATCH,
                severity=DriftSeverity.ERROR,
                title=f"Parameter documentation mismatch in '{func['name']}'",
                description=description,
                location=DriftLocation(
                    file_path=str(file_path),
                    line_start=func["line"],
                    line_end=func["line"],
                ),
                current_value=str(documented_params),
                expected_value=str(actual_params),
                suggested_fix=self._generate_param_fix(func),
            )
        
        return None
    
    def _generate_param_fix(self, func: Dict) -> str:
        """Generate a suggested docstring fix for parameters"""
        params = func.get("parameters", {})
        
        docstring = f'    """\n    {func["name"]} function.\n    \n    Args:\n'
        for param_name, param_type in params.items():
            docstring += f"        {param_name} ({param_type}): Description of {param_name}\n"
        
        docstring += f'\n    Returns:\n        {func.get("return_type", "Any")}: Description of return value\n    """'
        
        return docstring
    
    def check_readme_drifts(self, project_path: Optional[Path] = None) -> AnalysisResult:
        """Check for README documentation drifts"""
        if project_path is None:
            project_path = self.config.project_root
        
        readme_path = project_path / "README.md"
        
        if not readme_path.exists():
            return self.results
        
        # Get all Python files
        python_files = list(project_path.glob("**/*.py"))
        python_files = self._filter_files(python_files)
        
        # Extract all functions from Python files
        all_functions = []
        for py_file in python_files:
            functions = self.analyzer.extract_function_signatures(py_file)
            all_functions.extend(functions)
        
        # Check README examples
        issues = self.analyzer.check_readme_examples(readme_path, all_functions)
        
        for issue in issues:
            drift = self._create_drift(
                drift_type=DriftType.README_OUTDATED,
                severity=DriftSeverity.WARNING,
                title="README example may be outdated",
                description=issue,
                location=DriftLocation(
                    file_path=str(readme_path),
                    line_start=1,
                    line_end=1,
                ),
                current_value="Unknown",
                expected_value="Updated examples",
            )
            self.results.add_drift(drift)
        
        return self.results
    
    def _filter_files(self, files: List[Path]) -> List[Path]:
        """Filter files based on include/exclude patterns"""
        filtered = []
        
        for file_path in files:
            # Check exclude patterns
            should_exclude = False
            for pattern in self.config.exclude_patterns:
                if file_path.match(pattern):
                    should_exclude = True
                    break
            
            if should_exclude:
                continue
            
            # Check include patterns
            should_include = False
            for pattern in self.config.include_patterns:
                if file_path.match(pattern):
                    should_include = True
                    break
            
            if should_include:
                filtered.append(file_path)
        
        return filtered
    
    def _create_drift(
        self,
        drift_type: DriftType,
        severity: DriftSeverity,
        title: str,
        description: str,
        location: DriftLocation,
        current_value: str,
        expected_value: str,
        suggested_fix: Optional[str] = None,
    ) -> Drift:
        """Create a Drift object"""
        return Drift(
            drift_id=str(uuid.uuid4())[:8],
            drift_type=drift_type,
            severity=severity,
            title=title,
            description=description,
            location=location,
            current_value=current_value,
            expected_value=expected_value,
            suggested_fix=suggested_fix,
        )
    
    def _calculate_health_score(self) -> float:
        """Calculate documentation health score (0-100)"""
        if self.results.files_analyzed == 0:
            return 100.0
        
        # Weight different severity levels
        critical_weight = 10
        error_weight = 5
        warning_weight = 2
        info_weight = 1
        
        total_weight = 0
        for drift in self.results.drifts:
            if drift.severity == DriftSeverity.CRITICAL:
                total_weight += critical_weight
            elif drift.severity == DriftSeverity.ERROR:
                total_weight += error_weight
            elif drift.severity == DriftSeverity.WARNING:
                total_weight += warning_weight
            else:
                total_weight += info_weight
        
        # Max impact is 100 points
        max_impact = min(100, total_weight)
        score = max(0, 100 - max_impact)
        
        return round(score, 2)
