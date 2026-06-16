# CodeDrift Project Structure

```
CodeDrift/
├── codedrift/                 # Main package
│   ├── __init__.py           # Package initialization
│   ├── analyzer.py           # Code analysis logic
│   ├── cli.py                # Command-line interface
│   ├── config.py             # Configuration management
│   ├── detector.py           # Drift detection engine
│   └── models.py             # Data models
├── tests/                     # Test suite
│   └── test_codedrift.py    # Unit tests
├── examples/                  # Example files
│   └── example_api.py        # Example API with drifts
├── docs/                      # Documentation
├── .github/
│   └── workflows/            # GitHub Actions
│       └── codedrift.yml    # CI/CD pipeline
├── .codedrift.yml            # Configuration file
├── main.py                    # Entry point
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # Contribution guidelines
```

## Quick Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run CodeDrift
```bash
python main.py check          # Check for drifts
python main.py health         # Show health score
python main.py init           # Initialize config
python main.py fix            # Auto-fix drifts
python main.py export         # Export report
```

### Run Tests
```bash
pytest tests/
```

### Format Code
```bash
black codedrift/ tests/
```

## Module Overview

### `analyzer.py`
Analyzes code files to extract function signatures, docstrings, and check documentation consistency.

### `detector.py`
Main drift detection engine. Scans projects and identifies mismatches between code and documentation.

### `cli.py`
Command-line interface using Typer. Provides user-friendly commands for checking, fixing, and exporting drifts.

### `config.py`
Handles `.codedrift.yml` configuration files with Pydantic models.

### `models.py`
Data models for drifts, analysis results, and function signatures.

## Key Features

✅ Automatic documentation drift detection
✅ Function signature analysis
✅ Docstring completeness checking
✅ README example validation
✅ Health score calculation
✅ Multiple output formats (text, JSON, GitHub Actions)
✅ Configuration management
✅ Extensible design for multiple languages
