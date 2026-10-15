# JARVIS Troubleshooting Guide

This guide provides practical diagnostic procedures and solutions for common operational issues encountered across JARVIS subsystems.

---

## 1. Quick Diagnostic Checklist

When encountering unexpected behavior, run through these diagnostic steps:

1. **Verify Environment & Configuration**:
   ```bash
   uv run jarvis doctor
   ```
2. **Inspect Structured Logs**:
   - Check standard output or log files in `logs/jarvis.log` for `ERROR` or `CRITICAL` entries.
3. **Check Port Availability**:
   ```powershell
   # Windows PowerShell: check if Gateway port 8765 or Web port 8080 are occupied
   Get-NetTCPConnection -LocalPort 8765,8080 -ErrorAction SilentlyContinue
   ```
4. **Test Subsystem Health**:
   ```bash
   curl http://localhost:8080/health
   ```

---

## 2. Voice and Audio Subsystem Issues

### 2.1. Microphone Input is Silent
- **Symptom**: The Signal Orb remains in `IDLE` state and never transitions to `LISTENING` when speaking.
- **Probable Causes**:
  1. Windows microphone privacy permissions are blocking Python or terminal apps.
  2. Incorrect audio input device selected.
- **Resolution**:
  - Open **Windows Settings > Privacy & security > Microphone** and ensure "Let apps access your microphone" and "Let desktop apps access your microphone" are set to **On**.
  - List available audio devices:
    ```bash
    uv run jarvis audio devices
    ```
  - Explicitly set your microphone device in `.env`:
    ```env
    JARVIS_VOICE_DEVICE_INDEX=1
    ```

### 2.2. Echo Loop: JARVIS Hears Its Own Speech
- **Symptom**: During or immediately after speaking, JARVIS interprets its own output as user input and replies to itself.
- **Probable Causes**:
  1. WASAPI loopback capture is inactive, preventing the AEC filter from receiving the reference playback stream.
  2. Output speaker volume is high, causing acoustic clipping in the microphone capsule.
  3. AEC filter learning rate is set too low for room reverberation.
- **Resolution**:
  - Verify loopback capture is active in logs: `AudioAEC: WASAPI loopback capture running on default output`.
  - Lower physical speaker output volume to eliminate analog clipping.
  - In `.env`, increase AEC filter step size or adjust double-talk sensitivity:
    ```env
    JARVIS_AEC_STEP_SIZE=0.15
    JARVIS_AEC_DTD_THRESHOLD=0.45
    ```

### 2.3. Barge-In Triggers Prematurely on Background Noise
- **Symptom**: JARVIS stops speaking mid-sentence when a door closes, keyboard clatters, or air conditioner runs.
- **Probable Causes**:
  - Energy-based Voice Activity Detection (VAD) threshold is too sensitive.
- **Resolution**:
  - Increase the minimum RMS energy threshold in `.env`:
    ```env
    JARVIS_VAD_THRESHOLD=0.045
    JARVIS_VAD_SILENCE_MS=800
    ```

---

## 3. Gateway and WebSocket Connectivity

### 3.1. Browser Shows "Disconnected from Gateway"
- **Symptom**: Web client UI displays a red disconnected status badge; Signal Orb does not respond to clicks.
- **Probable Causes**:
  - Python Gateway server is not running or crashed.
  - WebSocket port `8765` is blocked by firewall or used by another application.
- **Resolution**:
  - Start or restart the gateway:
    ```bash
    uv run jarvis gateway
    ```
  - Check if port `8765` is bound:
    ```powershell
    netstat -ano | findstr :8765
    ```
  - Ensure browser client `frontend/js/config.js` points to `ws://localhost:8765`.

### 3.2. Handshake Protocol Violation
- **Symptom**: Gateway logs report `Invalid frame format: Expected RequestFrame`.
- **Probable Causes**:
  - Outdated client JavaScript caching in browser.
- **Resolution**:
  - Hard refresh the browser (`Ctrl + Shift + R` or `Cmd + Shift + R`) to clear cached JS scripts.

---

## 4. Execution Substrate (Node.js) Bridge Issues

### 4.1. "Substrate executable not found: node"
- **Symptom**: Startup log reports `SubstrateBridge: Failed to spawn Node.js runner`.
- **Probable Causes**:
  - Node.js is not installed or not present in system `PATH`.
