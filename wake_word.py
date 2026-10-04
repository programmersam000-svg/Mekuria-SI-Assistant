"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Wake Word  — The Activation Layer               ║
╚══════════════════════════════════════════════════════════════╝
Optional wake word detection using openWakeWord.
When enabled, Mekuria only starts listening after hearing the
activation phrase.
"""

import sys
from typing import Optional

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np
from rich.console import Console

import config

console = Console()

_wakeword_model = None


def _get_model():
    """Lazy-load the openWakeWord model."""
    global _wakeword_model
    if _wakeword_model is None:
        try:
            from openwakeword.model import Model
            _wakeword_model = Model(
                wakeword_models=[config.WAKE_WORD_MODEL],
                inference_framework="onnx",
            )
            console.print(
                f"[cyan]Wake word model loaded: '{config.WAKE_WORD_MODEL}'[/cyan]"
            )
        except ImportError:
            console.print(
                "[yellow]openwakeword not installed. "
                "Run: pip install openwakeword[/yellow]"
            )
            return None
        except Exception as e:
            console.print(f"[yellow]Wake word init failed: {e}[/yellow]")
            return None
    return _wakeword_model


def wait_for_wake_word() -> bool:
    """
    Block until the wake word is detected.
    Returns True when the wake word is heard, False on error.

    Continuously streams audio chunks and feeds them to the
    openWakeWord model for real-time detection.
    """
    if not config.WAKE_WORD_ENABLED:
        return True  # Skip wake word if disabled

    model = _get_model()
    if model is None:
        console.print("[yellow]Wake word disabled (model not available). "
                      "Listening immediately.[/yellow]")
        return True

    console.print(
        f"[dim]Say '[bold]{config.WAKE_WORD_MODEL.replace('_', ' ')}[/bold]' "
        f"to wake me up...[/dim]"
    )

    import sounddevice as sd

    chunk_size = 1280  # ~80ms at 16kHz
    stream = sd.InputStream(
        samplerate=config.SAMPLE_RATE,
        channels=config.CHANNELS,
        dtype="int16",
        blocksize=chunk_size,
    )

    try:
        stream.start()
        while True:
            audio_chunk, overflowed = stream.read(chunk_size)
            if overflowed:
                continue

            # openWakeWord expects int16 numpy array
            audio_data = audio_chunk.flatten()
            prediction = model.predict(audio_data)

            for model_name, score in prediction.items():
                if score >= config.WAKE_WORD_THRESHOLD:
                    console.print(
                        f"[bold green]Wake word detected! "
                        f"(confidence: {score:.2f})[/bold green]"
                    )
                    model.reset()
                    return True
    except KeyboardInterrupt:
        return False
    finally:
        stream.stop()
        stream.close()


def is_available() -> bool:
    """Check if wake word detection is available and enabled."""
    if not config.WAKE_WORD_ENABLED:
        return False
    try:
        from openwakeword.model import Model
        return True
    except ImportError:
        return False
