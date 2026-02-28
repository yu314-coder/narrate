"""Core narrate() function and configuration."""

import os

from narrate.engines import get_engine, available_engines

# ── Global defaults ──
_default_engine: str = ""
_default_voice: str = ""
_auto_play: bool = True
_output_dir: str = ""


def set_engine(name: str):
    """Set the default TTS engine ('kokoro' or 'chatterbox')."""
    global _default_engine
    _default_engine = name


def set_voice(voice: str):
    """Set the default voice ID."""
    global _default_voice
    _default_voice = voice


def list_engines() -> list[str]:
    """Return names of available (installed) engines."""
    return available_engines()


def list_voices(engine: str = "") -> list[dict]:
    """List available voices for an engine."""
    name = engine or _resolve_engine()
    eng = get_engine(name)
    return eng.list_voices()


def narrate(
    text: str,
    *,
    engine: str = "",
    voice: str = "",
    speed: float = 1.0,
    emotion: float = 0.0,
    output: str = "",
    play: bool | None = None,
) -> str:
    """Generate speech from text.

    Args:
        text: The text to speak.
        engine: TTS engine to use ('kokoro' or 'chatterbox').
                Defaults to the first available engine.
        voice: Voice ID. Each engine has its own set of voices.
        speed: Speech speed multiplier (default 1.0).
        emotion: Emotion intensity 0.0-1.0 (Chatterbox only).
        output: Path to save WAV file. If empty, uses a temp file.
        play: Whether to play audio. Defaults to True unless output is set.

    Returns:
        Path to the generated WAV file.
    """
    # Resolve engine
    engine_name = engine or _resolve_engine()
    eng = get_engine(engine_name)

    # Resolve voice
    voice_id = voice or _default_voice
    if not voice_id:
        voices = eng.list_voices()
        voice_id = voices[0]["id"] if voices else ""

    # Generate audio
    samples, sr = eng.synthesize(
        text, voice=voice_id, speed=speed, emotion=emotion
    )

    # Determine output path
    if not output:
        if _output_dir:
            os.makedirs(_output_dir, exist_ok=True)
            output = os.path.join(_output_dir, _make_filename(text))
        else:
            import tempfile
            fd, output = tempfile.mkstemp(suffix=".wav", prefix="narrate_")
            os.close(fd)

    # Save to file
    from narrate.player import save_audio
    save_audio(samples, sr, output)

    # Play audio
    should_play = play if play is not None else _auto_play
    if should_play:
        try:
            from narrate.player import play_audio
            play_audio(samples, sr)
        except RuntimeError:
            pass  # sounddevice not installed, skip playback

    return output


def _resolve_engine() -> str:
    """Pick the best available engine."""
    if _default_engine:
        return _default_engine

    engines = available_engines()
    if not engines:
        raise RuntimeError(
            "No TTS engine installed. Install one with:\n"
            "  pip install narrate[kokoro]      (82M, fast, CPU)\n"
            "  pip install narrate[chatterbox]  (500M, high quality)\n"
            "  pip install narrate[all]         (both engines)"
        )
    # Prefer kokoro (lighter) if both available
    if "kokoro" in engines:
        return "kokoro"
    return engines[0]


def _make_filename(text: str) -> str:
    """Generate a filename from text."""
    import hashlib
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    slug = "".join(c if c.isalnum() else "_" for c in text[:30]).strip("_")
    return f"narrate_{slug}_{h}.wav"
