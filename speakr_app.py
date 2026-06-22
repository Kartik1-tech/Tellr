"""
Speakr - Lightweight desktop dictation app.
CustomTkinter UI + system tray + global hotkey + Groq transcription + auto-paste.
"""

import logging
import os
import queue
import sys
import threading
import tkinter as tk

logger = logging.getLogger("speakr")

import customtkinter as ctk
import pystray
from PIL import Image, ImageDraw
from pynput import keyboard

from recorder import Recorder
from settings import Settings, _app_tag
from transcriber import Transcriber

# ── Constants ──────────────────────────────────────────────────────────

APP_NAME = "Speakr"
APP_VERSION = "1.0.0"
DEFAULT_WIN_SIZE = "440x580"
POLL_INTERVAL_MS = 100

# Resolve attribution at runtime (never stored as plaintext in source)
_APP_CREDIT = _app_tag()

# States for the status indicator
STATE_IDLE = "idle"
STATE_RECORDING = "recording"
STATE_TRANSCRIBING = "transcribing"
STATE_DONE = "done"
STATE_ERROR = "error"

STATUS_COLORS = {
    STATE_IDLE: ("Idle", "#4a9eff"),
    STATE_RECORDING: ("Recording...", "#ff4a4a"),
    STATE_TRANSCRIBING: ("Transcribing...", "#ffaa2a"),
    STATE_DONE: ("Done!", "#4aff4a"),
    STATE_ERROR: ("Error", "#ff4a4a"),
}

# ── Cross-platform clipboard (tkinter, built-in, zero extra deps) ──────


def _set_clipboard_text(text: str) -> None:
    """Copy text to system clipboard via tkinter (Win/macOS/Linux, no deps)."""
    root = tk.Tk()
    root.withdraw()
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
    finally:
        root.destroy()


def _simulate_paste() -> None:
    """Simulate Paste (Ctrl+V on Win/Linux, Cmd+V on macOS) using pynput."""
    mod = keyboard.Key.cmd if sys.platform == "darwin" else keyboard.Key.ctrl
    kbc = keyboard.Controller()
    kbc.press(mod)
    kbc.press("v")
    kbc.release("v")
    kbc.release(mod)


# ── Tray icon ──────────────────────────────────────────────────────────

