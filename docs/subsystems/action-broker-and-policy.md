# Action Broker, Capability Firewall & Policy Engine

The **Action Broker** ([`src/jarvis/actions/broker.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/actions/broker.py)) and **Policy Engine** ([`src/jarvis/policy/engine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/engine.py)) govern how cognitive models interact with the physical operating system. They enforce the architectural invariant: **The model is never the trust boundary.**

---

## 1. Architectural Architecture & Boundary Flow

```mermaid
flowchart TD
    ModelProposal["Model Tool Proposal: name + arguments"] --> Broker["🛡️ Action Broker (actions/broker.py)"]
    Broker --> RegistryCheck{"Tool in Registry?"}
    RegistryCheck -->|No| RejectUnregistered["❌ Error: Unknown capability"]
    
    RegistryCheck -->|Yes| Sanitizer["🧹 Parameter Sanitizer: Path Traversal & Shell Injection Checks"]
    Sanitizer --> SafeParams{"Parameters Clean?"}
    SafeParams -->|No| RejectSanitization["❌ Blocked: Malformed or dangerous parameter"]
    
    SafeParams -->|Yes| Firewall["🧱 Capability Firewall (policy/firewall.py)"]
    Firewall --> RiskClassification{"Risk Tier Assignment"}
    
    RiskClassification -->|READ_ONLY / LOW| ExecDriver["🚀 Dispatch to Execution Driver"]
    RiskClassification -->|MEDIUM / HIGH| ApprovalCheck{"Approval Policy (REQUIRE_APPROVALS)"}
    
    ApprovalCheck -->|Bypassed in Live Voice| ExecDriver
    ApprovalCheck -->|Active (Default)| DispatchApproval["🔐 Dispatch Approval Request to UI / Telegram"]
    
    DispatchApproval --> OperatorDecision{"Operator Action"}
    OperatorDecision -->|Approved| ExecDriver
    OperatorDecision -->|Rejected / Timed Out| AbortAction["❌ Execution Cancelled by Policy"]
```

---

## 2. The Capability Firewall

Every tool or action executable in JARVIS is mapped to a canonical capability string ([`src/jarvis/policy/firewall.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/firewall.py)):

### Canonical Capabilities & Risk Tiers:
| Capability Constant | Identifier | Risk Tier | Description |
| :--- | :--- | :--- | :--- |
| `CAPABILITY_FILESYSTEM_READ` | `filesystem.read` | **`READ_ONLY`** | Reads file contents or configuration files. |
| `CAPABILITY_FILESYSTEM_LIST` | `filesystem.list` | **`READ_ONLY`** | Enumerates directory entries. |
| `CAPABILITY_WINDOW_LIST` | `window.list` | **`READ_ONLY`** | Queries active desktop application windows. |
| `CAPABILITY_UI_INSPECT` | `ui.inspect` | **`READ_ONLY`** | Walks the COM accessibility control tree. |
| `CAPABILITY_COMPUTER_SCREENSHOT` | `computer.screenshot` | **`READ_ONLY`** | Captures display pixels or active window image. |
| `CAPABILITY_SYSTEM_VOLUME` | `system.volume` | **`LOW`** | Modifies soundcard master volume. |
| `CAPABILITY_WINDOW_FOCUS` | `window.focus` | **`LOW`** | Brings a window to foreground. |
| `CAPABILITY_FILESYSTEM_WRITE` | `filesystem.write` | **`MEDIUM`** | Creates or modifies file contents. |
| `CAPABILITY_APP_LAUNCH` | `app.launch` | **`MEDIUM`** | Spawns a desktop application process. |
| `CAPABILITY_UI_INTERACT` | `ui.interact` | **`MEDIUM`** | Invokes a button or types text into a UI control. |
| `CAPABILITY_FILESYSTEM_DELETE` | `filesystem.delete` | **`HIGH`** | Deletes a file or directory. Gated by user approval. |
| `CAPABILITY_PROCESS_TERMINATE` | `process.terminate` | **`HIGH`** | Kills an active OS process. Gated by user approval. |
| `CAPABILITY_SHELL_EXECUTE` | `shell.execute` | **`HIGH`** | Executes an arbitrary PowerShell command. Gated. |

---

## 3. Parameter Sanitization & Injection Defense

Before passing arguments to execution drivers, the Action Broker enforces strict sanitization:
1. **Path Traversal Protection:** Validates that target paths do not contain relative traversal sequences (`../`, `..\`) or target root system directories (`C:\Windows\System32`, `C:\Recovery`).
2. **Dangerous Shell Patterns:** Scans shell commands using `is_dangerous_command()` to detect destructive operations (`Remove-Item -Recurse`, `Format-Volume`, `rmdir /s /q`, broad wildcard deletions).

---

## 4. Human Approval Workflow

When a `HIGH` risk action is proposed and `settings.REQUIRE_APPROVALS` is active:
1. The **Approval Manager** ([`src/jarvis/policy/approvals.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/policy/approvals.py)) generates a cryptographically random challenge token and stores the pending action with a 300-second TTL.
2. An interactive approval prompt is emitted:
   - On the **Web UI**, an approval modal displays the exact command, target path, and risk rationale.
   - If paired with **Telegram**, an inline interactive card with `[✅ Approve]` and `[❌ Reject]` buttons is pushed to the operator's smartphone.
3. The model execution thread halts until the user approves or the challenge times out.
