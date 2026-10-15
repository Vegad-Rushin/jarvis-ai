# Contributing to JARVIS

This guide outlines development practices, engineering rules, quality gates, and code review standards for contributing to the JARVIS project.

---

## 1. Core Engineering Invariants

Every contribution must strictly adhere to the project's non-negotiable core invariants:

### Rule 1: Never Hardcode Anything
- **Dynamic Configuration**: Never hardcode API endpoints, credentials, filesystem paths, timeouts, model names, or environment flags.
- **Config Precedence**: All configurable values must be defined in `JarvisSettings` (`src/jarvis/config.py`) and overridable via environment variables.
- **Cross-Platform Portability**: Always use `pathlib.Path` for path manipulations. Never use OS-specific path separators or Unix-only shell commands.

### Rule 2: Strict Communication & Commit Standards
- **Conventional Commits**: All commit messages must follow the Conventional Commits specification:
  - `feat(scope): add new capability`
  - `fix(scope): resolve issue in component`
  - `refactor(scope): streamline internal implementation`
  - `docs(scope): update reference documentation`
  - `test(scope): add test coverage for module`
- **Terminology Invariant**: Never use the forbidden term `"s-t-a-g-e"` or its plural form anywhere in commit messages, user-facing text, documentation, comments, or docstrings. Document engineering progress by architectural domain, capability, or functional component.

### Rule 3: Data Safety & Privacy Invariant
- Never delete or modify user files, databases, or project assets without explicit verification and confirmation.
- Private session files (`sessions.json`, `conversations.json`, `*.log`, `*.jsonl`, `.env`, `coverage.xml`) must remain strictly gitignored and never tracked in version control.

### Rule 4: Zero Regression & Quality Gates
- Maintain a 100% test pass rate (`pytest`).
- Maintain 100% strict type safety (`mypy src tests`).
- Maintain 100% clean formatting and linting (`ruff check .`, `ruff format --check .`).
- Maintain valid JavaScript syntax (`node --check frontend/js/...`).

---

## 2. Development Workflow

### 2.1. Branching Strategy

Create dedicated branch names based on the nature of the change:
- `feature/<domain-or-capability>` (e.g. `feature/audio-dsp-enhancement`)
- `fix/<issue-description>` (e.g. `fix/sqlite-wal-locking`)
- `cleanup/<scope>` (e.g. `cleanup/repo-hygiene`)
- `docs/<scope>` (e.g. `docs/rebuild-knowledge-base`)

### 2.2. Setting Up Local Environment

```bash
# Clone the repository
git clone https://github.com/deepakrakshit/jarvis-ai.git
cd jarvis-ai

# Set up Python virtual environment with uv
uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install development dependencies
uv pip install -e ".[dev]"

# Install Substrate npm packages
npm install
```

### 2.3. Pre-Commit Verification Checklist

Before pushing commits or opening a pull request, run the complete verification suite locally:

```bash
# 1. Format code
ruff format .

# 2. Run linter
ruff check .

# 3. Check types
mypy src tests

# 4. Run automated tests
pytest

# 5. Check frontend syntax
node --check frontend/js/app.js
node --check frontend/js/config.js
node --check frontend/js/components/signal-orb.js
node --check frontend/js/gateway/client.js
```

---

## 3. Code Style and Conventions

- **Python**: Follow PEP 8 style, enforced strictly via Ruff with 100-character line limits.
- **Type Annotations**: All function signatures, parameters, and return types must be fully annotated. Avoid `Any` wherever a specific type or union can be declared.
- **Asynchronous Code**: Prefer `asyncio` for all I/O operations (file reading, network requests, subprocess communication). Avoid blocking calls in the main event loop thread.
- **Error Handling**: Use custom domain exceptions deriving from `JarvisError`. Never silently catch or swallow unexpected exceptions.

---

## 4. Pull Request Review Guidelines

When reviewing or submitting pull requests:

1. **Verify Evidence**: All PRs must include test output proving that new code passes existing and new test cases.
2. **Review Scope**: Keep PRs focused on a single architectural domain or capability. Avoid mixing unrelated refactors into feature PRs.
3. **Documentation**: Any change to configuration schemas, CLI commands, API frames, or system behavior must update the corresponding files in `docs/`.
