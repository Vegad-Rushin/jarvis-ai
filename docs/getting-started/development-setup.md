# Development Environment & Quality Gates

This document provides instructions for developers contributing to the JARVIS codebase, detailing the local development workflow, quality verification gates, and architectural invariants.

---

## 1. Prerequisites & Developer Tooling

Ensure your development environment has the following installed:
- **Python 3.10+ (64-bit)** with `pip` and `venv`.
- **Node.js 18+ LTS** for TypeScript execution substrate and frontend syntax verification.
- **Git** with support for Conventional Commits.
- An IDE with active Python typing, linting, and formatting extensions (VS Code or PyCharm recommended).

---

## 2. Setting Up the Local Workspace

```powershell
# 1. Activate your virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Install editable package with development dependencies
python -m pip install -e ".[dev]"

# 3. Verify that development tools are available
python -m ruff --version
python -m mypy --version
python -m pytest --version
```

---

## 3. The Four Core Invariants

Every modification submitted to JARVIS must satisfy four fundamental engineering invariants:

1. **Top-Most Invariant (Never Hardcode Anything):**
   - Dynamic configuration: Never hardcode endpoints, file paths, model names, timeouts, ports, or credentials.
   - Everything must be discoverable, parameterized, and driven by `JarvisSettings` ([`src/jarvis/config.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/config.py)), environment variables, or runtime discovery.
   - Cross-platform path handling: Use `pathlib.Path` instead of hardcoded Windows string paths or Unix assumptions.
2. **Strict Communication & Commit Standards:**
   - Follow Conventional Commits: `feat(...)`, `fix(...)`, `docs(...)`, `refactor(...)`, `test(...)`, `chore(...)`.
   - Document progress by functional capability and domain, never by numbered milestones.
   - **Absolute prohibition:** Never use the word "s-t-a-g-e" or its plural anywhere in user responses, commit messages, code, comments, or docstrings.
3. **Data Safety & Privacy Invariant:**
   - Never delete or modify user files, databases, or project assets without explicit authorization.
   - Keep private runtime session files (`sessions.json`, `conversations.json`, `*.log`, `*.jsonl`, `.env`, `coverage.xml`, `jarvis.db`) strictly gitignored.
4. **100% Quality Verification Gates:**
   - 100% test pass rate (`pytest`).
   - 100% strict type safety (`mypy src tests`).
   - 100% clean formatting and linting (`ruff check .`, `ruff format --check .`).

---

## 4. The Local Quality Verification Suite

Before pushing changes or submitting a pull request, run the complete suite of quality verification checks:

```powershell
# 1. Python Linter
python -m ruff check .

# 2. Python Code Formatter Check
python -m ruff format --check .

# 3. Static Type Checking (Strict Mode)
python -m mypy src tests

# 4. Frontend JavaScript Syntax Validation
node --check frontend/js/app.js frontend/js/config.js frontend/js/audio/player.js frontend/js/audio/recorder.js frontend/js/components/particle-field.js frontend/js/components/signal-orb.js frontend/js/components/speaking-orb.js frontend/js/gateway/client.js

# 5. Full Test Suite Execution
python -m pytest
```

### Running Targeted Tests During Development
To run specific test modules quickly:

```powershell
# Test Control Plane and cognitive execution
python -m pytest tests/test_control_plane.py -v

# Test Audio Acoustic Echo Cancellation DSP
python -m pytest tests/test_audio_aec.py -v

# Test Windows Application Control and UI Automation
python -m pytest tests/test_app_control.py -v

# Test Telegram Remote Control Daemon
python -m pytest tests/test_telegram_live.py -v
```

---

## 5. Working with External APIs During Testing

- Tests are architected to run deterministically using offline mocks by default.
- Paid external APIs (Gemini Live, Groq, WhatsApp telephony) are never called in automated unit tests unless live credentials are explicitly provided in environment variables.
- When running in an environment without physical audio capture devices, audio unit tests utilize synthetic PCM 16kHz sine waves and loopback mock streams.
