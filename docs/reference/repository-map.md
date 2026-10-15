# JARVIS Repository Map

This document provides a comprehensive structural and functional map of the JARVIS codebase. It details subsystem ownership, module responsibilities, key entry points, and architectural domains across the repository.

---

## 1. Top-Level Directory Layout

```
jarvis-ai/
├── src/jarvis/              # Core Python runtime (Control Plane, Voice, Gateway, Execution)
├── frontend/                # Browser client (WebGL 3D Signal Orb, Audio Streaming, Gateway Client)
├── substrate/               # Node.js/TypeScript execution substrate and extensions
├── tests/                   # Pytest test suite (unit, integration, and security tests)
├── docs/                    # Complete technical documentation and knowledge base
├── .github/workflows/       # Continuous Integration workflows (ruff, mypy, pytest)
├── pyproject.toml           # Python package configuration and tool metadata
├── package.json             # Substrate and frontend package dependencies
└── Makefile                 # Developer convenience commands for test and lint
```

---

## 2. Python Core: `src/jarvis/`

The Python core implements the central control plane, policy enforcement, cognitive routing, real-time voice DSP, WebSocket gateway, and system execution adapters.

### 2.1. Top-Level Modules

- **[`src/jarvis/config.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/config.py)**: Defines `JarvisSettings`, the pydantic-settings centralized configuration schema governing all 60+ environment variables, defaults, paths, and timeouts.
- **[`src/jarvis/telemetry.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telemetry.py)**: Logging configuration, structured JSON event logging, performance tracing, and metric collection.

---

### 2.2. Core Control Plane: `src/jarvis/core/`

The nerve center coordinating user interaction, memory retrieval, cognitive model reasoning, and action execution.

- **[`control_plane.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/core/control_plane.py)**: Implements `ControlPlane`, orchestrating the full conversational turn cycle:
  - Ingests incoming turn inputs from Gateway, Voice, Telegram, or WhatsApp.
  - Fetches working memory and compacts historical turns.
  - Selects model routes and queries LLM providers.
  - Dispatches tool invocations through the Action Broker.
  - Verifies execution outcomes and streams synthesized text or audio back to the user.
- **[`app_control_engine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/core/app_control_engine.py)**: Implements `AppControlEngine`, higher-level desktop coordination managing window focus, active application context, and cross-application workflows.

---

### 2.3. Voice and Audio Subsystem: `src/jarvis/voice/`

Implements low-latency duplex voice interaction, acoustic echo cancellation, and speech synthesis.

- **[`audio_aec.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/audio_aec.py)**: Advanced DSP acoustic echo cancellation engine:
  - Real-time WASAPI audio loopback reference stream capture.
  - Partitioned Block Frequency-Domain Adaptive Filtering (PBFDAF).
  - Coherence-based double-talk detection (DTD) and spectral subtraction.
- **[`microphone.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/microphone.py)**: Continuous audio input streaming via PyAudio / WASAPI input channels.
- **[`input_gate.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/input_gate.py)**: Energy-based voice activity detection (VAD), silence thresholding, and noise gate.
- **[`state_machine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/state_machine.py)**: `VoiceStateMachine` managing voice states (`IDLE`, `LISTENING`, `THINKING`, `SPEAKING`, `INTERRUPTED`) and barge-in transitions.
- **[`output_tracker.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/output_tracker.py)**: Tracks active speaker playback audio timestamps and chunk deliveries to correlate echo references.
- **[`synthesizer.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/synthesizer.py)**: Text-to-Speech (TTS) engine wrapping Edge-TTS and local speech synthesizers.

---

### 2.4. Policy & Security Engine: `src/jarvis/policy/`

Enforces least privilege, user approvals, and capability-based security.

