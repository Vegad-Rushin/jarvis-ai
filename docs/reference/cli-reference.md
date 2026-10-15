# Command Line Interface (CLI) Reference

The JARVIS Command Line Interface ([`src/jarvis/cli/`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/cli/)) provides direct access to all operating system capabilities, interactive dialogue sessions, system diagnostics, and background daemons.

---

## 1. Global Syntax & Entrypoints

JARVIS can be invoked through the installed script entrypoint or directly via Python module:

```powershell
# Using installed script
jarvis [SUBCOMMAND] [OPTIONS]

# Using Python module
python -m jarvis.cli [SUBCOMMAND] [OPTIONS]
```

---

## 2. Interactive Dialogue & Voice

### `jarvis chat`
Starts an interactive conversational session with JARVIS.

```powershell
jarvis chat [OPTIONS]
```

#### Options:
- `--live`: Enables real-time Gemini 3.8 Live API WebSocket mode with full-duplex audio streaming.
- `--with-daemon`: Launches background daemons (Gateway WebSocket, UI HTTP server, and Standing Intent heartbeat scheduler) alongside the chat session.
- `--with-ui`: Opens the dedicated 3D Neural Web interface in your default browser.
- `--voice <NAME>`: Overrides the synthesized voice persona (e.g. `Algenib`, `Puck`, `Charon`, `Kore`, `Fenrir`).
- `--session-id <ID>`: Resumes a specific persistent session ID.
- `--message <TEXT>`: Executes a one-shot query from the command line and exits.

#### Examples:
```powershell
# Boot the complete system with 3D UI, daemons, and live voice
jarvis chat --live --with-daemon --with-ui

# Run a one-shot query in console
jarvis chat --message "What windows are currently open on my desktop?"
```

---

## 3. System Health & Diagnostics

### `jarvis health` / `jarvis status`
Inspects host operating system health, registered execution nodes, and hardware audio streams.

```powershell
jarvis health
```

#### Output Fields:
- **OS Architecture:** Windows version, build number, 64-bit architecture.
- **Audio Capture:** Active WASAPI microphone name, sampling rate, channels, loopback capture state.
- **Cognitive Models:** API key presence and provider connectivity.
- **Execution Drivers:** COM UIA status, Playwright browser status, Substrate daemon state.
- **Database:** SQLite WAL file size, turn count, memory count.

---

## 4. Windows Application & Desktop Automation

### `jarvis app <SUBCOMMAND>`
Directly controls native Windows applications through the Application Control Engine.

```powershell
# Launch an application asynchronously with window readiness verification
jarvis app launch "Notepad"

# Bring a window to foreground using thread-input attachment
jarvis app focus "Spotify"

# Enumerate all open top-level application windows with HWNDs and titles
jarvis app windows

# Inspect the Microsoft UI Automation accessibility tree for a window
jarvis app inspect --target "Calculator" --depth 4

# Programmatically click a button or set input text via COM control patterns
jarvis app interact --target "Save" --action "click" --window "Notepad"

# Close an application window cleanly
jarvis app close "Calculator"
```

---

## 5. Mobile Telegram Remote Control

### `jarvis telegram <SUBCOMMAND>`
Manages the native Telegram smartphone supervision daemon.

```powershell
# Generate a cryptographic one-time pairing challenge & deep link
jarvis telegram pair [--ttl 300] [--no-wait]

# Display pairing status and authorized operator ID
jarvis telegram status

# Revoke paired device authorization
jarvis telegram unpair

# Run the Telegram long-polling daemon standalone
jarvis telegram daemon
```

---

## 6. Autonomous WhatsApp Telephony & Messaging

### `jarvis whatsapp <SUBCOMMAND>`
Controls the outbound VoIP calling bridge and message store.

```powershell
# Initiate an autonomous goal-oriented voice call
jarvis whatsapp call --target "+1234567890" --objective "Confirm meeting time"

# Display session lock status and WebRTC connection health
jarvis whatsapp status

# Inspect call history logs and transcripts
jarvis whatsapp history [--limit 10]

# Display terminal QR code for one-time WhatsApp Web pairing
jarvis whatsapp login

# Terminate active session and release session lock
jarvis whatsapp logout

# Synchronize contacts and recent chat messages to local database
jarvis whatsapp sync [--full]

# Search contacts by name, alias, or phone number
jarvis whatsapp contacts search --query "John"

# Review unread messages with dialogue context
jarvis whatsapp unread [--limit 15]

# Send a direct text message
jarvis whatsapp send --recipient "Alice" --text "On my way"
```

---

## 7. Daemons & Standalone Services

### `jarvis gateway`
Runs the asynchronous WebSocket server standalone:
```powershell
jarvis gateway [--host 127.0.0.1] [--port 8765]
```

### `jarvis serve` / `jarvis ui`
Serves the `frontend/` Web UI static assets:
```powershell
jarvis serve [--host 127.0.0.1] [--port 8080] [--no-browser]
```

### `jarvis cron`
Runs the background standing intent pulse evaluator:
```powershell
jarvis cron [--interval 10]
```
