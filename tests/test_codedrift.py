"""Tests for CodeDrift"""

import pytest
from pathlib import Path
from codedrift.detector import DriftDetector
from codedrift.config import CodeDriftConfig
from codedrift.analyzer import CodeAnalyzer
from codedrift.models import DriftType, DriftSeverity


def test_analyzer_extract_functions():
    """Test function extraction from Python files"""
    analyzer = CodeAnalyzer(language="python")
    
    # Create a test file
    test_file = Path("test_sample.py")
    test_code = '''
def greet(name: str) -> str:
    """
    Greet someone.
    
    Args:
        name (str): Person's name
        
    Returns:
        str: Greeting message
    """
    return f"Hello, {name}!"
'''
    
    test_file.write_text(test_code)
    
    try:
        functions = analyzer.extract_function_signatures(test_file)
        assert len(functions) > 0
        assert functions[0]["name"] == "greet"
        assert "name" in functions[0]["parameters"]
    finally:
        test_file.unlink()


def test_analyzer_check_docstring():
    """Test docstring completeness checking"""
    analyzer = CodeAnalyzer(language="python")
    
    func_info = {
        "name": "test_func",
        "parameters": {"param1": "str", "param2": "int"},
        "docstring": """
        Test function.
        
        Args:
            param1 (str): First parameter
        """,
    }
    
    issues = analyzer.check_docstring_completeness(func_info)
    assert len(issues) > 0
    assert "param2" in str(issues)


def test_detector_scan():
    """Test project scanning"""
    config = CodeDriftConfig(project_root=Path("."))
    detector = DriftDetector(config)
    
    results = detector.scan_project(Path("."))
    
    assert results.files_analyzed >= 0
    assert hasattr(results, "health_score")
    assert 0 <= results.health_score <= 100


def test_health_score_calculation():
    """Test health score calculation"""
    config = CodeDriftConfig(project_root=Path("."))
    detector = DriftDetector(config)
    
    # Test with no files
    results = detector.results
    results.files_analyzed = 0
    
    health = detector._calculate_health_score()
    assert health == 100.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
