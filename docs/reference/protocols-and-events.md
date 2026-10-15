# Protocols & Wire Event Specifications

This document defines the exact JSON schemas and wire contracts used by the **JARVIS Gateway WebSocket Protocol** and the **Substrate JSON-RPC IPC Bus**.

---

## 1. Gateway WebSocket Protocol Specifications

All messages exchanged between the Neural Web UI, external nodes, and the Gateway server follow typed JSON schemas defined in [`src/jarvis/gateway/protocol.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/gateway/protocol.py).

### 1.1 Handshake Challenge Event (`connect.challenge`)
Pushed by the server immediately upon opening the TCP WebSocket connection:
```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": {
    "nonce": "c9284fae109d43bf88a092de",
    "ts": 1729000000000
  },
  "seq": null
}
```

### 1.2 Client Connect Request (`connect`)
Sent by the client answering the challenge:
```json
{
  "type": "req",
  "id": "req-001",
  "method": "connect",
  "params": {
    "client_id": "NEURAL-WEB-UI",
    "challenge_response": "c9284fae109d43bf88a092de",
    "session_id": "SESS-MAIN",
    "client_version": "1.0.1"
  }
}
```

### 1.3 Server Connect Response (`hello-ok`)
```json
{
  "type": "res",
  "id": "req-001",
  "ok": true,
  "payload": {
    "status": "hello-ok",
    "session_id": "SESS-MAIN",
    "capabilities": [
      "filesystem.read",
      "window.list",
      "ui.interact",
      "live.audio"
    ]
  },
  "error": null
}
```

### 1.4 Live Synthesized Audio Event (`live.audio`)
Pushes synthesized 24kHz assistant speech frames to the client for Web Audio playback:
```json
{
  "type": "event",
  "event": "live.audio",
  "payload": {
    "pcm_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
    "sample_rate": 24000,
    "channels": 1,
    "mime_type": "audio/pcm"
  },
  "seq": 105
}
```

### 1.5 Tool Execution Proposal & Outcome Events
- **`live.tool_call`**: Broadcasts that an action has started:
  ```json
  {
    "type": "event",
    "event": "live.tool_call",
    "payload": {
      "call_id": "call-104",
      "tool_name": "app_launch",
      "arguments": { "target": "Notepad" }
    }
  }
  ```
- **`live.tool_complete`**: Broadcasts the verified result:
  ```json
  {
    "type": "event",
    "event": "live.tool_complete",
    "payload": {
      "call_id": "call-104",
      "tool_name": "app_launch",
      "success": true,
      "output": { "pid": 14208, "hwnd": "0x002B04E1", "window_title": "Untitled - Notepad" },
      "verification": "VERIFIED"
    }
  }
  ```

### 1.6 Interactive Approval Event (`approval.required`)
Broadcast when an action touches a `HIGH` risk tier:
```json
{
  "type": "event",
  "event": "approval.required",
  "payload": {
    "approval_id": "appr-8109",
    "capability": "filesystem.delete",
    "target": "C:\\Users\\Operator\\Desktop\\old_build.tmp",
    "rationale": "Operator requested cleanup of old build directory",
    "ttl_seconds": 300
  }
}
```

---

## 2. Substrate JSON-RPC 2.0 Stdio Wire Protocol

Exchanged between the Python `SubstrateBridge` and the Node.js runner (`jarvis_substrate_runner.ts`) over standard input/output. Every frame is a single newline-delimited JSON line.

### 2.1 Coordinate Input Request (`computer.action`)
```json
{
  "jsonrpc": "2.0",
  "id": "sub-req-42",
  "method": "computer.action",
  "params": {
    "action": "click",
    "x": 960,
    "y": 540,
    "button": "left"
  }
}
```

### 2.2 Screen Display Snapshot Request (`system.snapshot`)
```json
{
  "jsonrpc": "2.0",
  "id": "sub-req-43",
  "method": "system.snapshot",
  "params": {
    "format": "jpeg",
    "quality": 80
  }
}
```

### 2.3 Success Response
```json
{
  "jsonrpc": "2.0",
  "id": "sub-req-43",
  "result": {
    "success": true,
    "base64": "/9j/4AAQSkZJRgABAQEASABIAAD...",
    "width": 1920,
    "height": 1080
  }
}
```

### 2.4 Error Response
```json
{
  "jsonrpc": "2.0",
  "id": "sub-req-44",
  "error": {
    "code": -32603,
    "message": "Desktop Duplication API failed: Screen is locked or UAC secure desktop active"
  }
}
```
