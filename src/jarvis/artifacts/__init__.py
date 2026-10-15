"""JARVIS First-Class Artifacts & Sidecar Subsystem.

Implements Section 40 of ARCHITECTURE.md:
- Structured artifact generation, indexing, and storage
- Metadata and reference emission for LLM context
- Native sidecar process management
"""

from .emitters import ArtifactEmitter, artifact_emitter
from .models import (
    Artifact,
    ArtifactRetention,
    ArtifactSensitivity,
    ArtifactSummary,
    ArtifactType,
)
from .sidecar import SidecarManager, SidecarProcess, sidecar_manager
from .store import ArtifactStore, artifact_store

__all__ = [
    "Artifact",
    "ArtifactEmitter",
    "ArtifactRetention",
    "ArtifactSensitivity",
    "ArtifactStore",
    "ArtifactSummary",
    "ArtifactType",
    "SidecarManager",
    "SidecarProcess",
    "artifact_emitter",
    "artifact_store",
    "sidecar_manager",
]
