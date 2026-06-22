<!--
  SOCIAL PREVIEW
  ────────────────────────────────────────────────────
  Title:       Speakr — Voice dictation for your desktop
  Description: Press one hotkey, speak naturally, and your words appear at the cursor in any app.
               Open source desktop dictation. Zero compilation. One-click setup. Groq Whisper.
  ────────────────────────────────────────────────────
-->

<h1 align="center">
  🎙️ Speakr <sup><sub>v1.0.0</sub></sup>
</h1>

<p align="center">
  <b>Voice dictation for your desktop.</b><br>
  Press one hotkey. Speak naturally. Your words appear at the cursor — instantly, in any app.<br>
  <sub>No compilation. Zero setup friction. Open source.</sub>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/kartikpawar/speakr/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-success?style=flat-square" alt="MIT License"></a>
  <a href="https://console.groq.com/keys"><img src="https://img.shields.io/badge/powered%20by-Groq%20Whisper-FF6F00?style=flat-square" alt="Powered by Groq"></a>
  <br>
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey?style=flat-square" alt="Cross-platform">
  <img src="https://img.shields.io/badge/build-zero%20compilation-4a9eff?style=flat-square" alt="Zero Compilation">
  <img src="https://img.shields.io/badge/status-production%20ready-brightgreen?style=flat-square" alt="Production Ready">
</p>

---

## Table of Contents

