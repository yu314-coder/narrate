"""Kokoro ONNX TTS engine — 82M params, fast, runs on CPU.

Install: pip install narrate[kokoro]
"""

import os

from narrate.engines.base import TTSEngine
from narrate.engines import register

_kokoro_instance = None

# Model file URLs (from kokoro-onnx GitHub releases)
_MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
_VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
_MODEL_DIR = os.path.join(os.path.expanduser("~"), ".cache", "narrate", "kokoro")


def _download_file(url: str, dest: str):
    """Download a file with progress."""
    import urllib.request

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    filename = os.path.basename(dest)
    print(f"[narrate] Downloading {filename}...")
    urllib.request.urlretrieve(url, dest)
    size_mb = os.path.getsize(dest) / (1024 * 1024)
    print(f"[narrate] Downloaded {filename} ({size_mb:.1f} MB)")


def _ensure_models() -> tuple[str, str]:
    """Ensure model files exist, downloading if needed."""
    model_path = os.path.join(_MODEL_DIR, "kokoro-v1.0.onnx")
    voices_path = os.path.join(_MODEL_DIR, "voices-v1.0.bin")

    if not os.path.isfile(model_path):
        _download_file(_MODEL_URL, model_path)
    if not os.path.isfile(voices_path):
        _download_file(_VOICES_URL, voices_path)

    return model_path, voices_path


class KokoroEngine(TTSEngine):
    name = "kokoro"

    _VOICES = [
        {"id": "af_heart", "name": "Heart", "description": "Female, warm"},
        {"id": "af_bella", "name": "Bella", "description": "Female, clear"},
        {"id": "af_nicole", "name": "Nicole", "description": "Female, professional"},
        {"id": "af_sarah", "name": "Sarah", "description": "Female, soft"},
        {"id": "af_sky", "name": "Sky", "description": "Female, bright"},
        {"id": "am_adam", "name": "Adam", "description": "Male, deep"},
        {"id": "am_michael", "name": "Michael", "description": "Male, natural"},
        {"id": "bf_emma", "name": "Emma", "description": "British female"},
        {"id": "bm_george", "name": "George", "description": "British male"},
    ]

    def _get_kokoro(self):
        global _kokoro_instance
        if _kokoro_instance is None:
            import kokoro_onnx

            model_path, voices_path = _ensure_models()
            _kokoro_instance = kokoro_onnx.Kokoro(model_path, voices_path)
        return _kokoro_instance

    def synthesize(self, text, voice="af_heart", speed=1.0, emotion=0.0):
        kokoro = self._get_kokoro()
        samples, sr = kokoro.create(text, voice=voice, speed=speed)
        return samples, sr

    def list_voices(self):
        return self._VOICES

    def is_available(self):
        try:
            import kokoro_onnx  # noqa: F401
            import soundfile  # noqa: F401
            return True
        except ImportError:
            return False


register("kokoro", KokoroEngine)
