"""FFmpeg helpers and WAV chunk stitching (no Streamlit)."""

from __future__ import annotations

import os
import subprocess
import tempfile


def validate_wav_bytes(data: bytes, *, context: str = "Audio") -> None:
    """Ensure bytes look like a WAV container (browser clips should be WAV)."""
    if not data:
        raise ValueError(f"{context}: empty byte buffer.")
    if len(data) < 12:
        raise ValueError(f"{context}: data too short to be a valid WAV ({len(data)} bytes).")
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError(
            f"{context}: missing RIFF/WAVE header — input may not be WAV. "
            "Re-record or verify the browser uploaded a WAV clip."
        )


def run_ffmpeg(cmd: list[str], *, context: str) -> None:
    """Run ffmpeg; raise RuntimeError with stderr on failure."""
    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as e:
        raise RuntimeError(
            f"{context}: ffmpeg was not found. Install ffmpeg and add it to your PATH."
        ) from e
    except subprocess.CalledProcessError as e:
        err = (e.stderr or e.stdout or "").strip()
        tail = f"\n\nffmpeg stderr:\n{err}" if err else ""
        raise RuntimeError(
            f"{context}: ffmpeg exited with code {e.returncode}.{tail}"
        ) from e


def _ffmpeg_concat_escape_path(path: str) -> str:
    return path.replace("\\", "/").replace("'", r"'\''")


def stitch_audio_chunks(chunks: list[bytes]) -> bytes:
    """Concatenate multiple WAV byte blobs into one WAV using ffmpeg concat demuxer."""
    if not chunks:
        raise ValueError("stitch_audio_chunks requires at least one chunk")

    for i, chunk in enumerate(chunks):
        if not chunk:
            raise ValueError(f"stitch_audio_chunks: chunk {i} is empty (0 bytes).")
        validate_wav_bytes(chunk, context=f"Recorded clip {i + 1}")

    with tempfile.TemporaryDirectory() as tmpdir:
        list_file_path = os.path.join(tmpdir, "list.txt")

        with open(list_file_path, "w", encoding="utf-8", newline="\n") as list_file:
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(tmpdir, f"chunk_{i}.wav")
                with open(chunk_path, "wb") as f:
                    f.write(chunk)
                list_file.write(f"file '{_ffmpeg_concat_escape_path(chunk_path)}'\n")

        output_path = os.path.join(tmpdir, "output.wav")
        run_ffmpeg(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file_path,
                "-c",
                "copy",
                output_path,
            ],
            context="Combining recorded audio clips",
        )

        with open(output_path, "rb") as f:
            out = f.read()

    if len(out) < 200:
        raise RuntimeError(
            f"Stitched WAV is suspiciously small ({len(out)} bytes); concat may have failed silently."
        )
    validate_wav_bytes(out, context="Stitched recording")
    return out
