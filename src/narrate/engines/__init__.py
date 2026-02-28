"""TTS engine registry."""

from narrate.engines.base import TTSEngine

_registry: dict[str, type[TTSEngine]] = {}


def register(name: str, cls: type[TTSEngine]):
    _registry[name] = cls


def get_engine(name: str) -> TTSEngine:
    if name not in _registry:
        _try_import(name)
    if name not in _registry:
        raise RuntimeError(
            f"Engine '{name}' not available. "
            f"Install it with: pip install narrate[{name}]"
        )
    return _registry[name]()


def available_engines() -> list[str]:
    for name in ("kokoro", "chatterbox"):
        if name not in _registry:
            _try_import(name)
    return [name for name, cls in _registry.items() if cls().is_available()]


def _try_import(name: str):
    """Attempt to import an engine module, registering it if available."""
    try:
        if name == "kokoro":
            from narrate.engines import kokoro_engine  # noqa: F401
        elif name == "chatterbox":
            from narrate.engines import chatterbox_engine  # noqa: F401
    except ImportError:
        pass
