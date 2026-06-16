"""CodeDrift - Automatic Code and Documentation Synchronization"""

__version__ = "0.1.0"
__author__ = "CodeDrift Team"

from codedrift.detector import DriftDetector
from codedrift.analyzer import CodeAnalyzer
from codedrift.config import CodeDriftConfig

__all__ = ["DriftDetector", "CodeAnalyzer", "CodeDriftConfig"]
