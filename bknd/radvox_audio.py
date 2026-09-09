"""Audio validation helpers (no Streamlit)."""

from __future__ import annotations


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
