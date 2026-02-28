"""narrate — Local text-to-speech with Kokoro and Chatterbox engines.

Usage::

    from narrate import narrate

    # Quick TTS (uses default engine)
    narrate("Hello world")

    # Choose engine
    narrate("Hello world", engine="kokoro")
    narrate("Hello world", engine="chatterbox")

    # Save to file
    narrate("Hello world", output="hello.wav")

    # Adjust voice and speed
    narrate("Hello world", voice="af_heart", speed=1.2)

    # Chatterbox with emotion control
    narrate("Hello world", engine="chatterbox", emotion=0.8)
"""

__version__ = "0.1.0"

from narrate.core import narrate, set_engine, set_voice, list_voices, list_engines

__all__ = ["narrate", "set_engine", "set_voice", "list_voices", "list_engines"]
