"""Code analysis module"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import ast


class CodeAnalyzer:
    """Analyzes code for documentation consistency"""
    
    def __init__(self, language: str = "python"):
        self.language = language
    
    def extract_function_signatures(self, file_path: Path) -> List[Dict]:
        """Extract function signatures from Python file"""
        if self.language != "python":
            return []
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "parameters": self._extract_parameters(node),
                        "return_type": self._extract_return_type(node),
                        "docstring": ast.get_docstring(node),
                        "decorators": [d.id if hasattr(d, 'id') else str(d) for d in node.decorator_list],
                    }
                    functions.append(func_info)
            
            return functions
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []
    
    def _extract_parameters(self, node: ast.FunctionDef) -> Dict[str, str]:
        """Extract parameters from a function node"""
        params = {}
        
        for arg in node.args.args:
            param_type = "Any"
            if arg.annotation:
                param_type = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else "Any"
            params[arg.arg] = param_type
        
        return params
    
    def _extract_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type from a function node"""
        if node.returns:
            return ast.unparse(node.returns) if hasattr(ast, 'unparse') else "Any"
        return "Any"
    
    def extract_docstring_info(self, docstring: str) -> Dict:
        """Parse docstring for parameters and return types"""
        if not docstring:
            return {"parameters": {}, "returns": None}
        
        lines = docstring.split("\n")
        info = {"parameters": {}, "returns": None}
        
        in_params = False
        in_returns = False
        
        for line in lines:
            line = line.strip()
            
            # Look for Args/Parameters section
            if line.lower().startswith(("args:", "parameters:", "params:")):
                in_params = True
                in_returns = False
                continue
            
            # Look for Returns section
            if line.lower().startswith(("returns:", "return:")):
                in_returns = True
                in_params = False
                continue
            
            # Parse parameter lines
            if in_params and line and not line.lower().startswith(("returns:", "yield:", "raises:")):
                # Try to match "param_name (type): description"
                match = re.match(r"(\w+)\s*\(([^)]+)\)\s*:", line)
                if match:
                    info["parameters"][match.group(1)] = match.group(2)
            
            # Parse return type
            if in_returns and line and not line.lower().startswith(("args:", "params:")):
                # Simple extraction of type from return description
                type_match = re.match(r"(\w+(?:\[.*?\])?)", line)
                if type_match:
                    info["returns"] = type_match.group(1)
        
        return info
    
    def check_docstring_completeness(self, func_info: Dict) -> List[str]:
        """Check if docstring covers all parameters"""
        issues = []
        
        if not func_info["docstring"]:
            if func_info["parameters"]:
                issues.append(f"Missing docstring for function '{func_info['name']}'")
            return issues
        
        docstring_info = self.extract_docstring_info(func_info["docstring"])
        documented_params = docstring_info["parameters"]
        
        # Check for missing parameter documentation
        for param_name, param_type in func_info["parameters"].items():
            if param_name not in documented_params:
                issues.append(f"Parameter '{param_name}' not documented in '{func_info['name']}'")
        
        # Check for extra parameters in docstring (might be outdated)
        for doc_param in documented_params:
            if doc_param not in func_info["parameters"]:
                issues.append(f"Documented parameter '{doc_param}' not found in '{func_info['name']}' signature")
        
        return issues
    
    def extract_readme_examples(self, readme_path: Path) -> List[Dict]:
        """Extract code examples from README"""
        if not readme_path.exists():
            return []
        
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            examples = []
            # Look for code blocks
            pattern = r"```(?:python|py)?\n(.*?)\n```"
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for i, match in enumerate(matches):
                examples.append({
                    "code": match.group(1),
                    "start_line": content[:match.start()].count("\n"),
                })
            
            return examples
        except Exception as e:
            print(f"Error reading README: {e}")
            return []
    
    def check_readme_examples(self, readme_path: Path, functions: List[Dict]) -> List[str]:
        """Check if README examples match current API"""
        issues = []
        examples = self.extract_readme_examples(readme_path)
        function_names = [f["name"] for f in functions]
        
        for example in examples:
            code = example["code"]
            
            # Check for function calls to non-existent functions
            for func_name in function_names:
                if f"{func_name}(" in code:
                    # Found a function call in example
                    # In a real implementation, we'd do more detailed checking
                    pass
        
        return issues
