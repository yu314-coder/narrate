"""Abstract base class for TTS engines."""

from abc import ABC, abstractmethod


class TTSEngine(ABC):
    """Base class all TTS engines must implement."""

    name: str = ""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice: str = "",
        speed: float = 1.0,
        emotion: float = 0.0,
    ) -> tuple:
        """Generate speech audio from text.

        Returns:
            (samples, sample_rate): numpy array of audio samples and the sample rate.
        """
        ...

    @abstractmethod
    def list_voices(self) -> list[dict]:
        """Return available voices as [{id, name, description}, ...]."""
        ...

    def is_available(self) -> bool:
        """Check if this engine's dependencies are installed."""
        return True
