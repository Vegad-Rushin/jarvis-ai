"""Tests for JARVIS Dynamic Configuration."""

from jarvis.config import JarvisSettings, settings


def test_settings_initialization() -> None:
    """Ensure settings are discovered and initialized properly."""
    assert settings.APP_NAME == "JARVIS"
    assert settings.APP_VERSION == "1.0.1"
    assert len(settings.ALLOWED_MODEL_FAMILIES) == 6
    assert "Gemini 3.8 Live" in settings.ALLOWED_MODEL_FAMILIES
    assert "GPT-OSS 120B" in settings.ALLOWED_MODEL_FAMILIES
    assert "Qwen 3.8 27B" in settings.ALLOWED_MODEL_FAMILIES
    assert "Gemini 3.1 Flash-Lite" in settings.ALLOWED_MODEL_FAMILIES
    assert "Gemini 3.5 Flash-Lite" in settings.ALLOWED_MODEL_FAMILIES
    assert "Gemma 4 31B" in settings.ALLOWED_MODEL_FAMILIES
    assert settings.MODEL_MAP_GEMINI_3_1_FLASH_LITE == "gemini-3.1-flash-lite"
    assert settings.MODEL_MAP_GEMINI_3_5_FLASH_LITE == "gemini-3.5-flash-lite"


def test_directory_creation(test_settings: JarvisSettings) -> None:
    """Verify runtime directory creation."""
    test_settings.ensure_directories()
    assert test_settings.DATA_DIR.exists()
    assert test_settings.LOG_DIR.exists()
    assert test_settings.ARTIFACTS_DIR.exists()
