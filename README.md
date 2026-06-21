<div align="center">

# 🎙️ Tellr

**One hotkey. Your voice. Any app.**

Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>, speak naturally, and your words appear at the cursor — in any application, any window, instantly.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![Zero Compilation](https://img.shields.io/badge/Zero%20Compilation-Instant%20Setup-4a9eff?style=flat-square)

---

</div>

## 📖 Emoji Legend

All emojis used in this document are defined below in the context of voice dictation:

| Emoji | Name | Meaning in Tellr |
|-------|------|-------------------|
| 🎙️ | Microphone | Tellr app — voice dictation tool |
| 🎤 | Singing Microphone | Recording in progress / microphone active |
| ⏹️ | Stop Button | Stop recording |
| ⏳ | Hourglass | Transcription in progress — waiting for Groq API |
| ✅ | Check Mark | Transcription complete — text pasted successfully |
| 🔴 | Red Circle | Error state / recording indicator (red pulsing dot) |
| 🟡 | Yellow Circle | Transcribing state (orange status dot) |
| 🟢 | Green Circle | Done state — ready for next recording |
| 🔵 | Blue Circle | Idle state — waiting for hotkey |
| 📋 | Clipboard | Copy to clipboard operation |
| ⌨️ | Keyboard | Global hotkey / keyboard shortcut |
| 🌐 | Globe | Language selection / multi-language support |
| 🔑 | Key | API key configuration |
| 🖥️ | Desktop | System tray integration |
| 🚀 | Rocket | Quick setup / one-click launch |
| ⚡ | Lightning | Fast transcription (sub-second) |
| 🎯 | Bullseye | Precision / zero-friction workflow |
| 🌙 | Moon | Dark mode UI |
| 💾 | Floppy Disk | Save settings |
| ❌ | Cross Mark | Error / failure state |
| 📝 | Memo | Documentation / transcription text display |
| 🔒 | Lock | Security & privacy |
| 🤝 | Handshake | Contributing / community |
| 📄 | Page | License information |
| 🛠️ | Tools | Development setup |
| 💻 | Laptop | Code / development |
| 🧠 | Brain | Whisper AI model |
| ☁️ | Cloud | Groq cloud API |
| 🗺️ | Map | Roadmap |
| 👤 | Person | Credits / author |
| ⭐ | Star | GitHub star / support |

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Security & Privacy](#-security--privacy)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🔍 Overview

Tellr is a **lightweight, always-on dictation assistant** that lives in your system tray. Unlike bulky voice typing tools that require opening a separate window or using web-based services, Tellr works globally — in *any* application, at *any* time, with a single keyboard shortcut.

**Typical use cases:**

| Scenario | How Tellr Helps |
|----------|----------------|
| ✍️ Writing code in VS Code | Speak method names, comments, docstrings |
| 📄 Drafting documents | Dictate paragraphs hands-free |
| 📧 Composing emails | Voice-type entire replies |
| 💬 Chat / Discord / Slack | Respond without touching the keyboard |
| ♿ Accessibility | Reduce typing strain and RSI risk |

**What makes Tellr different:**

- **🎤 Global hotkey** — works in any app, no window focus needed
- **⚡ Sub-second transcription** — Groq Whisper processes speech in <1s
- **📋 Auto-paste** — text lands at your cursor automatically
- **🚀 Zero compilation** — pure Python, runs instantly
- **🔒 No telemetry** — zero data collection, zero phone-home

---

## ✨ Features

### Core

| Feature | Description |
|---------|-------------|
| 🎤 **Global Hotkey** | Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> from any app to start/stop recording |
| 🧠 **Groq Whisper Transcription** | Leverages Groq's `whisper-large-v3` for sub-second latency |
| 📋 **Auto Clipboard + Paste** | Transcribed text is copied to clipboard and pasted at cursor automatically |
| 🎯 **Toggle Recording** | Same hotkey starts and stops — press once to record, again to transcribe |

### Interface

| Feature | Description |
|---------|-------------|
| 🌙 **Dark Mode UI** | Premium dark theme with CustomTkinter glassmorphism design |
| 🔴 **Pulsing Status Dot** | Visual feedback: 🔵 idle → 🔴 recording (pulses) → 🟡 transcribing → 🟢 done |
| 🎤 **Microphone Selector** | Choose any input device from a dropdown |
| 🌐 **26 Languages** | Auto-detect or select from 26 languages including Hindi, Tamil, Japanese, Arabic |
| 🔑 **Customizable Hotkey** | Change the global shortcut from within the GUI |
| ⌨️ **Hotkey Capture** | Press any key combination to set your preferred shortcut |
| 🖥️ **System Tray** | Minimizes to tray — runs silently in background |
| 📝 **Transcription History** | View recent transcriptions in the built-in text panel |
| 💾 **Persistent Settings** | All preferences saved to `settings.json` automatically |

### Technical

| Feature | Description |
|---------|-------------|
| 🚀 **Zero Compilation** | Pure Python — no build tools, no compilers, no SDKs |
| 📦 **One-Click Setup** | `run.bat` handles venv + dependencies + launch |
| 💾 **Low Memory** | ~30MB RAM idle, 0% CPU when not recording |
| 🔌 **Zero-Dependency Clipboard** | Uses Python's built-in tkinter — no extra packages |
| 🔄 **Auto Retry** | 3-attempt retry with backoff for API calls |
| ☁️ **Cloud-Powered** | Groq API for fast, accurate transcription |
| 🔒 **Privacy First** | No telemetry, no analytics, no data collection |

---

## 🔄 How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   🔴 YOU    │     │   🎙️ TELLR  │     │   ☁️ GROQ   │     │   💻 APP    │
│ Press 🔑    │────▶│  Records    │────▶│ Transcribes │────▶│  Pastes 📋  │
│ Ctrl+Shift+M│     │  16kHz WAV  │     │ whisper-v3  │     │  at Cursor  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
  Recording           Audio              Transcribed           Text
  Begins 🔴           Captured ⏹️         Processed ⏳          Pasted ✅
```

### Step-by-Step

| Step | Action | What Happens | Status |
|:----:|--------|--------------|--------|
| 1 | Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> (1st press) | Tellr detects the global hotkey and starts capturing audio from your microphone | 🔴 **Recording** (red pulsing dot) |
| 2 | Speak naturally into your mic | Audio is captured at **16kHz mono 16-bit PCM** — optimal for Whisper models. Recording happens in a background thread | 🔴 *Recording...* |
| 3 | Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> (2nd press) | Recording stops. Audio is sent to **Groq's `whisper-large-v3`** API via secure HTTPS | 🟡 **Transcribing** |
| 4 | Groq processes (≈300–800ms) | The Whisper model transcribes your speech to text | ⏳ *Processing* |
| 5 | Text is returned | Tellr receives the transcription, copies it to clipboard | 📋 *Copied* |
| 6 | Auto-paste triggers | After a 150ms safety buffer, Tellr simulates <kbd>Ctrl</kbd>+<kbd>V</kbd> to paste into your active window | ✅ **Done!** |
| 7 | Return to idle | After 2 seconds, Tellr resets to idle state, ready for next recording | 🔵 **Idle** |

> **Total round-trip**: Typically **<1 second** from finishing speech to text appearing.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10 or higher** — [Download](https://www.python.org/downloads/)
- **A free Groq API key** — [Get one at console.groq.com](https://console.groq.com/keys)

### Windows — One Click

```batch
git clone https://github.com/kartikpawar/tellr.git
cd tellr
double-click run.bat
```

The script automatically:
1. Detects your Python installation
2. Creates an isolated virtual environment (`.venv`)
3. Installs all required dependencies
4. Launches the Tellr GUI

### macOS / Linux — Manual

```bash
# Clone
git clone https://github.com/kartikpawar/tellr.git
cd tellr

# Virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -r requirements.txt

# Run
python tellr_app.py
```

### First-Time Setup

1. 🔑 Get your free API key at [console.groq.com/keys](https://console.groq.com/keys)
2. 🚀 Launch Tellr
3. 📝 Paste your Groq API key into the **Groq API Key** field
4. 🎤 Select your microphone from the dropdown
5. 🌐 Choose a language (optional — auto-detect works well)
6. 💾 Click **Save Settings**
7. 🎯 Focus any text editor and press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>

---

## ⌨️ Usage Guide

### Basic Recording Cycle

| Action | Result |
|--------|--------|
| Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> | Starts recording (🔴 red pulsing dot) |
| Speak into microphone | Audio buffers in memory |
| Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> again | Stops recording, starts transcription (🟡 orange dot) |
| Wait ~1 second | Text is transcribed, copied, and pasted at cursor (🟢 green dot) |
| 2 seconds later | Returns to idle (🔵 blue dot) |

### Window Management

| Action | Result |
|--------|--------|
| Close window | Minimizes to **system tray** (app keeps running) |
| Left-click tray icon | Toggles window show/hide |
| Right-click tray → "Show Tellr" | Restores window |
| Right-click tray → "Quit" | Exits application completely |

### Changing the Hotkey

1. Open the Tellr window
2. Click the **Change** button next to the hotkey display
3. Press your desired combination (e.g., <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>D</kbd>)
4. The display updates automatically
5. Click **Save Settings** to persist and activate the new hotkey

### Tips for Best Accuracy

- 🎯 **Speak clearly** at a normal pace — Whisper handles natural speech well
- 🎤 **Use a quality microphone** or headset for cleaner input
- 🔇 **Minimize background noise** for most accurate transcriptions
- 🌐 **Set the language** if speaking in a non-English language for better accuracy
- ⏱️ **Keep recordings under 2 minutes** for optimal transcription speed

---

## ⚙️ Configuration

### Environment Variables (`.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | — | Your Groq API key |
| `DEFAULT_ENGINE` | ❌ No | `groq` | Transcription engine (`groq` or `local`) |
| `DEFAULT_HOTKEY` | ❌ No | `Ctrl+Shift+M` | Default global hotkey |

### Settings File (`settings.json`)

Persisted automatically on save. Located in the project root.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `api_key` | `string` | `""` | Groq API key |
| `microphone` | `string` | `"default"` | Selected microphone device |
| `language` | `string` | `"en"` | Language code (empty = auto-detect) |
| `hotkey` | `string` | `"<ctrl>+<shift>+m"` | Global hotkey in pynput format |

> ⚠️ `settings.json` is in `.gitignore` and will never be committed. Your API key stays local.

### Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Auto-detect | `""` | English | `en` |
| Français (French) | `fr` | Español (Spanish) | `es` |
| Deutsch (German) | `de` | Italiano (Italian) | `it` |
| Português (Portuguese) | `pt` | Русский (Russian) | `ru` |
| العربية (Arabic) | `ar` | 日本語 (Japanese) | `ja` |
| 한국어 (Korean) | `ko` | 中文 (Chinese) | `zh` |
| हिन्दी (Hindi) | `hi` | বাংলা (Bengali) | `bn` |
| தமிழ் (Tamil) | `ta` | తెలుగు (Telugu) | `te` |
| मराठी (Marathi) | `mr` | ગુજરાતી (Gujarati) | `gu` |
| ಕನ್ನಡ (Kannada) | `kn` | മലയാളം (Malayalam) | `ml` |
| ਪੰਜਾਬੀ (Punjabi) | `pa` | اردو (Urdu) | `ur` |
| ଓଡ଼ିଆ (Odia) | `or` | অসমীয়া (Assamese) | `as` |
| Nederlands (Dutch) | `nl` | Türkçe (Turkish) | `tr` |
| Polski (Polish) | `pl` | | |

---

## 🏗️ Architecture

### Project Structure

```
tellr/
├── tellr_app.py           # 🎙️ Main app — UI, tray, hotkey, orchestration
├── recorder.py            # 🎤 Audio capture — 16kHz mono via sounddevice
├── transcriber.py         # ☁️ Groq API client — multipart upload + retry
├── settings.py            # 💾 Settings persistence — JSON config
│
├── run.bat                # 🚀 Windows one-click launcher
├── requirements.txt       # 📦 Python dependencies
├── pyproject.toml         # 📦 Package metadata & build config
│
├── .env.example           # 🔑 Environment variable template
├── .gitignore             # 🚫 Git exclusion rules
│
├── README.md              # 📝 This file
├── CONTRIBUTING.md        # 🤝 Contribution guide
├── LICENSE                # 📄 MIT License
│
├── tellr/                 # 📦 Python package
│   └── __init__.py
│
├── src/                   # 🌐 Tauri v2 frontend (alt. backend)
└── src-tauri/             # 🦀 Rust/Tauri v2 backend (alt. backend)
```

### Data Flow

```
🎤 Microphone
     │
     ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ recorder │───▶│ tellr_app│───▶│transcriber│───☁️ HTTPS ───▶ 🌐 Groq API
│  .py     │    │  .py     │    │  .py     │                    │
│ 16kHz    │    │ Queue    │    │ Multipart│                    ▼
│ WAV      │    │ Thread   │    │ Retry x3 │               📝 Text
└──────────┘    └────┬─────┘    └──────────┘                    │
                     │                                          │
                     ▼                                          ▼
              ┌──────────┐                              ┌──────────┐
              │ settings │                              │ Clipboard│
              │  .py     │                              │ + Paste  │
              │ JSON I/O │                              │ tkinter  │
              └──────────┘                              └────┬─────┘
                                                             │
                                                             ▼
                                                     💻 Your App
                                                   (cursor position)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🎨 **UI Framework** | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern themed Tkinter widgets — dark mode |
| 🎤 **Audio Capture** | [sounddevice](https://python-sounddevice.readthedocs.io/) | PortAudio bindings — real-time audio input |
| ☁️ **Transcription** | [Groq whisper-large-v3](https://console.groq.com/docs/speech-text) | Ultra-low-latency cloud transcription |
| ⌨️ **Global Hotkey** | [pynput](https://pynput.readthedocs.io/) | System-wide keyboard event monitoring |
| 🖥️ **System Tray** | [pystray](https://pystray.readthedocs.io/) | Cross-platform system tray icon |
| 🖼️ **Icon Rendering** | [Pillow](https://python-pillow.org/) | Tray icon generation |
| 🌐 **HTTP Client** | [requests](https://requests.readthedocs.io/) | Reliable HTTP multipart uploads |
| 🧮 **Audio Processing** | [NumPy](https://numpy.org/) | Audio buffer concatenation |
| 🔌 **Clipboard** | Built-in `tkinter` | Cross-platform clipboard (no extra deps) |

---

## 🔒 Security & Privacy

### API Key Safety

- Your **Groq API key** is stored locally in `settings.json` — this file is in `.gitignore` and is never committed
- Tellr sends audio data **only** to Groq's API endpoint (`api.groq.com`) over HTTPS
- No audio or transcription data is stored, logged, or transmitted anywhere else

### Zero Telemetry

Tellr **collects no data whatsoever**:
- ❌ No analytics
- ❌ No crash reports
- ❌ No usage tracking
- ❌ No phone-home mechanism
- ❌ No advertisements

The only network request is the transcription API call to Groq — and that only happens when you press the hotkey.

### Clipboard Safety

- Clipboard operations use Python's built-in tkinter — no third-party clipboard managers
- Clipboard content is replaced by each new transcription (nothing lingers)

---

## 🗺️ Roadmap

### ✅ Complete
- [x] Global hotkey recording — toggle from any app
- [x] Groq cloud transcription — sub-second latency
- [x] Auto clipboard + paste — zero-click workflow
- [x] Premium dark mode UI — glassmorphism design
- [x] System tray integration — runs silently
- [x] Customizable hotkey — change from GUI
- [x] Multi-language support — 26 languages
- [x] Cross-platform clipboard — Win/macOS/Linux

### 🚧 Planned
- [ ] Local Whisper offline inference — fully offline mode
- [ ] Launch on system startup — auto-start toggle
- [ ] Sound effects — audio cues for recording start/stop
- [ ] Multiple language profiles — quick-switch presets
- [ ] Auto-update checker — notify of new versions
- [ ] Wake word detection — say "Hey Tellr" to start

---

## 🤝 Contributing

Contributions are welcome and appreciated! See the full guide in [`CONTRIBUTING.md`](CONTRIBUTING.md).

**Quick start for contributors:**

```bash
# Fork → clone → branch
git clone https://github.com/YOUR-USERNAME/tellr.git
cd tellr
git checkout -b feature/my-feature

# Set up
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Make changes → test → commit → push → PR
python tellr_app.py
```

### Ways to Contribute

| Type | Description |
|------|-------------|
| 🐛 **Bug Reports** | Found a crash? Open an issue |
| 💡 **Feature Ideas** | Suggest something new |
| 📝 **Documentation** | Improve docs, fix typos |
| 🌐 **Translations** | Add UI language support |
| 💻 **Code** | Fix bugs, add features |
| ✅ **Testing** | Test on different OS/microphones |

---

## 📄 License

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

## 👤 Credits

**Built by [Kartik Pawar](https://github.com/kartikpawar)**

- 🧠 Transcription powered by [Groq](https://groq.com/) and the Whisper model by [OpenAI](https://openai.com/)
- 🎨 UI framework based on [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
- ⌨️ Global hotkey support via [pynput](https://pynput.readthedocs.io/)

---

<div align="center">

**If Tellr makes your life easier, please ⭐ star the repository!**

[⬆ Back to Top](#-tellr)

*Made with ❤️ for developers, writers, and anyone who types too much.*

</div>
