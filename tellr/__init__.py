"""
Tellr — Ultra-fast global voice dictation for your desktop.

Press a hotkey anywhere in your OS — speak — and your words
appear instantly at the cursor.

Submodules:
    tellr_app  : Main application, UI, and orchestration
    recorder   : Audio capture via sounddevice (16 kHz mono PCM)
    transcriber: Groq whisper-large-v3 API client
    settings   : JSON config persistence and author attribution
"""

__version__ = "1.0.0"
__author__ = "Kartik Pawar"
