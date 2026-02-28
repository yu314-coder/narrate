"""Audio playback utilities."""

import numpy as np


def play_audio(samples: np.ndarray, sample_rate: int):
    """Play audio samples through the default output device.

    Requires: pip install narrate[play]
    """
    try:
        import sounddevice as sd
        sd.play(samples, samplerate=sample_rate)
        sd.wait()
    except ImportError:
        raise RuntimeError(
            "Audio playback requires sounddevice. "
            "Install with: pip install narrate[play]"
        )


def save_audio(samples: np.ndarray, sample_rate: int, path: str):
    """Save audio samples to a WAV file."""
    import soundfile as sf
    sf.write(path, samples, sample_rate)
