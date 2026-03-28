# AGENTS.md

This file contains guidelines for AI agents working in the `smart-trading` repository. Please follow these conventions strictly.

## Build, Lint, and Test

### Installation
Ensure your virtual environment is active:
```bash
source .venv/bin/activate
pip install -r algo-trading/requirements.txt
```

### Testing
Use `pytest` for all testing.

- **Run all tests:**
  ```bash
  pytest
  ```
- **Run a single test file:**
  ```bash
  pytest tests/path/to/test_file.py
  ```
- **Run a single test function:**
  ```bash
  pytest tests/path/to/test_file.py::test_function_name
  ```

### Linting and Formatting
This project enforces code quality and style using the following tools:
- **Formatting:** `black` for code, `isort` for imports.
- **Linting:** `flake8`.

Run these before submitting any changes:
```bash
black .
isort .
flake8 .
```

## Code Style Guidelines

### Imports
- Use `isort` to manage imports.
- Follow the order: standard library, third-party libraries, local project imports.

### Formatting
- Use `black` style (consistent indentation, 88 character line limit).

### Typing
- Use Python type hints (PEP 484) for all function arguments and return types.
- Favor `Optional`, `List`, `Dict`, `Union` from `typing` where appropriate.

### Naming Conventions
- **Functions/Methods:** `snake_case`.
- **Classes:** `PascalCase`.
- **Variables:** `snake_case`.
- **Constants:** `UPPER_SNAKE_CASE`.

### Error Handling
- Use specific exceptions rather than broad `Exception` clauses.
- Log errors using the standard `logging` module.

### Documentation
- Use Google-style docstrings for all classes and public methods.
- Explain the *why* rather than the *what* in code comments.

## Repository Structure
- `algo-trading/` — Core library (engine, data, strategies, utils).
- `strategies/` — Example strategies.
- `data/` — Sample datasets.
- `tests/` — Unit and integration tests.

## Security
- NEVER commit secrets (`.env`, `config.yml` with API keys) to the repository.
- Use environment variables for configuration.

## Git Commit Conventions
- Use conventional commit messages: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- Keep messages concise (under 50 characters).

## Agentic Coding Agent Guidelines

### General Principles
- **Be proactive:** Look for missing tests, unclear documentation, or outdated dependencies.
- **Verify before you finish:** Always run tests (`pytest`) and linting (`flake8`) before indicating a task is complete.
- **Context is key:** Before modifying code, search for usage patterns and existing tests to ensure changes are safe.
- **Minimize noise:** Do not add conversational filler in code comments or PR descriptions.

### Handling New Tasks
1. **Understand:** Read relevant files, check existing tests, and understand the problem.
2. **Plan:** Propose a brief, high-level plan to the user if the task is complex.
3. **Verify (Pre):** Run tests before making changes to establish a baseline.
4. **Implement:** Write code adhering to style guidelines.
5. **Verify (Post):** Run linting, formatting, and tests.
6. **Finalize:** Submit changes (if instructed) or inform the user.

### Refactoring
- Ensure you have a solid test suite covering the area you are refactoring *before* you start.
- If no tests exist, write them first.
- Keep refactorings separate from feature implementation.
