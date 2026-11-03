# AI detector

Checks how likely a paragraph is to be AI-written, on this laptop, for free. Nothing is sent anywhere.

It uses Desklib's open model ([desklib/ai-text-detector-v1.01](https://huggingface.co/desklib/ai-text-detector-v1.01), a fine-tuned DeBERTa-v3-large), which sits in `model/`.

## Use it

From this folder (`voice-agent-medium-blogs/ai-detector`), put the paragraph in quotes:

```bash
.venv/Scripts/python detect.py "Your paragraph here."
```

Several paragraphs at once, each in its own quotes:

```bash
.venv/Scripts/python detect.py "First paragraph." "Second paragraph."
```

A paragraph saved in a text file (Git Bash):

```bash
.venv/Scripts/python detect.py "$(cat paragraph.txt)"
```

Same in PowerShell:

```powershell
.venv\Scripts\python detect.py (Get-Content paragraph.txt -Raw)
```

It prints one line per paragraph:

```
1. 98% AI  (AI)  Racing two hosts cuts the slow tail, not the typical turn. I...
2. 20% AI  (human)  yo the thing is the agent kept going quiet for like 4 second...
```

It takes about 10 seconds, most of it loading the model. Check one paragraph at a time, not a whole article: the model reads at most about 500 words per paragraph, and anything past that is ignored. Leave out code, tables and headings.

## What the scores mean

A rough hint, not a verdict. Tested on 3 Nov 2026:

| Text | Scores | Median |
|---|---|---|
| My own dictated messages (Wispr Flow) | 10, 15, 73, 25, 0, 66% | 20% |
| My own typed messages | 17, 89, 93, 28, 30, 30% | 30% |
| Plain, terse docs Claude wrote in this repo | 2 to 27% | 4 to 27% |
| A typical "AI announcement" paragraph | 99% | |
| The same paragraph, rewritten by humanizer | 15% | |

So it catches stereotypical AI writing (hype, "it's not just X, it's Y", tidy three-part lists), misses plainer AI writing, and sometimes flags real human text. Medium uses its own tools, not this one.

## Set it up again (new laptop)

```bash
python -m venv .venv
.venv/Scripts/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/Scripts/python -m pip install transformers sentencepiece protobuf huggingface_hub
.venv/Scripts/python -c "from huggingface_hub import snapshot_download; snapshot_download('desklib/ai-text-detector-v1.01', local_dir='model')"
```

`model/` (1.7 GB) and `.venv/` are not in git.