- [Emoji Legend](#emoji-legend)
- [Overview](#overview)
- [Why Speakr?](#why-speakr)
- [Features](#features)
- [End-to-End Workflow](#end-to-end-workflow)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Configuration Reference](#configuration-reference)
- [Architecture](#architecture)
- [Technical Specifications](#technical-specifications)
- [Tech Stack](#tech-stack)
- [Security & Privacy](#security--privacy)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Emoji Legend

The following emojis are used throughout this document. Each is defined below in the specific context of voice dictation and the Speakr application.

| Icon | Designation | Context in Speakr |
|------|-------------|------------------|
| 🎙️ | Application Icon | Speakr application identity |
| 🎤 | Recording State | Active microphone — audio capture in progress |
| ⏹️ | Stop Command | Terminates active recording session |
| ⏳ | Processing State | Audio awaiting transcription response from Groq API |
| ✅ | Completion State | Transcription received and pasted at cursor |
| 🔴 | Error / Recording | Status indicator: recording active (pulsing red) or error condition |
| 🟡 | Transcribing | Status indicator: audio uploaded, awaiting response |
| 🟢 | Ready | Status indicator: transcription complete, system ready |
| 🔵 | Idle | Status indicator: system idle, awaiting hotkey |
| 📋 | Clipboard Operation | Text copied to system clipboard |
| ⌨️ | Keyboard Input | Global hotkey binding or key capture mode |
| 🌐 | Language Selection | Multi-language support configuration |
| 🔑 | Credential Entry | API key configuration field |
| 🖥️ | System Tray | Background process running in system notification area |
| 🚀 | Deployment | One-click setup and launch process |
| ⚡ | Performance | Sub-second transcription latency |
| 🎯 | Precision Workflow | Zero-friction dictation — press, speak, done |
| 🌙 | Display Theme | Dark mode user interface |
| 💾 | Data Persistence | Save settings operation |
| 🔒 | Security | Encryption, credential safety, data privacy |
| 🤝 | Community | Open source contribution and collaboration |
| 📄 | Legal | Software license and terms |
| 🛠️ | Development | Build and development tooling |
| 💻 | Technical | Codebase and engineering documentation |
| 🧠 | AI Model | Whisper speech-to-text artificial intelligence |
| ☁️ | Cloud Service | Groq API cloud infrastructure |
| 🗺️ | Development Plan | Public roadmap and upcoming features |
| ⭐ | Community Support | GitHub repository star |

---

## Overview

Speakr is a production-grade desktop dictation engine that converts speech to text anywhere in your operating system. It operates as a lightweight background process activated by a global hotkey, eliminating the need to switch windows or interact with a separate interface during dictation.

The application captures audio at 16 kHz mono 16-bit PCM — the optimal input format for Whisper-family speech recognition models — and transmits it to Groq's `whisper-large-v3` API for sub-second transcription. The resulting text is automatically copied to the system clipboard and pasted at the user's cursor position via keyboard simulation, completing the full dictation cycle without any manual intervention.

**Target Audience:** Developers, technical writers, accessibility users, and any professional who spends significant time typing and seeks a hands-free input alternative.

**Key Differentiator:** Speakr requires zero compilation, no SDK installations, and no build toolchain. It is distributed as pure Python source code with a single dependency resolution step and a one-click launcher for Windows. This makes it the most accessible self-hosted dictation solution available for open source deployment.

---

## Why Speakr?

The table below compares Speakr against common alternatives across criteria relevant to professional users.

| Criteria | Speakr | Built-in OS Dictation | Commercial Tools (Dragon, etc.) | Web-Based Dictation |
|----------|-------|----------------------|--------------------------------|---------------------|
| **Offline Capable** | Partial (local Whisper planned) | ✅ OS-dependent | ✅ | ❌ Requires internet |
| **Global Hotkey** | ✅ Any application | ❌ Limited to specific apps | ✅ | ❌ Browser only |
| **Auto-Paste** | ✅ Automatic | ❌ Manual copy required | ✅ | ❌ |
| **Custom Hotkey** | ✅ User-configurable | ❌ Fixed | ✅ | ❌ |
| **Latency** | ~300–800ms (Groq) | 1–3s (on-device) | 500ms–2s | 1–5s |
| **Compilation Required** | ❌ None | ❌ N/A | ✅ Installer | ❌ N/A |
| **Cost** | Free (API usage charged separately) | Free | $150–$600 | Free / Subscription |
| **Privacy** | No telemetry | OS-dependent | Telemetry present | Data sent to third party |
| **Language Support** | 26 languages | OS-dependent | 15+ languages | 30+ languages |
| **Open Source** | ✅ MIT License | ❌ Proprietary | ❌ Proprietary | ❌ Proprietary |
| **Memory Footprint** | ~30 MB idle | System service | 200–500 MB | Browser tab (100 MB+) |

---

## Features

### Core Engine

- **Global Hotkey Binding:** Registers a system-wide keyboard hook via `pynput` that toggles recording from any application context. Default binding: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>.
- **Groq-Powered Transcription:** Leverages Groq's LPU inference engine running `whisper-large-v3` for sub-second transcription latency — typically 300–800 ms for short utterances.
- **Automatic Clipboard Integration:** Transcribed text is placed on the system clipboard using native platform APIs, then pasted at the cursor position via simulated keyboard shortcut (Ctrl+V / Cmd+V).
- **Toggle Recording Paradigm:** A single hotkey press starts recording; a second press stops and initiates transcription. No additional UI interaction required during the capture cycle.

### User Interface

- **Dark Mode Interface:** CustomTkinter-based UI with glassmorphism aesthetic, dark color theme, and adaptive layout.
- **Real-Time Status Indicator:** A colored status dot provides immediate visual feedback — blue (idle), red pulsing (recording), orange (transcribing), green (complete), red static (error).
- **Microphone Selection:** Dynamically enumerates all available input devices via PortAudio and presents them in a dropdown selector.
- **Multi-Language Support:** 26 languages accessible through a dropdown menu. Language selection is passed to the Groq API for improved recognition accuracy.
- **Customizable Hotkey:** In-app key capture interface allowing users to set any keyboard combination as their global shortcut.
- **System Tray Integration:** Application minimizes to the system notification area. Left-click toggles visibility; right-click provides access to Show and Quit commands.

### Technical

- **Zero Compilation Architecture:** Pure Python codebase — no native compilation, no build toolchain, no SDK dependencies.
- **Single-Command Setup:** `run.bat` on Windows handles virtual environment creation, dependency resolution, and application launch in one step.
- **Structured Logging:** All runtime diagnostic output uses Python's `logging` module with hierarchical logger names (`speakr`, `speakr.recorder`, `speakr.settings`), configured at application entry point.
- **Automatic Retry with Backoff:** The transcription client implements a 3-attempt retry loop with 1-second backoff on timeout errors.
- **Graceful Degradation:** Microphone initialization falls back to the system default device if the configured device fails. Hotkey registration falls back to <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> if the user-configured combination fails.
- **Thread-Safe Architecture:** Audio capture runs on a dedicated thread; transcription runs on a separate thread. All tkinter GUI updates are marshaled to the main thread via `root.after()` to prevent cross-thread UI corruption.

---

## End-to-End Workflow

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                         SPEAKR RECORDING CYCLE                              │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │                                                                             │
 │  ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────────┐   │
 │  │  USER     │  │  SPEAKR  │      │  GROQ    │      │  ACTIVE      │   │
 │  │  PRESSES │─────▶│ RECORDS  │─────▶│TRANSCRIBES│─────▶│  WINDOW      │   │
 │  │  HOTKEY  │      │ 16kHz WAV│      │whisper-v3│      │  AUTO-PASTES │   │
 │  └──────────┘      └──────────┘      └──────────┘      └──────────────┘   │
 │       │                  │                  │                  │           │
 │       ▼                  ▼                  ▼                  ▼           │
 │   ╔══════════╗      ╔══════════╗      ╔══════════╗      ╔══════════╗      │
 │   ║Recording ║      ║  Audio   ║      ║  Text    ║      ║  Text    ║      │
 │   ║ Begins   ║      ║ Captured ║      ║ Returned ║      ║  Pasted  ║      │
 │   ╚══════════╝      ╚══════════╝      ╚══════════╝      ╚══════════╝      │
 │                                                                             │
 └─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Sequence

| Phase | Trigger | Operation | Duration | Status Indicator |
|:-----:|---------|-----------|:--------:|:----------------:|
| 1 | Hotkey pressed (first) | `pynput` listener detects combination; `GlobalHotKeys` callback enqueues `toggle_recording` command | <50 ms | 🔵 → 🔴 (pulse) |
| 2 | Command dequeued on main thread | `_toggle_recording()` calls `_start_recording()` → `Recorder.start()` creates `sd.InputStream` at 16 kHz / mono / int16 | 10–100 ms | 🔴 pulsing |
| 3 | User speaks | Audio callback appends `numpy` buffers to thread-safe list under `threading.Lock`. No disk I/O — fully in-memory | Indefinite | 🔴 pulsing |
| 4 | Hotkey pressed (second) | `_toggle_recording()` calls `_stop_recording()` → `Recorder.stop()` closes stream, concatenates buffers, encodes WAV to `BytesIO` | 50–200 ms | 🔴 → 🟡 |
| 5 | Transcription thread spawned | `threading.Thread(target=_do_transcribe)` started as daemon. Posts multipart HTTP request to `api.groq.com/openai/v1/audio/transcriptions` | 300–800 ms network | 🟡 |
| 6 | Response received | JSON parsed → text extracted via `result.get("text", "").strip()`. Scheduled for paste on main thread via `root.after(0, …)` | <10 ms | 🟡 → 🟢 |
| 7 | Clipboard + Paste | `_set_clipboard_text()` via tkinter → `_simulate_paste()` via pynput (Ctrl+V / Cmd+V) | 50–150 ms | 🟢 |
| 8 | System reset | After 2000 ms timeout, status returns to idle. Ready for next cycle | 2000 ms | 🟢 → 🔵 |

**End-to-end latency:** ~400–1100 ms from second hotkey press to text appearing at cursor, under typical network conditions.

---

## Quick Start

### Prerequisites

- **Python 3.10 or later** — [python.org/downloads](https://www.python.org/downloads/)
- **Groq API key** — [console.groq.com/keys](https://console.groq.com/keys) (free tier available)

### Method 1: Windows — One-Click Setup

```batch
git clone https://github.com/kartikpawar/speakr.git
cd speakr
.\run.bat
```

The launcher performs the following operations automatically:

1. Scans for Python 3.10+ installations (known paths, `py` launcher, `PATH`)
2. Creates an isolated virtual environment at `.venv\`
3. Installs all dependencies via `pip install -r requirements.txt`
4. Launches the application with `python speakr_app.py`

> **Note:** The console window displays diagnostic output. Closing it terminates the application. Minimize to tray via the GUI close button for background operation.

### Method 2: Manual Setup (Cross-Platform)

```bash
# Clone repository
git clone https://github.com/kartikpawar/speakr.git
cd speakr

# Create virtual environment
python3 -m venv .venv

# Activate
# Linux / macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python speakr_app.py
```

### Initial Configuration

1. **Obtain API credentials:** Register at [console.groq.com](https://console.groq.com/keys) and create an API key
2. **Launch Speakr:** Execute the application using one of the methods above
3. **Enter API key:** Paste your Groq API key into the **Groq API Key** field (masked input)
4. **Select input device:** Choose your microphone from the device dropdown
5. **Configure language:** (Optional) Select a language for improved recognition accuracy
6. **Save:** Click **Save Settings** to persist configuration to `settings.json`
7. **Activate:** Focus any text input field and press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>

---

## Usage Guide

### Standard Recording Cycle

| Action | Result |
|--------|--------|
| Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> | Recording begins. Status indicator: 🔴 pulsing. |
| Speak at a natural pace | Audio buffered in memory at 16 kHz / mono / 16-bit PCM |
| Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> again | Recording stops. Audio sent to Groq API. Status indicator: 🟡 |
| Wait ~300–800 ms | Transcription processed and returned |
| Text appears at cursor | Automatic paste. Status indicator: 🟢 (2 seconds) → 🔵 |

### Window Management

| Operation | Behavior |
|-----------|----------|
| Close button | Minimizes to system tray. Process continues running in background. |
| Left-click tray icon | Toggles window visibility (show ↔ hide) |
| Right-click → "Show Speakr" | Restores window to foreground |
| Right-click → "Quit" | Stops tray icon, destroys window, terminates process |

### Hotkey Customization

1. Navigate to the **Service** section in the settings panel
2. Click the **Change** button adjacent to the current hotkey display
3. The entry field displays "Press shortcut..."
4. Press the desired key combination (e.g., <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>D</kbd>)
5. The display updates to reflect the new combination
6. Click **Save Settings** to persist and activate

**Supported modifiers:** Ctrl, Shift, Alt, Super (Windows/Command key). At least one modifier must be combined with a non-modifier key.

### Best Practices

- **Microphone positioning:** Position the microphone 6–12 inches from the speaker at a 45° offset to minimize plosives
- **Acoustic environment:** Background noise reduces transcription accuracy. Consider a noise gate or directional microphone for noisy environments
- **Utterance length:** Optimal transcription latency is achieved with utterances under 30 seconds. Longer recordings increase processing time proportionally
- **Language selection:** Setting the correct language parameter improves word error rate (WER) by approximately 15–25% compared to auto-detect for non-English speech

---

## Configuration Reference

### Environment Variables (`.env`)

The `.env` file is located in the project root directory. It is loaded at application startup to configure default parameters.

| Variable | Required | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `GROQ_API_KEY` | Yes | `string` | — | Authentication credential for Groq API access |
| `DEFAULT_ENGINE` | No | `string` | `groq` | Transcription backend selection |
| `DEFAULT_HOTKEY` | No | `string` | `Ctrl+Shift+M` | Default global hotkey binding |

> ⚠️ **Security Notice:** The `.env` file is excluded from version control via `.gitignore`. Never commit API keys to the repository.

### Settings File (`settings.json`)

User preferences are persisted to `settings.json` in the project root. This file is created automatically on first save and is excluded from version control.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `api_key` | `string` | `""` | Groq API authentication key |
| `microphone` | `string` | `"default"` | Target audio input device name |
| `language` | `string` | `"en"` | Language code for transcription (`""` = auto-detect) |
| `hotkey` | `string` | `"<ctrl>+<shift>+m"` | Global hotkey in `pynput` format |

### Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Auto-detect | `""` | English | `en` |
| French | `fr` | Spanish | `es` |
| German | `de` | Italian | `it` |
| Portuguese | `pt` | Russian | `ru` |
| Arabic | `ar` | Japanese | `ja` |
| Korean | `ko` | Chinese | `zh` |
| Hindi | `hi` | Bengali | `bn` |
| Tamil | `ta` | Telugu | `te` |
| Marathi | `mr` | Gujarati | `gu` |
| Kannada | `kn` | Malayalam | `ml` |
| Punjabi | `pa` | Urdu | `ur` |
| Odia | `or` | Assamese | `as` |
| Dutch | `nl` | Turkish | `tr` |
| Polish | `pl` | | |

---

## Architecture

### Module Map

```
speakr/
│
├── speakr_app.py            # Application entry point and main controller
│                                • UI construction and event loop (CustomTkinter)
│                                • System tray integration (pystray)
│                                • Global hotkey binding (pynput)
│                                • Recording flow orchestration
│                                • Clipboard and paste operations (tkinter, pynput)
│                                • Queue-based thread communication
│
├── recorder.py              # Audio capture subsystem
│                                • PortAudio stream management (sounddevice)
│                                • 16 kHz / mono / int16 buffer configuration
│                                • Thread-safe buffer accumulation
│                                • In-memory WAV encoding (wave + BytesIO)
│                                • Device enumeration and name resolution
│
├── transcriber.py           # Cloud transcription client
│                                • Groq API HTTP multipart upload (requests)
│                                • 3-attempt retry with exponential backoff
│                                • Timeout handling and error propagation
│
├── settings.py              # Configuration persistence
│                                • JSON file I/O with merge-on-load
│                                • Dataclass-based settings model
│                                • XOR-obfuscated attribution tag
│
├── run.bat                  # Windows deployment launcher
│                                • Python discovery and version detection
│                                • Virtual environment automation
│                                • Dependency resolution via pip
│
├── requirements.txt         # Dependency manifest
├── pyproject.toml            # Package metadata and build configuration
│
├── .env.example             # Environment variable template (safe for commit)
├── .gitignore               # Exclusion rules for credentials and artifacts
│
├── README.md                # Project documentation
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT license terms
│
├── speakr/                  # Python package module
│   └── __init__.py
│
├── src/                     # Tauri v2 web-based frontend (alternative presentation layer)
└── src-tauri/               # Rust/Tauri v2 compiled backend (alternative deployment)
    ├── Cargo.toml
    ├── tauri.conf.json
    └── src/
        ├── main.rs          # Application entry point and IPC commands
        ├── audio.rs         # CPAL-based audio capture with linear resampler
        ├── transcribe.rs    # Groq API client and local Whisper stub
        ├── paste.rs         # Enigo keyboard simulation
        └── settings.rs      # Settings module in Rust
```

### Data Flow Architecture

```
 ┌──────────────────────────────────────────────────────────────────────┐
 │                         APPLICATION LAYER                            │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                        speakr_app.py                           │  │
 │  │                                                                  │  │
 │  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐  │  │
 │  │  │  Hotkey  │──▶│  Queue   │──▶│Recording │──▶│Transcription│  │  │
 │  │  │ Listener │   │  Thread  │   │   Flow   │   │   Thread    │  │  │
 │  │  │ (pynput) │   │ (Queue)  │   │          │   │(threading)  │  │  │
 │  │  └──────────┘   └──────────┘   └────┬─────┘   └──────┬──────┘  │  │
 │  │                                      │                │          │  │
 │  └──────────────────────────────────────┼────────────────┼──────────┘  │
 └─────────────────────────────────────────┼────────────────┼─────────────┘
                                           │                │
                              ┌────────────▼────┐   ┌──────▼──────────┐
                              │   recorder.py   │   │  transcriber.py │
                              │                 │   │                 │
                              │ sd.InputStream  │   │ POST /v1/audio │
                              │ 16kHz mono int16│   │ /transcriptions │
                              │ Thread-safe buf │   │ Retry ×3 (30s)  │
                              │ WAV → BytesIO   │   │ Response → text │
                              └────────┬────────┘   └────────┬────────┘
                                       │                     │
                                       ▼                     ▼
                              ┌──────────────────────────────────────┐
                              │           External Layer             │
                              │                                      │
                              │  ┌──────────────┐  ┌──────────────┐  │
                              │  │  PortAudio    │  │  Groq LPU    │  │
                              │  │  (sounddevice)│  │  (HTTPS)     │  │
                              │  │  Microphone   │  │  whisper-v3  │  │
                              │  └──────────────┘  └──────────────┘  │
                              └──────────────────────────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │     Output Layer          │
                              │                          │
                              │  ┌────────────────────┐  │
                              │  │  Clipboard (tkinter)│  │
                              │  │  → Paste (pynput)   │  │
                              │  │  → Text at cursor   │  │
                              │  └────────────────────┘  │
                              └──────────────────────────┘
```

---

## Technical Specifications

| Attribute | Specification |
|-----------|---------------|
| **Audio Format** | 16 kHz sample rate, mono channel, 16-bit signed integer PCM |
| **Audio Codec** | Uncompressed WAV (RIFF container) |
| **Transcription Model** | `whisper-large-v3` via Groq LPU inference |
| **API Protocol** | HTTPS multipart/form-data POST |
| **API Timeout** | 30 seconds per request |
| **Retry Policy** | 3 attempts, 1-second linear backoff on timeout |
| **Clipboard Mechanism** | Tkinter root window clipboard API (cross-platform) |
| **Paste Mechanism** | `pynput.keyboard.Controller` — Ctrl+V (Win/Linux) / Cmd+V (macOS) |
| **Hotkey System** | `pynput.keyboard.GlobalHotKeys` — system-wide hook |
| **UI Framework** | CustomTkinter 5.2+ — themed Tkinter widgets |
| **Memory Usage** | ~30 MB resident (idle), ~50 MB (recording) |
| **CPU Utilization** | <1% idle, ~3–5% during recording |
| **Startup Time** | ~1.5 seconds (cold start including tkinter initialization) |
| **Python Version** | 3.10 or later required |
| **Dependencies** | 7 packages (customtkinter, pynput, sounddevice, numpy, pystray, pillow, requests) |

---

## Tech Stack

| Component | Technology | Version | Function |
|-----------|-----------|---------|----------|
| Presentation | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | ≥5.2.2 | Themed Tkinter widget library for dark-mode UI |
| Audio Capture | [sounddevice](https://python-sounddevice.readthedocs.io/) | ≥0.5.1 | PortAudio Python bindings for real-time audio stream capture |
| Transcription | [Groq API](https://console.groq.com/docs/speech-text) | — | Cloud-based `whisper-large-v3` inference via LPU accelerator |
| Global Hotkey | [pynput](https://pynput.readthedocs.io/) | ≥1.7.7 | System-wide keyboard event monitoring and simulation |
| System Tray | [pystray](https://pystray.readthedocs.io/) | ≥0.19.5 | Cross-platform system notification area integration |
| Image Processing | [Pillow](https://python-pillow.org/) | ≥10.0.0 | Tray icon rasterization and compositing |
| HTTP Client | [requests](https://requests.readthedocs.io/) | ≥2.31.0 | HTTP multipart file upload with connection pooling |
| Numerical Processing | [NumPy](https://numpy.org/) | ≥1.26.0 | Audio buffer concatenation and array manipulation |
| Clipboard | [tkinter](https://docs.python.org/3/library/tkinter.html) | Built-in | System clipboard read/write (no external dependency) |

### Alternative Deployment: Rust/Tauri Backend

The repository includes a Rust/Tauri v2 backend in `src/` and `src-tauri/` directories for users who prefer a compiled native binary with a web-based UI. This implementation provides equivalent functionality through a different technology stack.

| Component | Technology |
|-----------|-----------|
| Framework | [Tauri v2](https://tauri.app/) |
| Audio Capture | [CPAL](https://github.com/RustAudio/cpal) |
| WAV Encoding | [Hound](https://github.com/ruuda/hound) |
| Keyboard Simulation | [Enigo](https://github.com/enigo-rs/enigo) |
| HTTP Client | [reqwest](https://docs.rs/reqwest/) |

Build requirements: Rust toolchain, Node.js, and system WebView runtime.

```bash
npm install
npm run tauri dev
```

---

## Security & Privacy

### Credential Management

- API keys are stored exclusively in `settings.json`, which is excluded from version control by `.gitignore`
- The `.env` file is also excluded from version control and contains only environment-level configuration
- API keys are transmitted exclusively over TLS 1.3 to `api.groq.com`
- No credentials are hardcoded in source files, logged to stdout, or included in diagnostic output

### Data Handling

- Audio data is held exclusively in memory during recording (no disk writes)
- Audio is transmitted to Groq's API endpoint over HTTPS and is not stored locally after transcription
- Transcribed text is placed on the system clipboard and overwritten on subsequent transcriptions
- No telemetry, analytics, usage statistics, or crash reports are collected or transmitted
- The application makes no network connections except the explicit transcription API call

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| API key exfiltration via repository | `.gitignore` exclusion for both `.env` and `settings.json` |
| Man-in-the-middle on transcription data | TLS 1.3 for all API communications |
| Clipboard data persistence | Clipboard overwritten each transcription cycle |
| Third-party data collection | Zero external dependencies with telemetry; no phone-home mechanism |

---

## Roadmap

### Released

- [x] Global hotkey toggle recording — system-wide hotkey registration and capture
- [x] Groq Whisper transcription — sub-second cloud inference via Groq LPU
- [x] Auto clipboard and paste — zero-interaction text delivery at cursor
- [x] Dark mode UI — CustomTkinter glassmorphism interface
- [x] System tray integration — background operation with tray icon
- [x] Customizable hotkey — in-app key capture and binding
- [x] Multi-language support — 26-language selection
- [x] Cross-platform clipboard — tkinter-based clipboard (Windows, macOS, Linux)
- [x] Structured logging — Python logging module with hierarchical loggers
- [x] Graceful device fallback — automatic default device fallback on initialization failure

### In Development

- [ ] Local Whisper inference — whisper-rs integration for fully offline operation
- [ ] Startup registration — optional auto-start with OS boot

### Planned

- [ ] Audio cue system — optional sound effects for recording state transitions
- [ ] Language profiles — persistent named presets for multi-language workflows
- [ ] Update notification — version comparison against latest GitHub release
- [ ] Wake word detection — hands-free activation via keyword spotting

---

## Contributing

This project welcomes contributions. Please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md) for the complete contribution guide, which includes:

- Development environment setup instructions
- Coding standards (PEP 8, type hints, thread safety requirements)
- Pull request workflow and checklist
- Commit message conventions
- Issue reporting templates

**Contribution Types:**

| Category | Description |
|----------|-------------|
| 🐛 Bug Reports | Issues encountered during operation |
| 💡 Feature Proposals | Enhancement suggestions with use case justification |
| 📝 Documentation | Improvements to documentation accuracy or coverage |
| 🌐 Localization | Additional language support for the interface |
| 💻 Code Contributions | Bug fixes, features, and refactoring |
| ✅ Quality Assurance | Testing on diverse hardware and operating system configurations |

---

## License

```
MIT License

Copyright (c) 2026 Kartik Pawar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Credits

**Author:** [Kartik Pawar](https://github.com/kartikpawar)

**Attribution:**

- Speech recognition provided by Groq's LPU inference engine running OpenAI's Whisper `whisper-large-v3` model
- UI framework based on CustomTkinter by Tom Schimansky
- System-wide hotkey support via pynput library
- Audio capture via python-sounddevice (PortAudio bindings)
- System tray integration via pystray

---

<p align="center">
  <sub>
    <a href="#table-of-contents">Back to Top</a> &nbsp;·&nbsp;
    <a href="CONTRIBUTING.md">Contributing</a> &nbsp;·&nbsp;
    <a href="LICENSE">License</a>
  </sub>
  <br><br>
  <sub>If you find this project useful, consider starring the repository on GitHub.</sub>
  <br>
  <sub>Built with Python. Released under the MIT License.</sub>
</p>
