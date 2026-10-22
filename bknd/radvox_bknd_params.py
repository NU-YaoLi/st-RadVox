"""Model IDs and related OpenAI options. Change versions here only.

How to fill this file:
  1) Put the OpenAI model id string in quotes (the same name you use in the API).
  2) Redeploy / restart the Streamlit app so the new values load.
  3) If Streamlit Cloud has RADVOX_CHAT_MODEL set, that env value wins over CHAT_MODEL.
"""

from __future__ import annotations

import os

# Chat completions: clinical polish + structured report.
# The 2nd argument of os.environ.get(...) is the default model id.
CHAT_MODEL = os.environ.get("RADVOX_CHAT_MODEL", "gpt-6.1-sol")

# reasoning_effort sent with every chat completion.
# Accepted values: low, medium, high, xhigh, max.
# medium matches this task: classify abnormal organs and follow the template
# rules, without the extra wait of high, xhigh, or max on every dictation.
# This model rejects temperature, so chat calls do not send it.
CHAT_REASONING_EFFORT: str | None = "medium"

# Speech-to-text models listed in the sidebar.
# A tuple of strings. The first entry is the default radio selection.
TRANSCRIBE_MODELS: tuple[str, ...] = ("gpt-transcribe",)
