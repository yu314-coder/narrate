"""Chatterbox TTS engine — 500M params, high quality, emotion control.

Install: pip install narrate[chatterbox]
"""

import numpy as np

from narrate.engines.base import TTSEngine
from narrate.engines import register

_model_instance = None


class ChatterboxEngine(TTSEngine):
    name = "chatterbox"

    _VOICES = [
        {"id": "default", "name": "Default", "description": "Chatterbox default voice"},
    ]

    def _get_model(self):
        global _model_instance
        if _model_instance is None:
            from chatterbox.tts import ChatterboxTTS
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
            _model_instance = ChatterboxTTS.from_pretrained(device=device)
        return _model_instance

    def synthesize(self, text, voice="default", speed=1.0, emotion=0.0):
        model = self._get_model()

        # Chatterbox uses exaggeration parameter for emotion (0.0 = neutral, 1.0 = max)
        wav = model.generate(
            text,
            exaggeration=emotion,
        )

        # wav is a torch tensor, convert to numpy
        if hasattr(wav, "numpy"):
            samples = wav.squeeze().cpu().numpy()
        else:
            samples = np.array(wav).squeeze()

        sr = 24000  # Chatterbox outputs at 24kHz
        return samples, sr

    def list_voices(self):
        return self._VOICES

    def is_available(self):
        try:
            import chatterbox  # noqa: F401
            return True
        except ImportError:
            return False


register("chatterbox", ChatterboxEngine)
