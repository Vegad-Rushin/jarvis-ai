# External Integrations Overview

JARVIS extends its operating system capabilities across external platforms, messaging protocols, and mobile devices while strictly preserving local trust boundaries.

---

## 1. Integrations Matrix

| Integration | Implementation Domain | Status | Communication Protocol | Authentication / Trust Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **[Telegram Remote Control](telegram.md)** | `src/jarvis/telegram/` | **Production** | Telegram Bot API / Long Polling | Cryptographic one-time nonce pairing (`/start pair_<token>`). Fail-closed. |
| **[WhatsApp Autonomous Telephony](whatsapp.md)** | `substrate/extensions/whatsapp` & `src/jarvis/execution/whatsapp/` | **Production** | WebRTC VoIP + Gemini 3.8 Live | Multi-file WASM session auth + exclusive single-instance lock file. |
| **[Windows Native Automation](../subsystems/windows-automation.md)** | `src/jarvis/execution/windows/` | **Production** | Microsoft COM (`UIAutomationCore.dll`) + Win32 | OS User Token / Local process boundary. |
| **[Browser Web Automation](../subsystems/browser-automation.md)** | `src/jarvis/execution/browser/` | **Production** | Chrome DevTools Protocol (CDP) / Playwright | Sandboxed browser contexts with isolated cookies. |
| **[Real-Time Web Search](../subsystems/action-broker-and-policy.md)** | `src/jarvis/cognition/web_search.py` | **Production** | HTTPS DuckDuckGo HTML parser | Anonymous outbound HTTP GET requests. Zero tracking. |

---

## 2. Shared Integration Security Principles

1. **Fail-Closed by Default:** If an external integration is enabled but unauthenticated, all incoming requests are rejected.
2. **Dedicated Cognitive Threads:** Remote channels (e.g. Telegram) operate their own dedicated conversation context threads. Remote interactions do not overwrite or desynchronize active desktop voice sessions.
3. **No Unrestricted Execution:** Actions proposed remotely through Telegram or WhatsApp must pass through the identical Capability Firewall and Policy Engine enforced on the local PC.
