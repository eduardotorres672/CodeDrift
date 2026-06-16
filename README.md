# CodeDrift - Keep Your Code and Documentation in Sync

![CodeDrift Logo](https://img.shields.io/badge/CodeDrift-v0.1.0-blue)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

🔍 **CodeDrift** automatically detects and fixes divergences between your code and documentation, keeping everything perfectly synchronized.

## ✨ Features

- 🎯 **Automatic Detection** - Finds documentation drifts in seconds
- 🔧 **Smart Fixes** - Suggests or automatically applies corrections
- 📊 **Health Score** - Visual documentation quality metrics
- 🚀 **CI/CD Ready** - GitHub Actions, pre-commit hooks, and more
- 🧠 **AI-Powered** - LLM suggestions for contextual fixes
- 🌐 **Multi-Language** - Python, TypeScript, JavaScript, and more
- 📝 **OpenAPI Support** - Validates and syncs API specs

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Initialize Configuration

```bash
python main.py init
```

### Check for Drifts

```bash
python main.py check
```

### View Health Score

```bash
python main.py health
```

### Export Report

```bash
python main.py export --output drift-report.json
```

## 📋 What Can CodeDrift Detect?

### 1. **Docstring Inconsistencies**
```python
def get_user(user_id: int, include_profile: bool) -> dict:
    """Get user by ID.
    
    Args:
        user_id (int): User ID
        # ❌ Missing 'include_profile' parameter!
    """
```

### 2. **Function Signature Mismatches**
```python
# Code
def create_post(title: str, content: str, author_id: int) -> dict:

# Documentation says:
# def create_post(title: str, content: str) -> dict:
# ❌ Missing 'author_id' parameter!
```

### 3. **Outdated README Examples**
```markdown
# README
User endpoint returns only `{ id, name, email }`
# But the code actually returns:
{ id, name, email, profile, verified_at }
# ❌ Documentation is outdated!
```

### 4. **Type Inconsistencies**
```python
# Docstring says returns int
# Code actually returns str
# ❌ Mismatch detected!
```

## 🎯 Use Cases

### For Individual Developers
```bash
# Before committing
python main.py check
# Get instant feedback on documentation quality
```

### In CI/CD Pipelines
```yaml
- name: Check Documentation Sync
  run: python main.py check --output github
```

### For Teams
```bash
# Dashboard view
python main.py health
# See documentation health trends over time
```

## 📊 Example Output

```
Found 3 drift(s):

┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳═══════════════════════┳══════════════┳═════┓
┃ Type                    ┃ Severity  ┃ Title                 ┃ File         ┃ Line ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇═══════════════════════╇══════════════╇═════┩
│ missing_docstring       │ ⚠️ warning │ Missing docstring     │ users.py     │ 45  │
│ parameter_mismatch      │ ❌ error   │ Parameter mismatch    │ posts.py     │ 67  │
│ readme_outdated         │ ⚠️ warning │ Example out of date   │ README.md    │ 120 │
└─────────────────────────┴───────────┴───────────────────────┴──────────────┴─────┘

📊 Health Score: 85/100
📁 Files analyzed: 12
```

## ⚙️ Configuration

Edit `.codedrift.yml` in your project root:

```yaml
languages:
  - python
  - typescript

include_patterns:
  - "**/*.py"
  - "**/*.ts"

exclude_patterns:
  - "**/node_modules/**"
  - "**/.venv/**"

check_jsdoc: true
check_openapi: true
check_readme: true
severity_threshold: warning

ai_enabled: true  # Optional: enable AI suggestions
auto_fix: false   # Optional: auto-fix drifts
```

## 🔧 CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py check` | Scan for documentation drifts |
| `python main.py health` | Show documentation health score |
| `python main.py init` | Initialize configuration |
| `python main.py fix` | Automatically fix drifts |
| `python main.py export` | Export drift report as JSON |

## 📦 Pre-commit Hook

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

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🌟 Roadmap

- [ ] VSCode Extension for inline drift detection
- [ ] Web dashboard with drift trends
- [ ] Multi-language support (Go, Java, Rust, C#)
- [ ] OpenAPI 3.1 full support
- [ ] Documentation generation
- [ ] Slack/Discord integration
- [ ] Enterprise features (SAML, audit logs)

---

**Made with ❤️ by the CodeDrift Team**

*Keep your code and documentation in perfect sync* ✨