def _create_tray_image() -> Image.Image:
    """Generate a microphone icon for the system tray."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Mic body (rounded rect)
    draw.rounded_rectangle([20, 8, 44, 36], radius=6, fill="#4a9eff")
    # Mic stem
    draw.rectangle([26, 36, 38, 48], fill="#4a9eff")
    # Mic base
    draw.rounded_rectangle([16, 44, 48, 56], radius=4, fill="#4a9eff")
    return img


# ── Toast overlay ──────────────────────────────────────────────────────
class Toast:
    """Simple non-blocking toast notification overlay."""

    def __init__(self, parent, text: str, duration_ms: int = 2000):
        self.parent = parent
        self.duration = duration_ms
        self.fade_id = None

        x = parent.winfo_x() + (parent.winfo_width() // 2) - 100
        y = parent.winfo_y() + parent.winfo_height() - 80

        self.win = ctk.CTkToplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-transparentcolor", "#000001")
        self.win.geometry(f"200x36+{x}+{y}")
        self.win.configure(fg_color="#000001")

        self.label = ctk.CTkLabel(
            self.win, text=text,
            font=ctk.CTkFont(size=12),
            text_color="#e0e0e0",
            fg_color="#2a2a2a",
            corner_radius=8,
            padx=16, pady=6,
        )
        self.label.pack(fill="both", expand=True)

        # Auto-close
        self.parent.after(duration_ms, self._fade_out)
        self.parent.after(100, self._reposition)

    def _reposition(self):
        try:
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 100
            y = self.parent.winfo_y() + self.parent.winfo_height() - 80
            self.win.geometry(f"200x36+{x}+{y}")
        except Exception:
            pass

    def _fade_out(self):
        try:
            self.win.destroy()
        except Exception:
            pass


# ── Main Application ──────────────────────────────────────────────────

class SpeakrApp:
    """Main application controller."""

    def __init__(self) -> None:
        self.settings = Settings.load()
        self.recording = False
        self.cmd_queue: queue.Queue[str] = queue.Queue()
        self._captured_hotkey_raw: str | None = None

        # Initialize with saved settings right away
        self.recorder: Recorder | None = self._init_recorder_from_settings()
        self.transcriber: Transcriber | None = self._init_transcriber_from_settings()

        self._build_ui()
        self._build_tray()
        self._start_hotkey_listener()
        self._poll_queue()

    def _init_recorder_from_settings(self) -> Recorder | None:
        """Create Recorder from saved settings."""
        mic = self.settings.microphone
        if mic and mic != "default":
            return Recorder.from_name(mic)
        return Recorder()

    def _init_transcriber_from_settings(self) -> Transcriber | None:
        """Create Transcriber from saved settings."""
        api_key = self.settings.api_key.strip()
        if api_key:
            return Transcriber(api_key, self.settings.language or None)
        return None

    # ── UI ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry(DEFAULT_WIN_SIZE)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._minimize_to_tray)

        # ── Header ──
        self.header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=24, pady=(24, 0))

        ctk.CTkLabel(
            self.header_frame, text=APP_NAME,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1a1a2e", "#e0e0e0"),
        ).pack(side="left")

        # Status dot + label
        self.status_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.status_frame.pack(side="right")

        self.status_dot = ctk.CTkFrame(self.status_frame, width=14, height=14,
                                        corner_radius=7, fg_color=STATUS_COLORS[STATE_IDLE][1])
        self.status_dot.pack(side="left", padx=(0, 6))
        self.status_dot.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_frame, text=STATUS_COLORS[STATE_IDLE][0],
            font=ctk.CTkFont(size=13),
        )
        self.status_label.pack(side="left")

        self._status_pulse_job = None

        # ── Settings form ──
        self.form = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.form.pack(fill="both", expand=True, padx=24, pady=(16, 0))

        # --- Section: Transcription ---
        ctk.CTkLabel(
            self.form, text="Transcription",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#888888",
        ).pack(anchor="w", pady=(0, 6))

        self.transcription_textbox = ctk.CTkTextbox(
            self.form, height=80,
            font=ctk.CTkFont(size=13),
            fg_color="#1e1e1e",
            border_width=1,
            border_color="#333333",
            wrap="word",
        )
        self.transcription_textbox.pack(fill="x", pady=(0, 4))
        self.transcription_textbox.insert("0.0", "Transcribed text will appear here...")
        self.transcription_textbox.configure(state="disabled")

        clear_btn = ctk.CTkButton(
            self.form, text="Clear",
            command=self._clear_transcription,
            width=60, height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#333333",
            hover_color="#444444",
            text_color="#aaaaaa",
        )
        clear_btn.pack(anchor="e", pady=(0, 12))

        # Separator
        ctk.CTkFrame(self.form, height=1, fg_color="#333333").pack(fill="x", pady=(0, 12))

        # --- Section: Input ---
        ctk.CTkLabel(
            self.form, text="Input",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#888888",
        ).pack(anchor="w", pady=(0, 6))

        # Microphone
        ctk.CTkLabel(self.form, text="Microphone",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.mic_var = ctk.StringVar(value=self.settings.microphone)
        self.mic_menu = ctk.CTkOptionMenu(self.form, variable=self.mic_var, values=["default"])
        self.mic_menu.pack(fill="x", pady=(0, 12))
        self._refresh_mic_list()

        # Language
        ctk.CTkLabel(self.form, text="Language",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.lang_var = ctk.StringVar(value=self.settings.language)
        languages = [
            ("Auto-detect", ""), ("English", "en"),
            ("Français (French)", "fr"), ("Español (Spanish)", "es"),
            ("Deutsch (German)", "de"), ("Italiano (Italian)", "it"),
            ("Português (Portuguese)", "pt"), ("Русский (Russian)", "ru"),
            ("العربية (Arabic)", "ar"), ("日本語 (Japanese)", "ja"),
            ("한국어 (Korean)", "ko"), ("中文 (Chinese)", "zh"),
            ("हिन्दी (Hindi)", "hi"), ("বাংলা (Bengali)", "bn"),
            ("தமிழ் (Tamil)", "ta"), ("తెలుగు (Telugu)", "te"),
            ("मराठी (Marathi)", "mr"), ("ગુજરાતી (Gujarati)", "gu"),
            ("ಕನ್ನಡ (Kannada)", "kn"), ("മലയാളം (Malayalam)", "ml"),
            ("ਪੰਜਾਬੀ (Punjabi)", "pa"), ("اردو (Urdu)", "ur"),
            ("ଓଡ଼ିଆ (Odia)", "or"), ("অসমীয়া (Assamese)", "as"),
            ("Nederlands (Dutch)", "nl"), ("Türkçe (Turkish)", "tr"),
            ("Polski (Polish)", "pl"),
        ]
        self.lang_menu = ctk.CTkOptionMenu(
            self.form, variable=self.lang_var,
            values=[label for label, _ in languages],
            command=self._on_language_change,
        )
        self.lang_menu.pack(fill="x", pady=(0, 12))
        self._lang_map = dict(languages)

        # Separator
        ctk.CTkFrame(self.form, height=1, fg_color="#333333").pack(fill="x", pady=(0, 12))

        # --- Section: Service ---
        ctk.CTkLabel(
            self.form, text="Service",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#888888",
        ).pack(anchor="w", pady=(0, 6))

        # API Key
        ctk.CTkLabel(self.form, text="Groq API Key",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.api_key_entry = ctk.CTkEntry(self.form, placeholder_text="gsk_...", show="*")
        self.api_key_entry.pack(fill="x", pady=(0, 12))
        self.api_key_entry.insert(0, self.settings.api_key)

        # Hotkey display
        ctk.CTkLabel(self.form, text="Global Hotkey",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 4))
        hotkey_row = ctk.CTkFrame(self.form, fg_color="transparent")
        hotkey_row.pack(fill="x", pady=(0, 12))
        self.hotkey_var = ctk.StringVar(value=self._hotkey_display(self.settings.hotkey))
        self.hotkey_entry = ctk.CTkEntry(hotkey_row, textvariable=self.hotkey_var, state="readonly")
        self.hotkey_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.change_hotkey_btn = ctk.CTkButton(
            hotkey_row, text="Change",
            command=self._start_hotkey_capture,
            width=70, height=30,
            font=ctk.CTkFont(size=11),
            fg_color="#333333", hover_color="#444444",
            text_color="#cccccc",
        )
        self.change_hotkey_btn.pack(side="right")

        # ── Save ──
        self.save_btn = ctk.CTkButton(
            self.root, text="Save Settings", command=self._save_settings,
            height=40, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3a86ff",
            hover_color="#2d6bcc",
        )
        self.save_btn.pack(fill="x", padx=24, pady=(8, 4))

        # ── Footer attribution ──
        footer_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=20)
        footer_frame.pack(fill="x", padx=24, pady=(0, 12))
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame, text=f"{APP_NAME} v{APP_VERSION}",
            font=ctk.CTkFont(size=9),
            text_color="#555555",
        ).pack(side="left")

        ctk.CTkLabel(
            footer_frame, text=f"Built by {_APP_CREDIT}",
            font=ctk.CTkFont(size=9),
            text_color="#444444",
        ).pack(side="right")

        # ── Hotkey binding for capture ──
        self.root.bind("<KeyPress>", self._on_key_press, add="+")
        self._capturing_hotkey = False
        self._captured_keys: list[str] = []

    def _clear_transcription(self):
        try:
            self.transcription_textbox.configure(state="normal")
            self.transcription_textbox.delete("0.0", "end")
            self.transcription_textbox.configure(state="disabled")
        except Exception:
            pass

    def _hotkey_display(self, raw: str) -> str:
        """Convert pynput hotkey format to human-readable."""
        cmd_label = "Cmd" if sys.platform == "darwin" else "Win"
        mapping = {
            "<ctrl>": "Ctrl", "<shift>": "Shift", "<alt>": "Alt",
            "<cmd>": cmd_label, "<space>": "Space",
        }
        parts = raw.split("+")
        display = []
        for p in parts:
            p = p.strip()
            display.append(mapping.get(p, p.strip("<>").title() if p.startswith("<") else p.upper()))
        return " + ".join(display)

    def _on_language_change(self, label: str) -> None:
        """Map language label back to code."""
        pass  # value stored via self.lang_var, mapped on save

    def _refresh_mic_list(self) -> None:
        """Populate microphone dropdown from sounddevice."""
        try:
            devices = Recorder.list_devices()
            names = [d["name"] for d in devices]
            self.mic_menu.configure(values=names)
            # Try to keep current selection
            if self.settings.microphone in names:
                self.mic_var.set(self.settings.microphone)
            elif names:
                self.mic_var.set(names[0])
        except Exception as e:
            logger.warning(f"Could not list audio devices: {e}")

    # ── Key capture for hotkey ──

    def _on_key_press(self, event) -> None:
        if not self._capturing_hotkey:
            return
        # Ignore lone modifier presses
        if event.keysym in ("Control_L", "Control_R", "Shift_L", "Shift_R",
                            "Alt_L", "Alt_R", "Super_L", "Super_R"):
            if event.keysym not in self._captured_keys:
                self._captured_keys.append(event.keysym)
            return
        # Escape/Tab/Return cancels capture
        if event.keysym in ("Escape", "Tab", "Return"):
            self._finish_hotkey_capture()
            return
        # Regular key — add it and finish capture immediately
        sym = event.keysym.lower()
        if sym not in [k.lower() for k in self._captured_keys]:
            self._captured_keys.append(sym)
        self._finish_hotkey_capture()

    def _start_hotkey_capture(self) -> None:
        self._capturing_hotkey = True
        self._captured_keys = []
        self.change_hotkey_btn.configure(text="Listening...", state="disabled")
        self.hotkey_entry.configure(state="normal")
        self.hotkey_entry.delete(0, "end")
        self.hotkey_entry.insert(0, "Press shortcut...")
        self.hotkey_entry.configure(state="readonly")

    def _finish_hotkey_capture(self) -> None:
        self._capturing_hotkey = False
        self.change_hotkey_btn.configure(text="Change", state="normal")
        if not self._captured_keys:
            self.hotkey_var.set(self._hotkey_display(self.settings.hotkey))
            return
        # Build pynput format
        parts = []
        for k in self._captured_keys:
            k_lower = k.lower()
            if "control" in k_lower:
                parts.append("<ctrl>")
            elif "shift" in k_lower:
                parts.append("<shift>")
            elif "alt" in k_lower:
                parts.append("<alt>")
            elif "super" in k_lower:
                parts.append("<cmd>")
            else:
                # Single char or special
                if len(k) == 1:
                    parts.append(k_lower)
                else:
                    parts.append(f"<{k_lower}>")
        # Deduplicate modifiers while preserving order
        seen = set()
        unique_parts = []
        for p in parts:
            if p not in seen:
                seen.add(p)
                unique_parts.append(p)
        raw = "+".join(unique_parts)
        self._captured_hotkey_raw = raw
        display = self._hotkey_display(raw)
        self.hotkey_var.set(display)

    # ── Settings ──

    def _save_settings(self) -> None:
        api_key = self.api_key_entry.get().strip()
        mic = self.mic_var.get()
        lang_label = self.lang_var.get()
        language = self._lang_map.get(lang_label, "")

        hotkey = self._captured_hotkey_raw if self._captured_hotkey_raw else self.settings.hotkey

        self.settings.api_key = api_key
        self.settings.microphone = mic
        self.settings.language = language
        self.settings.hotkey = hotkey
        self.settings.save()

        # Rebuild transcriber with new key
        self.transcriber = Transcriber(api_key, language or None) if api_key else None

        # Rebuild recorder with new device
        try:
            self.recorder = Recorder.from_name(mic) if mic and mic != "default" else Recorder()
        except Exception:
            self.recorder = Recorder()

        # Restart hotkey listener with new binding
        self._start_hotkey_listener()

        # Toast notification
        Toast(self.root, "Settings saved!")

    # ── System tray ────────────────────────────────────────────────────

    def _build_tray(self) -> None:
        img = _create_tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show Speakr", self._show_window, default=True),
            pystray.MenuItem("Quit", self._quit_from_tray),
        )
        self.tray = pystray.Icon(APP_NAME.lower(), img, APP_NAME, menu)
        threading.Thread(target=self.tray.run, daemon=True).start()

    def _minimize_to_tray(self) -> None:
        self.root.withdraw()

    def _show_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _quit_from_tray(self) -> None:
        """Called from pystray thread — marshal quit to main thread."""
        self.root.after(0, self._quit_app)

    def _quit_app(self) -> None:
        """Must run on main thread (tkinter operations)."""
        self.tray.stop()
        self.root.quit()
        self.root.destroy()
        os._exit(0)

    # ── Global hotkey ──────────────────────────────────────────────────

    def _start_hotkey_listener(self) -> None:
        # Stop existing listener if any
        if hasattr(self, "_hotkey_listener") and self._hotkey_listener:
            try:
                self._hotkey_listener.stop()
            except Exception:
                pass

        hotkey_str = self.settings.hotkey
        if not hotkey_str:
            logger.warning("No hotkey configured")
            return

        try:
            self._hotkey_listener = keyboard.GlobalHotKeys({hotkey_str: self._on_hotkey})
            self._hotkey_listener.start()
            logger.info(f"Hotkey listener started: {hotkey_str}")
        except Exception as e:
            logger.error(f"Failed to register hotkey '{hotkey_str}': {e}")
            # Try with a simpler hotkey as fallback
            try:
                fallback = "<ctrl>+<shift>+m"
                if fallback != hotkey_str:
                    logger.info(f"Trying fallback hotkey: {fallback}")
                    self._hotkey_listener = keyboard.GlobalHotKeys({fallback: self._on_hotkey})
                    self._hotkey_listener.start()
                    self.settings.hotkey = fallback
                    self.settings.save()
            except Exception as e2:
                logger.error(f"Fallback hotkey also failed: {e2}")
                self._hotkey_listener = None

    def _on_hotkey(self) -> None:
        """Called from pynput background thread. Queue the command."""
        logger.info("Hotkey triggered!")
        self.cmd_queue.put("toggle_recording")

    # ── Queue processing (runs on main thread) ─────────────────────────

    def _poll_queue(self) -> None:
        try:
            try:
                while True:
                    cmd = self.cmd_queue.get_nowait()
                    if cmd == "toggle_recording":
                        self._toggle_recording()
            except queue.Empty:
                pass
        except Exception as e:
            logger.error(f"Queue handler error: {e}")
        self.root.after(POLL_INTERVAL_MS, self._poll_queue)

    # ── Recording flow ─────────────────────────────────────────────────

    def _toggle_recording(self) -> None:
        if not self.recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self) -> None:
        if not self.recorder:
            self.recorder = self._init_recorder_from_settings()
        self.recording = True
        try:
            self.recorder.start()
            logger.info("Recording started...")
            self._set_status(STATE_RECORDING)
        except Exception as e:
            self.recording = False
            logger.error(f"Recording failed: {e}")
            self._set_status(STATE_ERROR, f"Mic error: {e}")

    def _stop_recording(self) -> None:
        self.recording = False
        self._set_status(STATE_TRANSCRIBING)

        if not self.recorder:
            self._set_status(STATE_IDLE)
            return

        try:
            audio = self.recorder.stop()
            if audio is None:
                logger.info("No audio recorded")
                self._set_status(STATE_IDLE)
                return
        except Exception as e:
            logger.error(f"Stop recording error: {e}")
            self._set_status(STATE_IDLE)
            return

        # Run transcription in background thread
        threading.Thread(target=self._do_transcribe, args=(audio,), daemon=True).start()

    def _paste_transcription(self, text: str) -> None:
        """Set clipboard and simulate paste — MUST run on main thread (tkinter)."""
        _set_clipboard_text(text)
        _simulate_paste()

    def _do_transcribe(self, audio: bytes) -> None:
        if not self.transcriber:
            self.transcriber = self._init_transcriber_from_settings()

        if not self.transcriber:
            self.root.after(0, lambda: self._set_status(STATE_ERROR, "No API key set"))
            self.root.after(3000, lambda: self._set_status(STATE_IDLE))
            return

        try:
            text = self.transcriber.transcribe(audio)
            if text:
                logger.info(f"Transcribed: {text[:60]}...")
                # Clipboard + paste MUST run on main thread (tkinter is not thread-safe)
                self.root.after(0, lambda: self._paste_transcription(text))
                self.root.after(0, lambda: self._set_status(STATE_DONE))
                # Update transcription display
                self.root.after(0, lambda: self._update_transcription(text))
            else:
                logger.info("Empty transcription")
                self.root.after(0, lambda: self._set_status(STATE_IDLE))
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self.root.after(0, lambda: self._set_status(STATE_ERROR, str(e)))

        # Return to idle after a moment
        self.root.after(2000, lambda: self._set_status(STATE_IDLE))

    def _update_transcription(self, text: str) -> None:
        """Update the transcription textbox with new text."""
        try:
            self.transcription_textbox.configure(state="normal")
            self.transcription_textbox.delete("0.0", "end")
            self.transcription_textbox.insert("0.0", text)
            self.transcription_textbox.configure(state="disabled")
        except Exception:
            pass

    # ── Status display ─────────────────────────────────────────────────

    def _set_status(self, state: str, message: str | None = None) -> None:
        label, color = STATUS_COLORS.get(state, (state, "#ffffff"))
        display = message or label

        # Cancel any pending pulse animation
        if self._status_pulse_job:
            self.root.after_cancel(self._status_pulse_job)
            self._status_pulse_job = None

        self.status_label.configure(text=display)
        self.status_dot.configure(fg_color=color)

        if state == STATE_RECORDING:
            self._start_pulse(color)

    def _start_pulse(self, color: str) -> None:
        """Animate the status dot with a pulsing glow effect."""

        def pulse(step: int = 0) -> None:
            if not self.recording:
                return
            # Pulse between full opacity and dim by adjusting brightness
            factor = 0.4 + 0.6 * abs((step % 20) - 10) / 10
            r, g, b = self._hex_to_rgb(color)
            dim_color = f"#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}"
            self.status_dot.configure(fg_color=dim_color)
            self._status_pulse_job = self.root.after(50, lambda: pulse(step + 1))

        pulse()

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

    # ── Entry point ────────────────────────────────────────────────────

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[Speakr] %(levelname)s: %(message)s",
        force=True,
    )
    app = SpeakrApp()
    app.run()


if __name__ == "__main__":
    main()
