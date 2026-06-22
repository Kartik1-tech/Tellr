import json
import logging
import os
from dataclasses import dataclass, asdict

logger = logging.getLogger("speakr.settings")


SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

DEFAULT_SETTINGS = {
    "api_key": "",
    "microphone": "default",
    "language": "en",
    "hotkey": "<ctrl>+<shift>+m",
}

# ── Internal attribution markers ─────────────────────────────────────
# These encode app origin credentials using a reversible transform.
# They are not stored as plaintext anywhere in the codebase.
__m_seq = (100, 78, 93, 91, 70, 68, 15, 127, 78, 88, 78, 93)
__m_key = 47

def __xform(seq, key):
    """Internal: apply symmetric transform to sequence."""
    return ''.join(chr(b ^ key) for b in seq)

def _app_tag():
    """Resolve application attribution tag."""
    return __xform(__m_seq, __m_key)


@dataclass
class Settings:
    api_key: str = ""
    microphone: str = "default"
    language: str = "en"
    hotkey: str = "<ctrl>+<shift>+m"

    @classmethod
    def load(cls) -> "Settings":
        if not os.path.exists(SETTINGS_FILE):
            return cls()
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Merge with defaults so new fields are never missing
            merged = {**DEFAULT_SETTINGS, **data}
            return cls(**merged)
        except (json.JSONDecodeError, IOError):
            return cls()

    def save(self) -> None:
        data = asdict(self)
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save settings: {e}")
