"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║            Speech-to-Text  — The Hearing Layer               ║
╚══════════════════════════════════════════════════════════════╝
Uses Faster-Whisper for fast, local, offline speech transcription.
"""

import io
import sys
import wave
from typing import Optional

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from rich.console import Console

import config

console = Console()

# ── Lazy-loaded singleton ─────────────────────────────────────────
_model: Optional[WhisperModel] = None


def _get_model() -> WhisperModel:
    """Lazy-initialize the Whisper model on first use."""
    global _model
    if _model is None:
        console.print(
            f"[cyan]Loading Whisper model '[bold]{config.WHISPER_MODEL_SIZE}[/bold]' "
            f"on {config.WHISPER_DEVICE}...[/cyan]"
        )
        _model = WhisperModel(
            config.WHISPER_MODEL_SIZE,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE,
        )
    return _model


# ── Microphone recording with silence detection ──────────────────

def record_audio() -> np.ndarray:
    """
    Record from the default microphone until the user stops speaking
    (detected by sustained silence) or MAX_RECORD_SECONDS is hit.

    Returns a 1-D float32 NumPy array of audio samples at 16 kHz.
    """
    console.print("[green]Listening... speak now.[/green]")

    frames: list = []
    silent_chunks = 0
    chunk_duration = 0.1  # 100 ms per chunk
    samples_per_chunk = int(config.SAMPLE_RATE * chunk_duration)
    max_chunks = int(config.MAX_RECORD_SECONDS / chunk_duration)
    silence_chunks_needed = int(config.SILENCE_DURATION / chunk_duration)

    has_speech = False

    for _ in range(max_chunks):
        chunk = sd.rec(
            samples_per_chunk,
            samplerate=config.SAMPLE_RATE,
            channels=config.CHANNELS,
            dtype="float32",
        )
        sd.wait()
        frames.append(chunk.flatten())

        rms = float(np.sqrt(np.mean(chunk ** 2)))

        if rms > config.SILENCE_THRESHOLD:
            has_speech = True
            silent_chunks = 0
        else:
            if has_speech:
                silent_chunks += 1

        if has_speech and silent_chunks >= silence_chunks_needed:
            break

    audio = np.concatenate(frames)
    console.print(f"[dim]Captured {len(audio) / config.SAMPLE_RATE:.1f}s of audio.[/dim]")
    return audio


def _audio_to_wav_bytes(audio: np.ndarray) -> bytes:
    """Convert a float32 numpy audio array to WAV bytes in memory."""
    int16_audio = (audio * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(config.CHANNELS)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(config.SAMPLE_RATE)
        wf.writeframes(int16_audio.tobytes())
    buf.seek(0)
    return buf.read()


def save_wav(audio: np.ndarray, path: Optional[str] = None) -> str:
    """Save audio to a WAV file and return the path."""
    path = path or config.AUDIO_TEMP_FILE
    wav_bytes = _audio_to_wav_bytes(audio)
    with open(path, "wb") as f:
        f.write(wav_bytes)
    return path


# ── Transcription ─────────────────────────────────────────────────

def transcribe(audio: np.ndarray) -> str:
    """
    Transcribe a numpy audio array to text using Faster-Whisper.
    Returns the full transcription as a single string.
    """
    model = _get_model()

    # Save to a temp WAV because faster-whisper expects a file path
    wav_path = save_wav(audio)

    segments, info = model.transcribe(
        wav_path,
        language=config.STT_LANGUAGE,
        beam_size=5,
        vad_filter=True,          # Filter out non-speech
    )

    detected_lang = info.language
    console.print(f"[dim]Detected language: {detected_lang} "
                  f"(prob {info.language_probability:.0%})[/dim]")

    text = " ".join(seg.text.strip() for seg in segments).strip()
    return text


def listen() -> str:
    """
    Full pipeline: record from the microphone -> transcribe -> return text.
    This is the main entry point for the hearing layer.
    """
    audio = record_audio()
    if len(audio) < config.SAMPLE_RATE * 0.3:
        return ""  # Too short to be meaningful
    text = transcribe(audio)
    console.print(f"[bold yellow]You said:[/bold yellow] {text}")
    return text
