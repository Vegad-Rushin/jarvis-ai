"""Computer-Use Execution and Action Contract Subsystem.

Adapts native CUA contracts for coordinate, mouse, keyboard, and visual automation.
"""

from jarvis.execution.computer.contract import (
    ActionResultEffect,
    ComputerActionName,
    ComputerActParams,
    ComputerActResult,
    ComputerBounds,
    ComputerObservation,
    DeliveryMode,
    ScrollDirection,
)

__all__ = [
    "ActionResultEffect",
    "ComputerActParams",
    "ComputerActResult",
    "ComputerActionName",
    "ComputerBounds",
    "ComputerObservation",
    "DeliveryMode",
    "ScrollDirection",
]
