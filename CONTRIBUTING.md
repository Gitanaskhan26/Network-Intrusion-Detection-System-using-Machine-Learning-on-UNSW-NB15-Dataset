# Contributing to Network Intrusion Detection System

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed**
- **Explain which behavior you expected to see instead**
- **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the behavior you expected to see**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Follow the Python style guide (PEP 8)
- Include appropriate test cases
- Document new code
- End all files with a newline

## Development Setup

1. Fork the repo
2. Clone your fork
3. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Create a branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Style Guidelines

### Python Style Guide

- Follow PEP 8
- Use meaningful variable names
- Write docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Project Structure

Please maintain the existing project structure when adding new components:

```
networksecurity/
├── components/      # Pipeline components
├── entity/          # Data classes
├── pipeline/        # Pipeline orchestration
├── utils/           # Utility functions
├── exception/       # Custom exceptions
└── logging/         # Logging configuration
```

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update comments if changing existing code

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for your contributions! 🚀