- **[`firewall.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/firewall.py)**: Defines all system capabilities (`CAPABILITY_SYSTEM_EXEC`, `CAPABILITY_FS_WRITE`, `CAPABILITY_BROWSER_CONTROL`, etc.) and maps tool schemas to required capabilities.
- **[`engine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/engine.py)**: `PolicyEngine` evaluating action requests against session permissions, user roles, and execution constraints.
- **[`approvals.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/approvals.py)**: `ApprovalManager` handling interactive human-in-the-loop elevation challenges for high-risk operations.

---

### 2.5. Action Broker & Tool Registry: `src/jarvis/actions/`

- **[`registry.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/actions/registry.py)**: Central registry of callable system tools, parameter schemas, and metadata.
- **[`broker.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/actions/broker.py)**: `ActionBroker` coordinating tool validation, policy checks, execution dispatching to local handlers or Substrate Bridge, and outcome verification.

---

### 2.6. Execution Subsystems: `src/jarvis/execution/`

Adapters connecting JARVIS to the operating system, browsers, and external runtimes.

- **[`substrate_bridge.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/substrate_bridge.py)**: Subprocess supervisor managing the Node.js TypeScript substrate via bidirectional stdio JSON-RPC.
- **`windows/` (Native Windows Automation)**:
  - **[`app_registry.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/app_registry.py)**: Scans Windows registry, Start Menu shortcuts, and PATH for installed software.
  - **[`app_launcher.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/app_launcher.py)**: Launches applications with argument injection and working directory isolation.
  - **[`window_manager.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/window_manager.py)**: Win32 API window control (focus, maximize, minimize, move, enumerate).
  - **[`uia.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/uia.py)**: Microsoft UI Automation COM wrapper for desktop accessibility tree inspection and control invocation.
  - **[`shell.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/shell.py)**: Safe PowerShell / CMD command execution with timeouts and output capture.
  - **[`filesystem.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/filesystem.py)**: Sandboxed local file operations (read, write, list, delete).
  - **[`process.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/process.py)**: Process lifecycle monitoring and termination.
  - **[`system.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/system.py)**: System metrics (CPU, RAM, disk, battery status).
  - **[`desktop.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/desktop.py)**: Desktop screen capture and coordinate translation.
  - **[`winsta.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/winsta.py)**: Windows station and desktop session token detection.
- **`browser/` (Browser Automation)**:
  - **[`host.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/browser/host.py)**: Playwright Chromium browser manager with Chrome DevTools Protocol (CDP) connectivity.
  - **[`session.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/browser/session.py)**: Interactive browser session handling DOM interaction, navigation, clicks, and semantic accessibility snapshots.
- **`whatsapp/` (WhatsApp Desktop Subsystem)**:
  - **[`store.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/whatsapp/store.py)**: SQLite caching for WhatsApp contact phone numbers and conversation history.
  - **[`resolver.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/whatsapp/resolver.py)**: Resolves contact names and nicknames to international phone numbers.
  - **[`unread.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/whatsapp/unread.py)**: Inspects unread message counts via UI Automation.
  - **[`voice_caller.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/whatsapp/voice_caller.py)**: Automates WhatsApp desktop voice calling workflows via UI element clicks.
  - **[`node.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/whatsapp/node.py)**: Integrates WhatsApp messaging through Substrate Baileys protocol extension.
- **`computer/` (Computer Use)**:
  - **[`contract.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/computer/contract.py)**: Defines schema contracts for low-level mouse and keyboard actions.

---

### 2.7. Cognition & LLM Routing: `src/jarvis/cognition/`

- **[`model_router.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/model_router.py)**: Dynamic LLM router managing task complexity classification, candidate priority cascades, and multi-tier fallbacks.
- **[`quota_manager.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/quota_manager.py)**: Tracks token usage, rate limits, and provider budget exhaustion.
- **[`gemini_live.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/gemini_live.py)**: Manages low-latency bidirectional WebSocket audio streaming sessions with Gemini Live API.
- **[`web_search.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/web_search.py)**: Integrated web search query synthesis and result ranking.
- **`providers/`**:
  - **[`base.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/providers/base.py)**: Abstract base class for model providers (`BaseModelProvider`).
  - **[`google_genai.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/providers/google_genai.py)**: Native Google GenAI SDK integration (`gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.8-live`).
  - **[`groq_provider.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cognition/providers/groq_provider.py)**: Groq API client integration (`llama-3.3-70b-versatile`).

---

### 2.8. Memory Subsystem: `src/jarvis/memory/`

- **[`manager.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/manager.py)**: Unified interface for working memory, episodic conversation logs, and semantic factual memory.
- **[`working.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/working.py)**: In-memory sliding window of immediate conversation turns.
- **[`context_engine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/context_engine.py)**: Assembles system prompts, dynamic memory snippets, active tasks, and tool schemas.
- **[`ranking.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/ranking.py)**: Multi-factor search ranking combining BM25 relevance score and exponential temporal decay.
- **[`standing_intents.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/standing_intents.py)**: Persistent active goals and recurring background user mandates.
- **[`governance.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/memory/governance.py)**: Privacy filters and retention expiration sweeps for stored memories.

---

### 2.9. Gateway & Networking: `src/jarvis/gateway/`

- **[`server.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/gateway/server.py)**: Asyncio WebSocket Gateway server managing client connections, authentication, and heartbeats.
- **[`web_server.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/gateway/web_server.py)**: AIOHTTP HTTP server hosting static frontend assets and REST health endpoints.
- **[`protocol.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/gateway/protocol.py)**: Strict dataclass definitions for JSON-RPC wire frames (`RequestFrame`, `ResponseFrame`, `EventFrame`).
- **[`connection_manager.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/gateway/connection_manager.py)**: Tracks active sessions, client channels, and broadcast event routing.

---

### 2.10. Storage & Migrations: `src/jarvis/storage/`

- **[`database.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/storage/database.py)**: SQLite database engine with Write-Ahead Logging (WAL), foreign keys, and synchronous NORMAL settings.
- **[`migrations.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/storage/migrations.py)**: Sequential schema migrations and FTS5 virtual table initialization.

---

### 2.11. Telegram Remote Integration: `src/jarvis/telegram/`

- **[`service.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/service.py)**: Long-polling Telegram bot service routing incoming updates into the Control Plane.
- **[`pairing.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/pairing.py)**: Ephemeral 6-digit cryptographic pairing code generator and authorization validator.
- **[`authorizer.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/authorizer.py)**: Verifies user ID whitelist and chat privileges.
- **[`live_session.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/live_session.py)**: Dedicated background session keeping Telegram conversations synchronized with desktop memory.
- **[`keyboards.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/keyboards.py)**: Inline interactive approval buttons (`Approve` / `Deny`).
- **[`cards.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/cards.py)**: Formats structured message cards for task status and system metrics.
- **[`formatters.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/telegram/formatters.py)**: Escapes MarkdownV2 entities and sanitizes outbound responses.

