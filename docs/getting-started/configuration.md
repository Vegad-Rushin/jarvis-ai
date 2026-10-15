# Configuration & Environment Guide

JARVIS enforces a fundamental architectural invariant: **Never hardcode configurations, credentials, API endpoints, fixed filesystem paths, timeouts, or policy values.** Everything is discoverable, parameterized, and loaded through dynamic configuration schemas.

---

## 1. Configuration Precedence & Resolution

Configuration is managed by the `JarvisSettings` model ([`src/jarvis/config.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/config.py)) using `pydantic-settings`. Values resolve dynamically in the following order of precedence (highest to lowest):

```
1. Explicit CLI arguments (e.g. --port 8765, --live)
2. Operating System Environment Variables (e.g. $env:GEMINI_API_KEY)
3. Local .env file in the workspace root (<root>/.env)
4. Subsystem .env file (<root>/jarvis/.env)
5. Default schema values defined in JarvisSettings
```

---

## 2. Quick Setup: Creating Your `.env` File

Copy the template from `.env.example` to create your local `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` in your text editor and configure your primary keys:

```ini
# =====================================================================
# PRIMARY COGNITIVE CORE (REQUIRED FOR VOICE, VISION & MULTIMODAL)
# =====================================================================
GEMINI_API_KEY="your-gemini-api-key-here"

# =====================================================================
# SPECIALIST MODELS & FALLBACK (OPTIONAL: CODING & REASONING)
# =====================================================================
GROQ_API_KEY="your-groq-api-key-here"

# =====================================================================
# REMOTE CONTROL & MOBILE INTEGRATION (OPTIONAL)
# =====================================================================
TELEGRAM_BOT_TOKEN="your-telegram-bot-token-here"
```

> [!CAUTION]
> **Data Safety & Privacy Invariant:** Never commit `.env` or credentials into version control. Ensure `.env` remains strictly ignored in `.gitignore`.

---

## 3. Core Configuration Categories

### 3.1 Cognitive & Multimodal Model Keys
- **`GEMINI_API_KEY`** (`str`, optional but required for live audio/vision): Authentication key for Google Gemini 3.8 Live API WebSockets and Gemini 3.5 Flash-Lite models.
- **`GROQ_API_KEY`** (`str`, optional): High-speed inference key for specialist models: `GPT-OSS 120B` (deep reasoning) and `Qwen 3.8 27B` (coding & refactoring).
- **`USER_CALLSIGN`** (`str`, default `"Sir"`): The personalized honorific used by the assistant in spoken audio and console prompts. Can be dynamically updated during runtime.

### 3.2 Dynamic Audio Pipeline & Hardware AEC
- **`AUDIO_INPUT_DEVICE_INDEX`** (`int`, default `None`): Index of physical capture device. When `None`, JARVIS dynamically auto-discovers the default Windows WASAPI microphone.
- **`AUDIO_INPUT_SAMPLE_RATE`** (`int`, default `16000`): 16kHz mono PCM required by Gemini Live.
- **`AUDIO_OUTPUT_SAMPLE_RATE`** (`int`, default `24000`): 24kHz synthesized audio output from Gemini Live.
- **`AUDIO_AEC_ENABLED`** (`bool`, default `True`): Activates real-time Partitioned Block Frequency Domain Adaptive Filtering (PBFDAF) against the Windows WASAPI loopback speaker reference.
- **`AUDIO_AEC_SUPPRESSION_DB`** (`float`, default `30.0`): Magnitude Squared Coherence (MSC) spectral suppression threshold in decibels.
- **`VOICE_DRAIN_HOLD_MS`** (`int`, default `250`): Buffer drain hold interval to prevent assistant self-interruption right after finishing vocal speech.

### 3.3 Gateway Daemon & Web Interface Ports
- **`GATEWAY_HOST`** (`str`, default `"127.0.0.1"`): WebSocket bind host.
- **`GATEWAY_PORT`** (`int`, default `8765`): WebSocket server port.
- **`GATEWAY_PORT_AUTO_DISCOVERY`** (`bool`, default `True`): When enabled, if port 8765 is occupied, JARVIS scans incremental ports up to `GATEWAY_PORT_SEARCH_LIMIT` (50).
- **`UI_HOST`** (`str`, default `"127.0.0.1"`): Local HTTP server host for the Neural Web interface.
- **`UI_PORT`** (`int`, default `8080`): Neural Web interface port.
- **`UI_AUTO_OPEN_BROWSER`** (`bool`, default `True`): Automatically launches the default web browser in app window mode upon boot.

### 3.4 Security & Capability Approvals
- **`REQUIRE_APPROVALS`** (`bool`, default `True`): When `True`, destructive operations (file deletion, process termination, shell script execution) require explicit user confirmation.
- **`DEFAULT_TIMEOUT_SECONDS`** (`float`, default `60.0`): Maximum execution budget for tool invocations and subagent delegations.

### 3.5 External Integrations
- **`TELEGRAM_BOT_ENABLED`** (`bool`, default `True`): Enables the native Telegram remote control daemon.
- **`WHATSAPP_VOIP_ENABLED`** (`bool`, default `True`): Enables outbound autonomous WhatsApp VoIP audio calling.

For the exhaustive list of all 60+ parameters, types, and defaults, refer to the [Configuration Reference](../reference/configuration-reference.md).
