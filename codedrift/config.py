"""Configuration management for CodeDrift"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from pydantic import BaseModel, Field


class CodeDriftConfig(BaseModel):
    """Configuration model for CodeDrift"""
    
    project_root: Path = Field(default=Path("."), description="Root directory of the project")
    languages: List[str] = Field(
        default=["python", "typescript", "javascript"],
        description="Languages to analyze"
    )
    include_patterns: List[str] = Field(
        default=["**/*.py", "**/*.ts", "**/*.js"],
        description="File patterns to include"
    )
    exclude_patterns: List[str] = Field(
        default=["**/node_modules/**", "**/.venv/**", "**/__pycache__/**", "**/dist/**"],
        description="File patterns to exclude"
    )
    check_jsdoc: bool = Field(default=True, description="Check JSDoc/docstring consistency")
    check_openapi: bool = Field(default=True, description="Check OpenAPI specs")
    check_readme: bool = Field(default=True, description="Check README examples")
    check_types: bool = Field(default=True, description="Check TypeScript types")
    severity_threshold: str = Field(
        default="warning",
        description="Minimum severity to report (info, warning, error)"
    )
    ai_enabled: bool = Field(default=False, description="Enable AI-powered suggestions")
    ai_provider: str = Field(default="openai", description="AI provider (openai, ollama, local)")
    auto_fix: bool = Field(default=False, description="Automatically fix drifts")
    
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_file(cls, config_path: Path = Path(".codedrift.yml")) -> "CodeDriftConfig":
        """Load config from YAML file"""
        if not config_path.exists():
            return cls()
        
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
        
        # Convert string paths to Path objects
        if "project_root" in data:
            data["project_root"] = Path(data["project_root"])
        
        return cls(**data)
    
    def save(self, config_path: Path = Path(".codedrift.yml")) -> None:
        """Save config to YAML file"""
        config_dict = self.dict()
        config_dict["project_root"] = str(config_dict["project_root"])
        
        with open(config_path, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False)