---

### 2.12. Agent Communication Protocol (ACP) & Sandbox: `src/jarvis/acp/`

- **[`broker.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/acp/broker.py)**: Inter-agent message broker for multi-agent delegation.
- **[`permission_relay.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/acp/permission_relay.py)**: Relays approval prompts and security context between child agents and user.
- **[`sandbox.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/acp/sandbox.py)**: Isolated filesystem and execution container for delegated specialist sub-agents.
- **[`validator.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/acp/validator.py)**: Validates input/output schemas of specialist agent messages.
- **[`models.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/acp/models.py)**: Data contracts for ACP messages and envelopes.

---

### 2.13. Specialist Agents: `src/jarvis/agents/`

- **[`delegator.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/agents/delegator.py)**: Inspects complex user requests and decomposes them across specialist agents.
- **[`specialists.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/agents/specialists.py)**: Domain-specific prompt definitions and tool constraints for specialized subagents (researcher, coder, system operator).
- **[`models.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/agents/models.py)**: Agent lifecycle states and capability definitions.

---

### 2.14. Artifacts Subsystem: `src/jarvis/artifacts/`

- **[`store.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/artifacts/store.py)**: Local disk store managing generated artifacts (code snippets, images, reports, logs).
- **[`sidecar.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/artifacts/sidecar.py)**: Sidecar metadata index tracking artifact creation timestamps, hashes, and MIME types.
- **[`emitters.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/artifacts/emitters.py)**: Emits artifact creation events to WebSocket and Telegram clients.
- **[`models.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/artifacts/models.py)**: Dataclasses for artifact payloads.

---

### 2.15. Cron & Background Scheduler: `src/jarvis/cron/`

