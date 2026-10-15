"""Browser Automation Subsystem for JARVIS."""

from jarvis.execution.browser.host import BrowserNode, browser_node
from jarvis.execution.browser.session import BrowserManager, browser_manager

__all__ = [
    "BrowserManager",
    "BrowserNode",
    "browser_manager",
    "browser_node",
]