- **Resolution**:
  - Verify Node.js version in terminal:
    ```bash
    node -v
    ```
  - Node.js version 18.0.0 or higher is required. Add Node to system `PATH` or define `JARVIS_NODE_PATH` in `.env`.

### 4.2. "Cannot find module" in Substrate Runner
- **Symptom**: Substrate runner exits immediately with exit code `1`.
- **Probable Causes**:
  - Node dependencies have not been installed.
- **Resolution**:
  - Navigate to the repository root and install npm dependencies:
    ```bash
    npm install
    ```

---

## 5. Cognition and Model Routing Issues

### 5.1. Rate Limit or Quota Exceeded
- **Symptom**: Model router logs report `QuotaExceededError (HTTP 429)` from Google GenAI or Groq.
- **Probable Causes**:
  - Daily or per-minute token quota exceeded on the active API tier.
- **Resolution**:
  - JARVIS automatically falls back through configured candidate models:
    `gemini-3.5-flash-lite` -> `gemini-3.1-flash-lite` -> `llama-3.3-70b-versatile` (Groq).
  - Verify that fallback API keys (`GROQ_API_KEY`) are present in `.env`.
  - Check current quota usage in logs or restart quota interval:
    ```bash
    uv run jarvis quota status
    ```

### 5.2. Tool Call Syntax Hallucinations
- **Symptom**: Model generates malformed JSON arguments for tool calls.
- **Probable Causes**:
  - Lower-tier model generating invalid tool call formats under high context loads.
- **Resolution**:
  - JARVIS features an automated tool call repair pass that re-parses and sanitizes markdown-escaped JSON.
  - If errors persist, elevate the primary model tier in `.env`:
    ```env
    JARVIS_PRIMARY_MODEL="gemini-3.5-flash-lite"
    ```

---

## 6. SQLite Storage and Database Locking

### 6.1. "database is locked" (OperationalError)
- **Symptom**: Python raises `sqlite3.OperationalError: database is locked`.
- **Probable Causes**:
  - Multiple concurrent processes attempting writes without WAL mode enabled, or an uncommitted long transaction.
- **Resolution**:
  - Ensure Write-Ahead Logging is active:
    ```sql
    PRAGMA journal_mode = WAL;
    PRAGMA busy_timeout = 5000;
    ```
  - Check for lingering duplicate JARVIS processes:
    ```powershell
    Get-Process -Name python,node | Where-Object { $_.MainWindowTitle -match "jarvis" }
    ```
  - Run WAL checkpoint and vacuum:
    ```bash
    uv run jarvis db optimize
    ```

---

## 7. Telegram and WhatsApp Remote Integration

### 7.1. Telegram Bot Does Not Respond
- **Symptom**: Bot receives messages in Telegram chat but produces no reply.
- **Probable Causes**:
  - User ID not authorized.
  - Ephemeral pairing code has expired.
- **Resolution**:
  - Check terminal output for incoming pairing requests.
  - Send the 6-digit challenge code displayed in the JARVIS desktop terminal to the bot.
  - Add your Telegram user ID directly to `TELEGRAM_ALLOWED_USERS` in `.env`.

### 7.2. WhatsApp Baileys Socket Disconnects Frequently
- **Symptom**: WhatsApp integration drops connection with `ConnectionClosed: 428 Precondition Required`.
- **Probable Causes**:
  - Stale auth session credentials or corrupted pre-keys.
- **Resolution**:
  - Clear the local session cache and scan a fresh QR code:
    ```powershell
    Remove-Item -Recurse -Force substrate\extensions\whatsapp\auth\*
    uv run jarvis whatsapp pair
    ```

---

## 8. Windows UI Automation Issues

### 8.1. "Element not found" or "UIA invocation timeout"
- **Symptom**: Window manager fails to click buttons or focus third-party applications.
- **Probable Causes**:
  - The target application is running as Administrator while JARVIS is running as a non-elevated user.
  - The window is minimized or covered by a modal dialog.
- **Resolution**:
  - If controlling elevated administrative software, start JARVIS in an elevated PowerShell session ("Run as administrator").
  - Use `AppLauncher` to ensure the window is un-minimized and brought to foreground before sending UI Automation control patterns.
