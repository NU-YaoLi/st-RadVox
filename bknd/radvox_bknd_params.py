"""Model IDs and related OpenAI options. Change versions here only.

How to fill this file:
  1) Put the OpenAI model id string in quotes (the same name you use in the API).
  2) Redeploy / restart the Streamlit app so the new values load.
  3) If Streamlit Cloud has RADVOX_CHAT_MODEL set, that env value wins over CHAT_MODEL.
"""

from __future__ import annotations

import os

# Chat completions: clinical polish + structured report.
# Fill in the 2nd argument of os.environ.get(...) — that is the default model id.
#
# Samples (use one string, not a list):
#   "gpt-5.6-sol"
#   "gpt-4o"
#   "gpt-4.1"
#   "gpt-4o-mini"
#
# Example if you switch chat models:
#   CHAT_MODEL = os.environ.get("RADVOX_CHAT_MODEL", "gpt-4o")
CHAT_MODEL = os.environ.get("RADVOX_CHAT_MODEL", "gpt-6.1-sol")

# Extra chat.completions field for the current chat model family.
# Fill in either "none" or None (no quotes on None).
#
# Samples:
#   "none"  → gpt-5.6-* (and similar reasoning chat models)
#   None    → gpt-4o, gpt-4.1, gpt-4o-mini, and anything that rejects reasoning_effort
#
# Example if you switched CHAT_MODEL to gpt-4o:
#   CHAT_REASONING_EFFORT: str | None = None
CHAT_REASONING_EFFORT: str | None = "none"

# Speech-to-text models listed in the sidebar.
# Fill in a tuple of strings. The first entry is the default radio selection.
# Add more entries if you want extra choices in the UI.
#
# Samples:
#   ("gpt-transcribe",)
#   ("gpt-4o-transcribe",)
#   ("gpt-4o-mini-transcribe",)
#   ("whisper-1",)
#   ("gpt-transcribe", "gpt-4o-transcribe", "whisper-1")
#
# Example with one model:
#   TRANSCRIBE_MODELS: tuple[str, ...] = ("gpt-4o-transcribe",)
# Example with several models (sidebar radio will show all of them):
#   TRANSCRIBE_MODELS: tuple[str, ...] = ("gpt-transcribe", "whisper-1")
TRANSCRIBE_MODELS: tuple[str, ...] = ("gpt-transcribe",)
