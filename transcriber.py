import time

import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
MODEL = "whisper-large-v3"


class Transcriber:
    """Transcribes audio via Groq's cloud Whisper API."""

    def __init__(self, api_key: str, language: str | None = None):
        self.api_key = api_key
        self.language = language

    def transcribe(self, audio_wav: bytes) -> str | None:
        """Send WAV audio bytes to Groq and return the transcribed text."""
        if not self.api_key:
            raise ValueError("Groq API key is not set")

        files = {"file": ("recording.wav", audio_wav, "audio/wav")}
        data = {"model": MODEL, "response_format": "json"}
        if self.language:
            data["language"] = self.language

        headers = {"Authorization": f"Bearer {self.api_key}"}

        for attempt in range(3):
            try:
                resp = requests.post(
                    GROQ_API_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30,
                )
                resp.raise_for_status()
                result = resp.json()
                return result.get("text", "").strip()
            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(1)
                    continue
                raise
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"Transcription failed: {e}") from e
