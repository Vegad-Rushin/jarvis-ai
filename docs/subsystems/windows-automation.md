# Windows In-App Automation & UI Control Engine

The **Windows Automation Subsystem** ([`src/jarvis/execution/windows/`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/)) enables deep, deterministic interaction with native Windows desktop applications. Instead of brittle pixel coordinate guessing or screen scraping, JARVIS integrates directly with the **Microsoft UI Automation COM engine** (`UIAutomationCore.dll`) and Win32 APIs.

---

## 1. Multi-Provider Automation Hierarchy

When an action is requested against an application or control, the **Application Control Engine** ([`src/jarvis/core/app_control_engine.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/core/app_control_engine.py)) resolves the most deterministic provider:

```
[Target Action Request]
          │
          ▼
┌─────────────────────────────────┐
│ Tier 1: Native Application URI  │  e.g., Spotify URI, VSCode protocol, deep links
└────────────────┬────────────────┘
                 │ (if unsupported or failed)
                 ▼
┌─────────────────────────────────┐
│ Tier 2: Microsoft COM UIA Tree  │  Direct COM interface: UIAutomationCore.dll
└────────────────┬────────────────┘  Control patterns (Invoke, Value, Toggle)
                 │ (if target is browser web content)
                 ▼
┌─────────────────────────────────┐
│ Tier 3: Playwright DOM Host     │  Direct browser CDP element manipulation
└────────────────┬────────────────┘  CSS selectors, text matching, DOM dispatch
                 │ (if target is non-standard custom control)
                 ▼
┌─────────────────────────────────┐
│ Tier 4: Coordinate CUA Fallback │  Native Substrate / Win32 mouse_event
└─────────────────────────────────┘  Sub-pixel coordinate clicking & typing
```

---

## 2. Core Architectural Subsystems

### 2.1 Dynamic Application Registry (`AppRegistry`)
Eliminates hardcoded paths and static application dictionaries ([`src/jarvis/execution/windows/app_registry.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/app_registry.py)). It dynamically discovers installed host applications by:
1. Scanning Start Menu shortcuts (`.lnk` files across User and Common Start Menu folders).
2. Enumerating registered `AppUserModelId` packages via Windows shell.
3. Reading registered URI protocol handlers from `HKEY_CLASSES_ROOT`.
4. Correlating active processes with verified executable filepaths.

### 2.2 Asynchronous Detached Application Launcher (`AppLauncher`)
Prevents blocking the Python event loop while waiting for GUI processes ([`src/jarvis/execution/windows/app_launcher.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/app_launcher.py)):
- Spawns GUI processes using detached flags:
  ```python
  subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
  ```
- Executes a bounded polling loop (e.g. 5 seconds) verifying:
  1. Has the process ID been created?
  2. Does a visible top-level window exist for that process?
  3. Is the window responsive and ready for operator input?

### 2.3 Win32 Window Manager (`WindowManager`)
Controls application windows via native Win32 HWND handles ([`src/jarvis/execution/windows/window_manager.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/window_manager.py)):
- **Fuzzy Window Matching:** Resolves windows by process name, title substring, or HWND.
- **Clean Foregrounding:** Attaches thread input queues via `AttachThreadInput` to reliably bring background windows to the foreground without flashing taskbar icons.
- **Window Geometry:** `minimize()`, `maximize()`, `restore()`, `close()`, and `move_resize_window()`.

### 2.4 Microsoft COM UI Automation Engine (`WindowsUIAutomation`)
Interacts with the live control hierarchy using COM interfaces ([`src/jarvis/execution/windows/uia.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/execution/windows/uia.py)):

#### Supported Native Control Patterns:
- **`IUIAutomationInvokePattern`:** Clicks buttons, menu items, and links programmatically without moving the physical mouse cursor.
- **`IUIAutomationValuePattern`:** Sets text values inside edit boxes and input fields instantaneously via `SetValue(BSTR)`.
- **`IUIAutomationTogglePattern`:** Toggles checkboxes and radio buttons between checked and unchecked states.
- **`IUIAutomationSelectionItemPattern`:** Selects tabs, dropdown options, and list entries.
- **`IUIAutomationExpandCollapsePattern`:** Expands accordion menus, trees, and comboboxes.
- **`IUIAutomationScrollPattern`:** Programmatically scrolls scrollbars and document panes.

---

## 3. Semantic Target Resolution & Confidence Scoring

When a model requests an action (e.g. `click(target="Save")`), the engine resolves the natural language label against the accessibility tree using a confidence cascade:

$$\text{AutomationId} \longrightarrow \text{Name} \longrightarrow \text{ControlType} \longrightarrow \text{ClassName} \longrightarrow \text{Bounding Box}$$

- **Exact AutomationId Match:** $1.0$ confidence.
- **Exact Name Match:** $0.95$ confidence.
- **Case-Insensitive Substring Match:** $0.85$ confidence.
- **Fuzzy Text Similarity:** $0.60 - 0.80$ confidence.
- **Ambiguity Policy:** If multiple elements match with high confidence, JARVIS does not guess blindly; it prompts the operator for clarification.

---

## 4. Normalized UI Tree Snapshots

Raw accessibility trees can contain tens of thousands of layout containers, borders, and empty canvas panels. The tree normalizer walks the tree and prunes non-interactive nodes, emitting a compact hierarchy for cognitive models:

```text
Window: "Paint" [HWND: 0x001204A2]
├── Tab: "Home" (Selected)
├── Tab: "View"
├── Button: "Paste" (Enabled)
├── Group: "Tools"
│   ├── Button: "Pencil"
│   ├── Button: "Fill with color"
│   └── Button: "Text"
└── Group: "Shapes"
    ├── Button: "Line"
    ├── Button: "Rectangle"
    └── Button: "Ellipse"
```
This representation preserves token budgets while giving models complete structural awareness of active controls.