- **[`scheduler.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cron/scheduler.py)**: Background task scheduler evaluating recurring cron intervals and triggering actions.
- **[`heartbeat.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cron/heartbeat.py)**: Periodic liveness tick monitoring background services and checking for stale tasks.
- **[`models.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cron/models.py)**: Dataclasses for recurring schedule entries.

---

### 2.16. Contracts: `src/jarvis/contracts/`

Houses foundational Pydantic and dataclass contracts shared across multiple layers:
- **`action.py`**: Action definitions and results.
- **`memory.py`**: Memory records and search parameters.
- **`model.py`**: Model requests, completions, and token metrics.
- **`node.py`**: Execution node topology and capabilities.
- **`policy.py`**: Policy decisions, risk tiers, and approval tickets.
- **`task.py`**: Task definitions and lifecycle states.

---

### 2.17. CLI: `src/jarvis/cli/`

- **[`commands.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cli/commands.py)**: Click/Typer CLI commands (`jarvis chat`, `jarvis app`, `jarvis gateway`, `jarvis whatsapp`, `jarvis telegram`, `jarvis test`).
- **[`__main__.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cli/__main__.py)**: Standard Python package execution entry point (`python -m jarvis`).

---

## 3. Frontend Web Client: `frontend/`

The frontend provides an interactive WebGL interface featuring a 12,000-particle Signal Orb, audio streaming, and WebSocket communication.

- **[`index.html`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/frontend/index.html)**: Main web application entry point hosting the canvas and UI overlays.
- **`css/`**:
  - **`main.css`**: Application typography, layout, response flight animations, and responsiveness.
  - **`orbs.css`**: Orb positioning, glow effects, and state styling.
- **`js/`**:
  - **`app.js`**: Main client-side orchestrator initializing components, handling keyboard shortcuts, and updating UI states.
  - **`config.js`**: Frontend configuration parameters (Gateway WebSocket URL, particle counts, animation physics).
  - **`components/signal-orb.js`**: Core 3D WebGL particle orb rendering 12,000 particles arranged in a spherical Fibonacci lattice. Manages dynamic particle displacement, state colors, and mouse interaction.
  - **`components/particle-field.js`**: Background ambient particle field animation.
  - **`components/speaking-orb.js`**: Auxiliary audio visualization ring responding to output playback energy.
  - **`audio/recorder.js`**: Browser Web Audio API microphone capture and 16 kHz PCM chunk streaming.
  - **`audio/player.js`**: Low-latency PCM audio chunk player with jitter buffer.
  - **`gateway/client.js`**: Client-side WebSocket manager handling automated reconnects and JSON-RPC dispatching.

---

## 4. Substrate Execution Engine: `substrate/`

The Node.js TypeScript substrate executes tools requiring high-speed Node ecosystem integrations, browser automation via CDP, and WhatsApp protocol sessions.

- **`runner/jarvis_substrate_runner.ts`**: Main TypeScript entry point communicating with Python `SubstrateBridge` over stdio JSON-RPC.
- **`worker/node-computer-protocol.ts`**: Substrate side of the computer use and tool execution protocol.
- **`security/`**:
  - **`dangerous-tools.ts`**: Identification and parameter guards for destructive tools.
  - **`exec-filesystem-policy.ts`**: Substrate path validation ensuring containment within authorized directories.
- **`extensions/whatsapp/`**: Baileys multi-device WhatsApp protocol integration for direct socket connectivity.
- **`shared/`**: Common TypeScript utilities (text chunking, JSON schema defaults, Markdown escaping, session unread tracking).

---

## 5. Test Suite: `tests/`

The repository maintains automated test coverage across all major architectural domains:

```
tests/
├── unit/                    # Unit tests for individual classes and functions
│   ├── test_config.py       # Configuration loading, validation, and defaults
│   ├── test_voice.py        # Voice state machine, VAD, and output tracking
│   ├── test_aec.py          # AEC math, PBFDAF filter, double-talk detection
│   ├── test_router.py       # Model routing logic, quota manager, candidate chains
│   ├── test_memory.py       # SQLite FTS5 search, temporal decay ranking
│   └── test_policy.py       # Capability firewall, risk evaluation, approvals
├── integration/             # Multi-component integration tests
│   ├── test_control_plane.py# Full turn execution cycle with mocked providers
│   ├── test_gateway.py      # WebSocket handshake, frame encoding, RPC dispatch
│   └── test_substrate.py    # Python-to-TypeScript stdio IPC bridge
└── security/                # Security and safety tests
    ├── test_firewall.py     # Forbidden path access, privilege elevation checks
    └── test_sanitization.py # Prompt injection defense and output escaping
```

---

## 6. Architectural Cross-Reference Matrix

| Subsystem Domain | Primary Python Modules | Frontend / Substrate Modules | Test Suites |
| :--- | :--- | :--- | :--- |
| **Control Plane** | `src/jarvis/core/control_plane.py` | `frontend/js/app.js` | `tests/integration/test_control_plane.py` |
| **Voice & AEC** | `src/jarvis/voice/*` | `frontend/js/audio/*` | `tests/unit/test_voice.py`, `test_aec.py` |
| **Cognition & Routing**| `src/jarvis/cognition/*` | N/A | `tests/unit/test_router.py` |
| **Memory & Storage** | `src/jarvis/memory/*`, `storage/*` | N/A | `tests/unit/test_memory.py` |
| **Policy & Security** | `src/jarvis/policy/*`, `acp/*` | `substrate/security/*` | `tests/unit/test_policy.py`, `tests/security/*` |
| **Execution Substrate**| `src/jarvis/execution/substrate_bridge.py` | `substrate/runner/*` | `tests/integration/test_substrate.py` |
| **Windows Automation**| `src/jarvis/execution/windows/*` | N/A | `tests/unit/test_windows.py` |
| **Gateway & Network** | `src/jarvis/gateway/*` | `frontend/js/gateway/*`| `tests/integration/test_gateway.py` |
| **UI & Visualization**| `src/jarvis/gateway/web_server.py` | `frontend/js/components/*` | `frontend/tests/signal-orb.test.cjs` |
| **Integrations** | `src/jarvis/telegram/*`, `whatsapp/*` | `substrate/extensions/whatsapp/*` | `tests/integration/test_integrations.py` |
