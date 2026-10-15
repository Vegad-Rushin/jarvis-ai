# Installation & System Requirements

This document provides a verified, step-by-step installation guide for setting up the **JARVIS Personal AI Operating System** on Windows.

---

## 1. System Requirements & Prerequisites

JARVIS is engineered for direct integration with the Windows operating system and requires the following hardware and software prerequisites:

| Requirement | Minimum Specification | Recommended Specification | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10 (64-bit, 20H2+) | Windows 11 (64-bit, 22H2+) | Required for Microsoft UI Automation COM (`UIAutomationCore.dll`) and WASAPI loopback capture. |
| **Python** | Python 3.10.x | Python 3.10.x - 3.12.x | Python 64-bit required. Ensure `python` and `pip` are on system PATH. |
| **Node.js** | Node.js 18.x LTS | Node.js 20.x or 22.x LTS | Required for the Execution Substrate daemon and WhatsApp VoIP WebRTC audio bridge. |
| **Audio Hardware** | Standard physical microphone & stereo speakers | Headset or desktop microphone + speakers | Physical speaker playback is required for WASAPI loopback reference capture. |
| **Web Browser** | Google Chrome or Microsoft Edge | Google Chrome / Microsoft Edge (latest) | Used for rendering the dedicated Neural 3D Web UI and Playwright browser automation. |
| **Git** | Git 2.35+ | Git (latest) | Required for version control and submodule resolution. |

---

## 2. Environment Setup Steps

### Step 1: Clone the Repository
Clone `deepakrakshit/jarvis-ai` using PowerShell or Windows Terminal:

```powershell
git clone https://github.com/deepakrakshit/jarvis-ai.git
cd jarvis-ai
```

### Step 2: Create and Activate Python Virtual Environment
Always install JARVIS in an isolated virtual environment to prevent package collisions:

```powershell
# Create virtual environment in .venv
python -m venv .venv

# Activate the virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1
```

> [!NOTE]
> If script execution is restricted on Windows, allow current-user execution via:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 3: Upgrade Pip & Install JARVIS in Editable Mode
Install JARVIS with all core dependencies and development tools (`[dev]` extra):

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

This installs core runtime libraries (`google-genai`, `groq`, `langgraph`, `fastapi`, `uvicorn`, `websockets`, `pywin32`, `pycaw`, `pyautogui`, `sounddevice`, `numpy`, `scipy`, `aiogram`, `playwright`, `rich`) and quality gate tools (`pytest`, `pytest-asyncio`, `ruff`, `mypy`).

### Step 4: Install Optional Substrate Extension Dependencies (WhatsApp VoIP)
If utilizing autonomous WhatsApp voice telephony or the Baileys WebRTC bridge:

```powershell
cd substrate\extensions\whatsapp
npm install
npm run build
cd ..\..\..
```

### Step 5: Install Playwright Browser Binaries
If browser automation via Playwright is required:

```powershell
python -m playwright install chromium
```

---

## 3. Verifying Installation

Verify that all CLI commands, dynamic paths, and execution nodes are properly recognized:

```powershell
# Verify system diagnostics and registered nodes
python -m jarvis.cli health
```

Expected output:
- Python environment: Active virtual environment.
- OS Architecture: `Windows (x64)`.
- Core Modules: `jarvis.core.control_plane`, `jarvis.voice.audio_aec`, `jarvis.gateway.server`.
- Audio Devices: Primary microphone and default audio output device detected.

Next, proceed to [Configuration](configuration.md) to set up your API keys and environment variables.
