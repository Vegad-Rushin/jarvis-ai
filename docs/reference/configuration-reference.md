# Configuration Reference

This reference documents every parameter defined in `JarvisSettings` ([`src/jarvis/config.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/config.py)), including environment variable bindings, types, default values, and consuming components.

---

## 1. Identity & Persona

| Setting / Env Variable | Type | Default | Consuming Component | Description |
| :--- | :--- | :--- | :--- | :--- |
| `APP_NAME` | `str` | `"JARVIS"` | UI, CLI, Gateway | Display identifier of the system. |
| `APP_VERSION` | `str` | `"1.0.1"` | Gateway, CLI, UI | Semantic version of the operating system. |
| `ENVIRONMENT` | `str` | `"production"` | Logging, Diagnostics | Runtime environment (`production`, `development`, `test`). |
| `USER_CALLSIGN` | `str` | `"Sir"` | Voice, CLI, Telegram | Spoken and textual honorific used by the assistant. |
| `VOICE_DEFAULT_NAME` | `str` | `"Algenib"` | Gemini Live, Voice | Voice persona name for speech synthesis (`Algenib`, `Puck`, `Charon`, `Kore`, `Fenrir`). |

---

## 2. API Credentials & Authentication

| Setting / Env Variable | Type | Default | Consuming Component | Description |
| :--- | :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | `Optional[str]` | `None` | `GeminiLiveClient`, `GoogleGenAIProvider` | Primary API key for Gemini 3.8 Live API WebSockets and vision. |
| `GROQ_API_KEY` | `Optional[str]` | `None` | `GroqProvider`, `ModelRouter` | API key for high-speed specialist models (`GPT-OSS 120B`, `Qwen 3.8 27B`). |
| `TELEGRAM_BOT_TOKEN` | `Optional[str]` | `None` | `TelegramService` | Bot token acquired from `@BotFather` for mobile remote control. |

---

## 3. Dynamic Audio Pipeline & Hardware AEC

| Setting / Env Variable | Type | Default | Consuming Component | Description |
| :--- | :--- | :--- | :--- | :--- |
| `AUDIO_INPUT_DEVICE_INDEX` | `Optional[int]` | `None` | `MicrophoneCapture` | Target audio capture device index. When `None`, resolves default WASAPI mic. |
| `AUDIO_INPUT_SAMPLE_RATE` | `int` | `16000` | Voice Pipeline, AEC | Sampling frequency (Hz) for microphone capture and model streaming. |
| `AUDIO_INPUT_CHANNELS` | `int` | `1` | `MicrophoneCapture` | Input channel count (mono PCM). |
| `AUDIO_INPUT_CHUNK_MS` | `int` | `30` | `MicrophoneCapture` | Audio frame slice duration (ms) per captured packet. |
| `AUDIO_OUTPUT_SAMPLE_RATE` | `int` | `24000` | `PcmStreamPlayer` | Sampling frequency (Hz) for synthesized assistant audio. |
| `AUDIO_VAD_ENERGY_THRESHOLD` | `float` | `15.0` | `AudioInputGate` | RMS voice activity detection threshold for opening the audio gate. |
| `AUDIO_DUPLEX_SUPPRESSION` | `bool` | `True` | `AudioInputGate` | Suppresses microphone energy during active vocal playback. |
| `VOICE_DRAIN_HOLD_MS` | `int` | `250` | `PlaybackActivityTracker` | Post-synthesis buffer drain hold (ms) preventing trailing echo feedback. |
| `AUDIO_AEC_ENABLED` | `bool` | `True` | `AudioEchoCanceller` | Enables WASAPI loopback acoustic echo cancellation. |
| `AUDIO_AEC_PARTITIONS` | `int` | `6` | `PartitionedBlockAEC` | Number of frequency-domain filter partitions ($P$). |
| `AUDIO_AEC_STEP_SIZE` | `float` | `0.25` | `PartitionedBlockAEC` | Normalized LMS adaptive filter convergence step size ($\mu$). |
| `AUDIO_AEC_SUPPRESSION_DB` | `float` | `30.0` | `PartitionedBlockAEC` | Maximum spectral suppression depth (dB) for coherent speaker echo. |
| `AUDIO_AEC_DELAY_MAX_MS` | `int` | `250` | `PartitionedBlockAEC` | Maximum buffer delay compensation window (ms) for speaker playback. |

---

## 4. Gateway Daemon & Neural Web Interface

| Setting / Env Variable | Type | Default | Consuming Component | Description |
| :--- | :--- | :--- | :--- | :--- |
| `GATEWAY_HOST` | `str` | `"127.0.0.1"` | `GatewayServer` | IP address for WebSocket daemon binding. |
| `GATEWAY_PORT` | `int` | `8765` | `GatewayServer` | Default TCP port for WebSocket server. |
| `GATEWAY_PORT_AUTO_DISCOVERY`| `bool` | `True` | `GatewayServer` | Scans incremental ports if `GATEWAY_PORT` is occupied. |
| `GATEWAY_PORT_SEARCH_LIMIT` | `int` | `50` | `GatewayServer` | Maximum sequential ports to check before raising error. |
| `UI_HOST` | `str` | `"127.0.0.1"` | `JarvisWebServer` | Bind host for local Neural Web UI HTTP server. |
| `UI_PORT` | `int` | `8080` | `JarvisWebServer` | HTTP port for serving `frontend/` assets. |
| `UI_PORT_AUTO_DISCOVERY` | `bool` | `True` | `JarvisWebServer` | Scans incremental ports if `UI_PORT` is occupied. |
| `UI_AUTO_OPEN_BROWSER` | `bool` | `True` | `JarvisWebServer` | Automatically opens browser window pointing to UI on startup. |

---

## 5. Security & Policy Controls

| Setting / Env Variable | Type | Default | Consuming Component | Description |
| :--- | :--- | :--- | :--- | :--- |
| `REQUIRE_APPROVALS` | `bool` | `True` | `PolicyEngine`, `ApprovalManager` | Requires explicit operator approval for high-risk actions. |
| `DEFAULT_TIMEOUT_SECONDS` | `float` | `60.0` | `ActionBroker`, `ControlPlane` | Maximum execution budget (seconds) per tool action or model turn. |
| `MAX_SUBAGENT_DEPTH` | `int` | `3` | `AgentDelegator` | Maximum recursion depth for delegated subagent swarms. |

---

## 6. Model Allowlist & Dynamic Mappings

| Setting / Env Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `MODEL_MAP_GEMINI_LIVE` | `str` | `"gemini-3.8-live"` | Model endpoint for Gemini Live WebSocket session. |
| `MODEL_MAP_GPT_OSS_120B` | `str` | `"openai/gpt-oss-120b"` | Model endpoint for deep logical reasoning. |
| `MODEL_MAP_QWEN_3_8_27B` | `str` | `"qwen/qwen3.8-27b"` | Model endpoint for code generation and refactoring. |
| `MODEL_MAP_GEMINI_3_5_FLASH_LITE`| `str`| `"gemini-3.5-flash-lite"` | Model endpoint for conversation compaction. |
| `MODEL_MAP_GEMINI_3_1_FLASH_LITE`| `str`| `"gemini-3.1-flash-lite"` | Model endpoint for fast extraction. |
| `MODEL_MAP_GEMMA_4_31B` | `str` | `"gemini-2.5-flash"` | Model endpoint for edge / low-power reasoning. |
