# Speakr - Project Handover

## Overview
Speakr is a lightweight desktop dictation app. It uses a global hotkey to record audio, transcribes it via Groq's API, and auto-pastes the result.

## Current Architecture

### Python Stack (Primary - Working)
- `speakr_app.py` - Main app: CustomTkinter UI, system tray, global hotkey, clipboard, auto-paste
- `recorder.py` - 16kHz mono audio capture via sounddevice
- `transcriber.py` - Groq cloud transcription via requests
- `settings.py` - JSON settings persistence
- `run.bat` - One-click launcher

### Rust/Tauri Stack (Alternative)
- `src-tauri/src/main.rs` - Tauri entry point with audio worker thread
- `src-tauri/src/audio.rs` - CPAL audio capture with resampler
- `src-tauri/src/transcribe.rs` - Groq API + local model download
- `src-tauri/src/paste.rs` - Enigo auto-paste
- `src-tauri/src/settings.rs` - Settings with .env + JSON

## Key Architectural Decisions

1. **Audio Thread Safety** (Rust): CPAL streams are not `Send`/`Sync` on Windows. Solved via dedicated worker thread with mpsc channel.
2. **Groq Cloud Default**: Local Whisper is a stub (needs whisper-rs + LLVM).
3. **Clipboard Paste Delay**: 150ms sleep before paste to avoid race conditions.

## Roadmap
- Local Whisper offline inference (whisper-rs integration)
- Launch on login
- macOS/Linux clipboard support (currently Win32 native)
