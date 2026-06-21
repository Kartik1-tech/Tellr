# Contributing to Tellr

First off, thank you for considering contributing to Tellr. It's people like you who make this tool better for everyone.

This document outlines the guidelines for contributing. Following them helps maintainers and contributors communicate effectively and keeps the project healthy.

> **Note**: By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

## Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Ways to Contribute](#-ways-to-contribute)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Coding Standards](#-coding-standards)
- [Pull Request Process](#-pull-request-process)
- [Commit Guidelines](#-commit-guidelines)
- [Issue Reporting](#-issue-reporting)
- [Feature Requests](#-feature-requests)
- [Review Process](#-review-process)
- [Getting Help](#-getting-help)

---

## 🤝 Code of Conduct

This project adheres to a simple code of conduct:

- **Be respectful** — Disagreement is not an excuse for disrespect
- **Assume good faith** — Most contributors want what's best for the project
- **Keep it constructive** — Critique ideas, not people
- **Help others learn** — If someone makes a mistake, help them understand why

---

## 🧭 Ways to Contribute

You don't have to write code to contribute. Every contribution type is valued equally.

| Contribution Type | Description | Ideal For |
|-------------------|-------------|-----------|
| 🐛 **Bug Reports** | Report issues you encounter while using Tellr | Everyone |
| 💡 **Feature Ideas** | Suggest new capabilities or improvements | Power users |
| 📝 **Documentation** | Improve README, fix typos, add examples | Writers |
| 🌐 **Translations** | Add language support for the UI | Multilingual users |
| 🎨 **UI/UX** | Improve the visual design or user experience | Designers |
| 💻 **Code** | Fix bugs, add features, refactor | Developers |
| ✅ **Testing** | Test on different OS/microphone setups | QA contributors |

---

## 🛠️ Development Setup

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/downloads)
- **Groq API key** — [Get one free](https://console.groq.com/keys) (for testing transcription)

### One-Time Setup

```bash
# 1. Fork the repository
#    Click "Fork" at https://github.com/kartikpawar/tellr

# 2. Clone your fork locally
git clone https://github.com/YOUR-USERNAME/tellr.git
cd tellr

# 3. Add the upstream remote (to sync with main repo later)
git remote add upstream https://github.com/kartikpawar/tellr.git

# 4. Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create your .env file (copy from template, never commit real keys)
copy .env.example .env          # Windows
cp .env.example .env            # macOS / Linux
```

### Verify It Works

```bash
python tellr_app.py
```

The Tellr GUI should appear. If it doesn't, check the error output and ensure all dependencies are installed.

### Syncing Your Fork

Before starting new work, sync your fork with the upstream repository:

```bash
git checkout main
git pull upstream main
git push origin main
```

---

## 📁 Project Structure

```
tellr/
├── tellr_app.py          # Main application — UI, system tray, hotkey, orchestration
├── recorder.py           # Audio capture — 16kHz mono PCM via sounddevice
├── transcriber.py        # Groq cloud transcription — HTTP multipart API client
├── settings.py           # Settings persistence — JSON config management
│
├── run.bat               # Windows one-click launcher
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Package metadata and build configuration
│
├── .env.example          # Environment variable template
├── .gitignore            # Git exclusion rules
│
├── README.md             # Project documentation
├── CONTRIBUTING.md       # This file
├── HANDOVER.md           # Developer architecture documentation
├── LICENSE               # MIT License
│
├── tellr/                # Python package
│   └── __init__.py
│
├── src/                  # Tauri v2 frontend (alternative backend)
├── src-tauri/            # Rust/Tauri v2 backend (alternative backend)
```

---

## 📐 Coding Standards

### Python Style Guide

- Follow **PEP 8** conventions
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **100 characters**
- Use **type hints** for all function signatures
- Write **docstrings** for all public functions, classes, and methods

### Type Hints

Use Python 3.10+ modern syntax:

```python
# ✅ Correct — modern union syntax
def process(audio: bytes | None) -> str | None:

# ❌ Avoid — deprecated typing syntax
from typing import Optional
def process(audio: Optional[bytes]) -> Optional[str]:
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Variables & functions | `snake_case` | `_set_clipboard_text()` |
| Classes | `PascalCase` | `TellrApp` |
| Constants | `UPPER_SNAKE` | `SAMPLE_RATE = 16000` |
| Private members | `_leading_underscore` | `self._recording` |
| Module-level private | `__double_underscore` | `__m_seq` (XOR-protected data) |

### Logging

Use the project's structured logging instead of `print()`:

```python
import logging
logger = logging.getLogger("tellr.module_name")

logger.info("Operation completed")      # Normal operations
logger.warning("Degraded state...")      # Non-critical issues
logger.error("Operation failed: ...")    # Failures
```

### Error Handling

```python
# ✅ Correct — specific exception types
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid input: {e}")
except OSError as e:
    logger.error(f"System error: {e}")

# ❌ Avoid — bare except
try:
    ...
except:
    pass
```

### Thread Safety

Tellr uses background threads for recording and transcription. When updating the GUI from a thread:

```python
# ✅ Correct — schedule on main thread
self.root.after(0, lambda: self._set_status(STATE_DONE))

# ❌ Avoid — direct tkinter calls from background threads
self.status_label.configure(text="Done")  # Will crash on macOS/Linux
```

---

## 🔄 Pull Request Process

### Step-by-Step

```bash
# 1. Create a new branch for your feature/fix
git checkout -b feature/my-feature
#    Use a descriptive name: fix/hotkey-crash, feat/language-add, docs/typo

# 2. Make your changes

# 3. Test your changes
python tellr_app.py

# 4. Stage and commit
git add .
git commit -m "feat: add support for Turkish language"

# 5. Push to your fork
git push origin feature/my-feature

# 6. Open a Pull Request
#    Go to https://github.com/kartikpawar/tellr and click "Compare & Pull Request"
```

### PR Checklist

Before submitting, verify:

- [ ] Code compiles and runs without errors
- [ ] All existing features still work (tested manually)
- [ ] New code follows the project's coding standards
- [ ] Type hints are added for new functions
- [ ] Docstrings are written for new public APIs
- [ ] No `print()` statements — use `logger` instead
- [ ] No `from typing import Optional` — use `X | None` syntax
- [ ] Thread safety is considered (no tkinter calls from background threads)
- [ ] Commit messages follow the [conventional format](#commit-message-format)

### PR Title Format

Use descriptive titles:

```
✅ feat: add Turkish language support
✅ fix: crash when microphone is disconnected
✅ docs: update API key instructions in README
✅ refactor: simplify recorder fallback logic
✅ test: add edge case for empty transcription
```

### What Happens After

| Step | Who | What |
|------|-----|------|
| 1 | Automated checks | Lint and basic validation run |
| 2 | Maintainer review | Code review within 3-5 business days |
| 3 | You | Address feedback, push updates |
| 4 | Maintainer | Final approval and merge |

---

## 💬 Commit Guidelines

### Commit Message Format

```
type(scope): short description

Optional longer body explaining the why, not the what.
Separated by a blank line from the subject.
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons, etc. (no code change) |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |

### Examples

```
feat(lang): add Turkish language support

Added 'tr' to the language dropdown with proper Unicode display.
Tested with Groq whisper-large-v3 — works correctly.
```

```
fix(clipboard): prevent crash when called from background thread

Moved clipboard operations to main thread via root.after()
to avoid tkinter thread-safety violation on macOS.
```

---

## 🐛 Issue Reporting

### Before Reporting

1. **Search existing issues** — Your bug may already be reported or fixed
2. **Try the latest version** — The issue may have been resolved
3. **Check the console** — Run `python tellr_app.py` from terminal and look for error logs

### Bug Report Template

When opening a bug report, include:

```markdown
**Describe the bug**
A clear and concise description of what happened.

**To Reproduce**
Steps to reproduce the behavior:
1. Open Tellr
2. Click on '...'
3. Press '....'
4. See error

**Expected behavior**
What you expected to happen instead.

**Screenshots / Logs**
If applicable, paste error output from the terminal.

**Environment (please complete):**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 24.04]
- Python version: [e.g., 3.12.3]
- Tellr version: [e.g., 1.0.0]
- Microphone: [e.g., built-in, USB headset]

**Additional context**
Any other context about the problem.
```

---

## 💡 Feature Requests

Feature requests are welcome. To submit one:

1. **Search existing issues** — Your idea may already be discussed
2. **Open a new issue** with the label `enhancement`
3. **Describe the problem** your feature would solve, not just the solution
4. **Explain why** it would benefit other users, not just your use case

Good feature request:

> *"Auto-detect the system's default input device on launch instead of defaulting to 'default'. This would help users who frequently switch between headsets and built-in microphones."*

---

## 👀 Review Process

### What Reviewers Look For

- **Correctness** — Does the code do what it claims?
- **Safety** — Are there thread safety issues, resource leaks, or crash risks?
- **Simplicity** — Is there a simpler way to achieve the same result?
- **Consistency** — Does the code match the project's existing patterns?
- **Testability** — Can the change be verified?

### If Your PR Needs Changes

Don't worry — this is normal. Address the feedback, push updates to the same branch, and the PR updates automatically. Use `--force-with-lease` if you need to rebase:

```bash
git checkout feature/my-feature
# Make changes
git add .
git commit -m "fix: address review feedback"
git push origin feature/my-feature
```

### Merge Criteria

A PR is merged when:

- ✅ At least one maintainer has approved
- ✅ All automated checks pass
- ✅ No unresolved review comments
- ✅ The change is backwards-compatible (or a major version bump is justified)

---

## ❓ Getting Help

| Resource | Where |
|----------|-------|
| **Documentation** | [`README.md`](README.md) |
| **Bug Reports** | [GitHub Issues](https://github.com/kartikpawar/tellr/issues) |
| **Feature Ideas** | [GitHub Discussions](https://github.com/kartikpawar/tellr/discussions) |
| **Quick Questions** | Open a discussion with the `Q&A` label |

If you're stuck on a contribution, open a **draft pull request** with what you have so far and ask for guidance. We're happy to help.

---

## 🙏 Thank You

Every contribution — whether it's a typo fix, a new feature, or just a bug report — makes Tellr better for everyone. The time and effort you put into contributing is genuinely appreciated.

**Happy coding. Speak freely.**

— *Kartik Pawar*

---

<div align="center">
  <a href="README.md">⬆ Back to README</a> &nbsp;|&nbsp;
  <a href="LICENSE">📄 License</a>
</div>
