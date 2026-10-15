# AI Agent Guidelines for JARVIS Development

This document defines operational rules, development protocols, and safety constraints for autonomous AI coding agents operating within the JARVIS codebase.

---

## 1. Prime Invariants

Any AI coding agent modifying or reading this repository must strictly adhere to these core rules:

### Rule 1: Never Hardcode Anything
- Always parameterize configurations, paths, timeouts, URLs, and model identifiers.
- Route all system configuration through `JarvisSettings` in [`src/jarvis/config.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/config.py).
- Use cross-platform abstractions (`pathlib.Path`) for all filesystem interactions. Never assume Unix utilities (`rm`, `sed`, `awk`) or Windows-only backslashes in path strings.

### Rule 2: Strict Communication & Commit Standards
- **Forbidden Word Constraint**: Never write the term `"s-t-a-g-e"` or its plural form anywhere in user responses, commit messages, code, comments, or docstrings.
- **Milestone Documentation**: Always describe architectural progress by functional capability, domain, or component, never by numbered progression milestones.
- **Conventional Commits**: Format all commit messages according to the Conventional Commits specification (`feat(...)`, `fix(...)`, `refactor(...)`, `docs(...)`, `test(...)`).

### Rule 3: Data Safety and Privacy
- Never modify or delete user data, databases (`jarvis.db`), private tokens, or session artifacts without explicit confirmation.
- Ensure private runtime files (`sessions.json`, `conversations.json`, `*.log`, `*.jsonl`, `.env`, `coverage.xml`) are strictly gitignored and never tracked in Git.

### Rule 4: Zero Regression & Quality Gates
Before concluding any task, verify that all four engineering gates pass with zero errors:
1. `pytest` (100% pass rate).
2. `mypy src tests` (strict mode, zero errors).
3. `ruff check .` (zero lint violations).
4. `ruff format --check .` (zero formatting discrepancies).
5. `node --check frontend/js/...` (valid JavaScript syntax).

---

## 2. Operational Protocol for AI Agents

### Step 1: Pre-Modification Inspection
- Check current git status: verify active branch, uncommitted modifications, and untracked files.
- Establish the baseline state before proposing or writing changes.
- Never overwrite, reset, or silently discard pre-existing user modifications.

### Step 2: Implementation Integrity
- Keep changes minimal, targeted, and scoped strictly to the task.
- Preserve all existing comments, docstrings, and documentation unless specifically instructed to modify them.
- Avoid replacing working implementations with theoretical abstractions simply because they look cleaner.

### Step 3: Verification Execution
- Do not assume that because a file was edited cleanly it functions correctly.
- Execute the test suite and verify edge cases.
- If a test fails, diagnose the root cause rather than weakening assertions or disabling test cases.

---

## 3. Subsystem Knowledge Shortcuts

When debugging or implementing features in specific subsystems, refer directly to these canonical documentation files:

| Subsystem Domain | Primary Documentation | Key Source Files |
| :--- | :--- | :--- |
| **Control Plane** | [`docs/architecture/control-plane.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/architecture/control-plane.md) | `src/jarvis/core/control_plane.py` |
| **Voice & AEC** | [`docs/subsystems/audio-aec.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/audio-aec.md) | `src/jarvis/voice/audio_aec.py` |
| **Signal Orb UI** | [`docs/subsystems/signal-orb-and-ui.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/signal-orb-and-ui.md) | `frontend/js/components/signal-orb.js` |
| **Gateway & Protocol**| [`docs/subsystems/gateway-and-websockets.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/gateway-and-websockets.md) | `src/jarvis/gateway/*` |
| **Policy Firewall** | [`docs/subsystems/action-broker-and-policy.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/action-broker-and-policy.md) | `src/jarvis/policy/*` |
| **Substrate Bridge** | [`docs/subsystems/execution-substrate.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/execution-substrate.md) | `src/jarvis/execution/substrate_bridge.py` |
| **Windows Automation**| [`docs/subsystems/windows-automation.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/subsystems/windows-automation.md) | `src/jarvis/execution/windows/*` |
| **Model Routing** | [`docs/architecture/model-routing.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/architecture/model-routing.md) | `src/jarvis/cognition/*` |
| **Memory System** | [`docs/architecture/memory-and-persistence.md`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/docs/architecture/memory-and-persistence.md) | `src/jarvis/memory/*` |
