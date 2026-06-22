import io
import logging
import wave
import threading

import numpy as np
import sounddevice as sd

logger = logging.getLogger("speakr.recorder")

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "int16"


class Recorder:
    """Records 16 kHz mono 16-bit PCM audio from the selected microphone."""

    def __init__(self, device: int | str | None = None):
        self.device = self._resolve_device(device) if isinstance(device, str) else device
        self._recording: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None
        self._lock = threading.Lock()
        self._is_recording = False

    @staticmethod
    def _resolve_device(device_name: str) -> int | None:
        """Resolve a device name string to a sounddevice device ID."""
        if not device_name or device_name == "default":
            return None
        try:
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if dev["max_input_channels"] > 0 and dev["name"] == device_name:
                    return i
            # Try partial match
            for i, dev in enumerate(devices):
                if dev["max_input_channels"] > 0 and device_name.lower() in dev["name"].lower():
                    return i
        except Exception as e:
            logger.warning(f"Device resolution error: {e}")
        return None

    @classmethod
    def from_name(cls, device_name: str) -> "Recorder":
        """Create a Recorder from a device name string."""
        return cls(device=device_name)

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def start(self) -> None:
        if self._is_recording:
            return
        self._recording = []
        self._is_recording = True

        def callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"Audio stream status: {status}")
            with self._lock:
                self._recording.append(indata.copy())

        # Try configured device first, fall back to default
        devices_to_try = [self.device, None] if self.device is not None else [None]
        last_error = None
        for dev in devices_to_try:
            try:
                self._stream = sd.InputStream(
                    samplerate=SAMPLE_RATE,
                    channels=CHANNELS,
                    dtype=DTYPE,
                    device=dev,
                    callback=callback,
                )
                self._stream.start()
                self.device = dev
                return  # Success
            except Exception as e:
                last_error = e
                self._recording = []
                logger.warning(f"Recorder start failed (device={dev}): {e}")
                # Fall through to try next device

        # All attempts failed
        self._is_recording = False
        self._stream = None
        logger.error(f"Could not start recording on any device: {last_error}")

    def stop(self) -> bytes | None:
        """Stop recording and return WAV bytes. Returns None if nothing was recorded."""
        if not self._is_recording:
            return None
        self._is_recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        with self._lock:
            if not self._recording:
                return None
            audio = np.concatenate(self._recording, axis=0)

        # Write to WAV in memory
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio.tobytes())
        return buf.getvalue()

    @staticmethod
    def list_devices() -> list[dict]:
        """Return a list of available input devices."""
        devices = sd.query_devices()
        inputs = []
        for i, dev in enumerate(devices):
            if dev["max_input_channels"] > 0:
                inputs.append({"id": i, "name": dev["name"]})
        return inputs
