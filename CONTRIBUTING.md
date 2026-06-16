# Contributing to CodeDrift

Thank you for your interest in contributing to CodeDrift! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Install development dependencies: `pip install -r requirements.txt`

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

We use black for code formatting:

```bash
black codedrift/ tests/
```

### Type Checking

```bash
mypy codedrift/
```

## Areas for Contribution

- 🐛 **Bug fixes** - Report and fix bugs
- ✨ **Features** - Add new language support, detection types, etc.
- 📚 **Documentation** - Improve docs and examples
- 🧪 **Tests** - Increase test coverage
- 🎨 **UI/UX** - Improve CLI output and visualization

## Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Example: "Add TypeScript support" or "Fix parameter detection bug"

## Pull Request Process

1. Update tests for any new functionality
2. Ensure all tests pass: `pytest`
3. Update README if needed
4. Submit PR with clear description of changes

## Questions?

Open an issue or start a discussion on GitHub!

---

Happy coding! 🚀
