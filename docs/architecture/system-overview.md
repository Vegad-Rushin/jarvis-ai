# System Architecture Overview

JARVIS is architected as an autonomous personal artificial intelligence operating system. Rather than running as a superficial chatbot wrapper, it operates as an operating-system-level cognitive control plane that pairs low-latency multimodal reasoning with deterministic Windows desktop execution.

---

## 1. System Blueprint & High-Level Architecture

JARVIS divides responsibilities cleanly between real-time cognitive reasoning, governance, and physical operating system execution:

```mermaid
graph TD
    User(["👤 Operator: Voice / Screen / Text / Mobile"]) <-->|WebRTC PCM Audio & WebSockets| UI["🖥️ Neural 3D Desktop UI (frontend/)"]
    User <-->|Telegram Smartphone Remote| TelegramBot["📱 Telegram Daemon (telegram/service.py)"]
    User <-->|Autonomous Voice Calls| WhatsAppVoIP["📞 WhatsApp VoIP Bridge (substrate/extensions/whatsapp)"]

    subgraph KERNEL ["JARVIS Cognitive Kernel & Control Plane (src/jarvis/)"]
        UI <-->|JSON-RPC WebSockets (ws://127.0.0.1:8765)| Gateway["🌐 Gateway Server (gateway/server.py)"]
        Gateway <--> ControlPlane["🧠 Control Plane (core/control_plane.py)"]
        
        subgraph COGNITION ["Cognitive Core"]
            GeminiLive["⚡ Gemini 3.8 Live Multimodal (cognition/gemini_live.py)"]
            ModelRouter["🔀 Multi-Model Router (cognition/model_router.py)"]
            ModelRouter --> GroqProviders["🧠 Specialist Models (GPT-OSS 120B, Qwen 3.8 27B)"]
        end

        ControlPlane <--> COGNITION
        ControlPlane <--> ActionBroker["🛡️ Action Broker (actions/broker.py)"]
        ControlPlane <--> PolicyEngine["🧱 Capability Firewall & Policy Engine (policy/engine.py)"]
        ControlPlane <--> MemoryFabric[("💾 Memory Fabric: SQLite WAL + FTS5 (storage/database.py)")]
    end

    subgraph AUDIO_SUBSYSTEM ["Audio DSP & Echo Cancellation Subsystem"]
        Mic["🎤 Physical Microphone"] --> PrimaryCapture["d(n) Primary Audio"]
        Speaker["🔊 Speakers / System Audio"] --> WASAPILoopback["x(n) Loopback Reference"]
        PrimaryCapture --> AEC["🎛️ PBFDAF Adaptive Filter & Spectral Mask (voice/audio_aec.py)"]
        WASAPILoopback --> AEC
        AEC --> CleanAudio["Clean 16kHz PCM"] --> GeminiLive
    end

    subgraph EXECUTION ["Execution Fabric & Drivers"]
        ActionBroker --> WindowsNode["🪟 Windows Node: COM UIA + Win32 (execution/windows/)"]
        ActionBroker --> SubstrateBridge["⚡ Substrate Bridge: JSON-RPC IPC (execution/substrate_bridge.py)"]
        ActionBroker --> BrowserNode["🌐 Browser Node: Playwright CDP (execution/browser/)"]
        SubstrateBridge --> NodeRunner["Persistent Node.js CUA Runner (jarvis_substrate_runner.ts)"]
    end
```

---

## 2. Core Architectural Subsystems

### 2.1 The Multimodal Cognitive Core
- **Gemini 3.8 Live API Client (`gemini_live.py`):** Maintains bidirectional WebSockets streaming 16kHz mono PCM audio and JPEG video/screen frames while receiving real-time assistant speech audio chunks and structured tool proposals.
- **Multi-Model Intent Router (`model_router.py`):** Automatically classifies incoming requests and delegates complex programming tasks, deep reasoning, or summarization to specialized models (e.g. Qwen 3.8 27B for code refactoring, GPT-OSS 120B for deep reasoning).

### 2.2 Hardware-Isolated Audio & Echo Cancellation
- **WASAPI Loopback Capture Worker (`audio_aec.py`):** Captures physical speaker output at the Windows hardware layer.
- **Partitioned Block Frequency Domain Adaptive Filter (PBFDAF):** Mathematically models the room acoustic impulse response and subtracts system sounds (YouTube, music, game sound) from the microphone stream.
- **Playback Activity Tracker (`output_tracker.py`):** Monitors physical hardware buffer drain to eliminate barge-in collision while the assistant is speaking.

### 2.3 Governance & The Capability Firewall
- **Invariant:** *The model is never the trust boundary.*
- **Policy Engine & Firewall (`policy/`):** Evaluates every action against canonical capability identifiers (`CAPABILITY_*`).
- **Risk Tiers:** Actions are classified into **Read-Only** (execute immediately), **Low/Medium** (execute with audit trail), and **High-Risk/Destructive** (gated behind explicit user confirmation).

### 2.4 Multi-Provider Desktop Execution Fabric
- **Application Control Engine (`app_control_engine.py`):** Coordinates automation across a deterministic hierarchy:
  1. *Native URI Schemes* (e.g. `spotify:`, `vscode:`)
  2. *Microsoft UI Automation COM* (`UIAutomationCore.dll`) directly invoking controls via Windows accessibility trees.
  3. *Playwright CDP* for web content inside browser windows.
  4. *Substrate Coordinate Fallback* via persistent Node.js runner.

---

## 3. Communication Protocols

| Channel | Transport | Protocol / Format | Purpose |
| :--- | :--- | :--- | :--- |
| **Desktop UI $\leftrightarrow$ Gateway** | WebSocket (`ws://127.0.0.1:8765`) | JSON-RPC Frames (`req`, `res`, `event`) | State synchronization, audio chunks, tool events. |
| **Python $\leftrightarrow$ Substrate Daemon** | OS stdio pipe | JSON-RPC 2.0 (newline-delimited JSON) | Coordinate mouse/keyboard simulation and screen snapshots. |
| **Python $\leftrightarrow$ Gemini Live** | TLS WebSocket | Google GenAI Live Protocol | Real-time audio, text, video, tool calls. |
| **Python $\leftrightarrow$ Telegram** | HTTPS / Long Polling | Telegram Bot API / aiogram | Smartphone remote supervision and approval cards. |
| **Python $\leftrightarrow$ WhatsApp Subprocess** | Process pipe / IPC | Structured JSON stdio | Autonomous VoIP audio bridge and contact sync. |

---

## 4. Next Steps

- Explore the [Control Plane](control-plane.md) for session state and turn execution details.
- Review the [Execution Lifecycle](execution-lifecycle.md) for the end-to-end trace of a user request.
- Consult the [Security Threat Model](../security/threat-model-and-trust.md) for capability firewall rules.
