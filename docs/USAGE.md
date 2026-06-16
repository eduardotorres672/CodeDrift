# CodeDrift CLI Usage Guide

## Installation

```bash
pip install -r requirements.txt
```

## Commands

### 1. Check for Drifts

Scan your project for documentation inconsistencies.

```bash
python main.py check
python main.py check --path ./my-project
python main.py check --output json   # JSON format
python main.py check --output github # GitHub Actions format
```

**Output:**
```
Found 3 drift(s):

┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳═══════════════════════┳══════════════┳═════┓
┃ Type                    ┃ Severity  ┃ Title                 ┃ File         ┃ Line ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇═══════════════════════╇══════════════╇═════┩
│ missing_docstring       │ warning   │ Missing docstring     │ users.py     │ 45  │
└─────────────────────────┴───────────┴───────────────────────┴──────────────┴─────┘
```

### 2. View Health Score

Get a quick overview of your documentation quality.

```bash
python main.py health
```

**Output:**
```
📊 Documentation Health Score

92.5/100 ███████████████████████████░░
Files analyzed: 12
Total drifts: 2
```

### 3. Initialize Configuration

Create a `.codedrift.yml` configuration file.

```bash
python main.py init
```

**Creates `.codedrift.yml`:**
```yaml
languages:
  - python
  - typescript

check_jsdoc: true
check_readme: true
severity_threshold: warning
```

### 4. Auto-Fix Drifts

Automatically fix detected drifts (experimental).

```bash
python main.py fix
python main.py fix --approve  # Skip confirmation
```

### 5. Export Report

Save analysis results to a JSON file.

```bash
python main.py export
python main.py export --output ./reports/drift-report.json
```

**Output:** `codedrift-report.json`
```json
{
  "timestamp": "2024-06-15T10:30:00",
  "summary": {
    "files_analyzed": 12,
    "total_drifts": 2,
    "health_score": 92.5,
    "by_severity": {
      "error": 1,
      "warning": 1,
      "info": 0,
      "critical": 0
    }
  },
  "drifts": [...]
}
```

## Configuration (.codedrift.yml)

```yaml
# Supported languages
languages:
  - python
  - typescript
  - javascript

# Files to include
include_patterns:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.js"

# Files to exclude
exclude_patterns:
  - "**/node_modules/**"
  - "**/.venv/**"

# Detection options
check_jsdoc: true        # Check JSDoc/docstrings
check_openapi: true      # Check OpenAPI specs
check_readme: true       # Check README examples
check_types: true        # Check TypeScript types

# Reporting
severity_threshold: warning  # info | warning | error

# AI Features
ai_enabled: false
ai_provider: openai

# Auto-fixing
auto_fix: false
```

## Integration Examples

### GitHub Actions

Add to `.github/workflows/codedrift.yml`:

```yaml
name: CodeDrift Check
on: [pull_request, push]

jobs:
  codedrift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python main.py check --output github
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: codedrift
      name: CodeDrift Check
      entry: python main.py check
      language: system
      types: [python]
```

### Makefile

```makefile
.PHONY: check health export

check:
	python main.py check

health:
	python main.py health

export:
	python main.py export

fix:
	python main.py fix --approve
```

## Exit Codes

- `0` - No issues found
- `1` - Errors detected
- `2` - Critical errors detected

## Examples

### Check with custom path
```bash
python main.py check --path ~/projects/myapp
```

### Export and view report
```bash
python main.py export --output report.json
cat report.json | jq '.summary'
```

### Continuous monitoring
```bash
watch -n 60 'python main.py health'  # Update every 60s
```

## Troubleshooting

### No drifts found?
- Check `.codedrift.yml` configuration
- Verify file patterns match your project
- Ensure Python files have docstrings

### High number of false positives?
- Adjust `severity_threshold` in config
- Update `exclude_patterns` to skip files
- Add custom rules to `.codedrift.yml`

---

For more help: `python main.py --help`
