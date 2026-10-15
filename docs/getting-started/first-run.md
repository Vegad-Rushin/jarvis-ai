# First Run & Operational Walkthrough

This guide details how to launch, operate, and verify the **JARVIS Personal AI Operating System** on your machine.

---

## 1. Starting JARVIS

JARVIS can be started in two primary operational modes: **Full Desktop Experience** (with dedicated 3D Neural UI and background daemons) or **Terminal Chat Mode**.

### Option A: The Full Desktop Experience (Recommended)

Run the included launch script from the project root:

```powershell
.\run.bat
```

Or execute directly through Python:

```powershell
python -m jarvis.cli chat --live --with-daemon
```

### What Happens During Boot:
1. **Dynamic Port Discovery:** The Gateway checks port `8765` (falling back dynamically if occupied) and starts the WebSocket server (`ws://127.0.0.1:8765`).
2. **UI Web Server Launch:** Serves [`frontend/`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/frontend/) on `http://127.0.0.1:8080` (with fallback discovery).
3. **Application Window Launch:** Launches your default browser in dedicated app window mode pointing to `http://127.0.0.1:8080/index.html`.
4. **Hardware Audio Capture & AEC:** Opens the WASAPI loopback speaker capture stream and primary microphone, initiating the PBFDAF echo filter.
5. **Real-Time Cognitive Connection:** Establishes the low-latency WebSocket stream with the **Gemini 3.8 Live API**.
6. **Background Daemons:** Background tasks for standing intents (heartbeat scheduler) and Telegram remote control (if configured) activate.

---

## 2. Using the Neural 3D Interface

When the interface opens, you will observe:
- **Signal Orb (`signal-orb.js`):** A 12,000-particle Fibonacci sphere displaying the assistant's state:
  - **Amber/Gold:** Listening for your voice.
  - **Purple/Violet:** Thinking and reasoning.
  - **Cyan with Orbiting Rings:** Performing live web search or tool execution.
  - **Mint Green:** Task completed.
- **Speaking Orb (`speaking-orb.js`):** Displays real-time spoken typography synchronized to audio output.
- **Ambient 3D Particle Field (`particle-field.js`):** 5,200 depth-projected particles reacting to mouse parallax, audio amplitude, and state changes.

---

## 3. Basic Voice & Interaction Verification

Try the following initial commands to verify end-to-end operation:

### Voice Verification
1. **Greet JARVIS:** Speak naturally into your microphone: *"Hello JARVIS."*  
   JARVIS will answer in real time using the configured voice persona (default: *Algenib*).
2. **Test Real-Time Barge-In (Interruption):** While JARVIS is speaking, speak over the voice: *"Wait, pause."*  
   The AEC loopback reference filter detects your voice, cuts playback immediately, and transitions to listening with zero transition artifacts.
3. **Multimodal Desktop Perception:** With an application open on screen, say: *"Look at my screen and tell me what window is currently in focus."*  
   JARVIS captures a desktop snapshot, submits it to Gemini Live, and describes your workspace.

### In-App Automation Verification
1. Say: *"Open Notepad and write a reminder to review the project roadmap."*
2. Observe JARVIS:
   - Discovers `Notepad.exe` via `AppRegistry`.
   - Launches detached GUI process via `AppLauncher`.
   - Inspects UI hierarchy via `UIAutomationCore.dll`.
   - Injects the text using `IUIAutomationValuePattern`.
   - Verifies the text appeared via closed-loop post-action observation.

---

## 4. Option B: Lightweight Terminal Chat Mode

If you prefer operating strictly in text mode without audio capture:

```powershell
python -m jarvis.cli chat
```

You can interact using natural language, execute tool commands, and inspect memory records.

To exit a session cleanly:
Type `exit` or `quit`, or press `Ctrl+C`. All daemons, WebSockets, and loopback audio streams will shut down gracefully.
