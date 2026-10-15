"""Windows Execution Body package export for JARVIS."""

from jarvis.execution.windows.desktop import (
    capture_screenshot,
    list_open_windows,
    mouse_click,
    press_key,
    type_text,
)
from jarvis.execution.windows.filesystem import (
    delete_file,
    list_directory,
    read_file,
    write_file,
)
from jarvis.execution.windows.host import WindowsNode, windows_node
from jarvis.execution.windows.process import (
    enumerate_processes,
    inspect_process,
    launch_process,
    terminate_process,
)
from jarvis.execution.windows.shell import run_shell_command
from jarvis.execution.windows.system import (
    get_display_brightness,
    get_system_info,
    get_system_volume,
    set_display_brightness,
    set_system_volume,
)

__all__ = [
    "WindowsNode",
    "capture_screenshot",
    "delete_file",
    "enumerate_processes",
    "get_display_brightness",
    "get_system_info",
    "get_system_volume",
    "inspect_process",
    "launch_process",
    "list_directory",
    "list_open_windows",
    "mouse_click",
    "press_key",
    "read_file",
    "run_shell_command",
    "set_display_brightness",
    "set_system_volume",
    "terminate_process",
    "type_text",
    "windows_node",
    "write_file",
]
