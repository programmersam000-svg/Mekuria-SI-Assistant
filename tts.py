"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║           Text-to-Speech  — The Speaking Layer               ║
╚══════════════════════════════════════════════════════════════╝
Uses edge-tts (Microsoft Edge neural voices) for free, high-quality
text-to-speech synthesis. Audio playback via Windows Media Player COM.
"""

import asyncio
import os
import subprocess
import sys
import tempfile
import threading
import time

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console

import config

console = Console()


# ── Persistent event loop for async TTS (avoids RuntimeError on Windows) ──
_loop = None
_loop_thread = None


def _get_event_loop() -> asyncio.AbstractEventLoop:
    """Get or create a persistent background event loop for async TTS calls."""
    global _loop, _loop_thread
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        _loop_thread = threading.Thread(target=_loop.run_forever, daemon=True)
        _loop_thread.start()
    return _loop


def _run_async(coro):
    """Run an async coroutine on the persistent background event loop."""
    loop = _get_event_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=30)


# ── Core TTS functions ────────────────────────────────────────────

async def _synthesize(text: str, output_file: str = None) -> str:
    """
    Synthesize text to an MP3 file using edge-tts.
    Returns the path to the saved audio file.
    """
    import edge_tts

    output_file = output_file or os.path.join(
        tempfile.gettempdir(), "mekuria_response.mp3"
    )

    communicate = edge_tts.Communicate(
        text,
        voice=config.TTS_VOICE,
        rate=config.TTS_RATE,
        volume=config.TTS_VOLUME,
    )
    await communicate.save(output_file)
    return output_file


def _play_audio(file_path: str):
    """
    Play an audio file using Windows' built-in capabilities.
    Uses PowerShell with Windows Media Player COM object for reliable MP3 playback.
    """
    abs_path = os.path.abspath(file_path)

    # Use PowerShell + Windows Media Player COM for reliable MP3 playback
    ps_script = (
        f'$player = New-Object System.Windows.Media.MediaPlayer; '
        f'$player.Open([uri]"{abs_path}"); '
        f'Start-Sleep -Milliseconds 500; '
        f'$player.Play(); '
        f'while ($player.NaturalDuration.HasTimeSpan -eq $false) {{ Start-Sleep -Milliseconds 100 }}; '
        f'$duration = $player.NaturalDuration.TimeSpan.TotalSeconds; '
        f'Start-Sleep -Seconds ($duration + 0.5); '
        f'$player.Close()'
    )

    try:
        subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                "Add-Type -AssemblyName PresentationCore; " + ps_script
            ],
            capture_output=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        console.print("[yellow]Audio playback timed out.[/yellow]")
    except Exception as e:
        console.print(f"[red]Audio playback error: {e}[/red]")


def speak(text: str):
    """
    Synchronous entry point — synthesize text and play it out loud.
    Uses a persistent event loop to avoid Windows asyncio issues.
    Does NOT print the text (caller handles display).
    """
    if not text.strip():
        return
    try:
        audio_file = _run_async(_synthesize(text))
        _play_audio(audio_file)
        # Clean up temp file
        try:
            os.remove(audio_file)
        except OSError:
            pass
    except Exception as e:
        console.print(f"[red]TTS Error: {e}[/red]")


# ── Utility ───────────────────────────────────────────────────────

def list_voices_sync(language_filter: str = "en") -> list:
    """Return a list of available voice names for a given language prefix."""
    import edge_tts

    async def _list():
        voices = await edge_tts.list_voices()
        return [
            v["ShortName"]
            for v in voices
            if v["Locale"].lower().startswith(language_filter.lower())
        ]

    return _run_async(_list())


if __name__ == "__main__":
    # Quick test
    test_text = f"Hello! I am {config.ASSISTANT_NAME}, your personal AI assistant. How may I help you today?"
    console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {test_text}")
    speak(test_text)
