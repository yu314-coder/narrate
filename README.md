# narrate

Local text-to-speech with multiple engine support.

## Install

```bash
pip install narrate[kokoro]       # Kokoro 82M — fast, runs on CPU
pip install narrate[chatterbox]   # Chatterbox 500M — high quality, emotion control
pip install narrate[all]          # Both engines + audio playback
```

## Usage

```python
from narrate import narrate

# Uses the best available engine automatically
narrate("Hello world")

# Choose engine, voice, speed
narrate("Hello world", engine="kokoro", voice="af_heart", speed=1.2)

# Chatterbox with emotion control (0.0 = neutral, 1.0 = expressive)
narrate("Hello world", engine="chatterbox", emotion=0.8)

# Save to file without playing
narrate("Hello world", output="hello.wav", play=False)
```

## Engines

| Engine | Params | Speed | Quality | Features |
|--------|--------|-------|---------|----------|
| Kokoro | 82M | Fast (CPU) | Good | 9 voices, speed control |
| Chatterbox | 500M | Moderate | Excellent | Emotion control, voice cloning |

## License

MIT
