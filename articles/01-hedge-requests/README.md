# 1. Hedge requests

**Title:** Hedged Requests for LLMs: Cutting Tail Latency in Voice Agents

Sending every voice-agent turn to the same model on two providers at once and using whichever speaks first. Built on Dean and Barroso's hedged requests ("The Tail at Scale", 2013), measured with my own benchmark and keys. Written as an independent experiment: nothing in the article comes from or points to my work.

| File | What it is |
|---|---|
| [article-v1.md](article-v1.md) | **The article, v1**, written as it would appear on Medium: title, subtitle, sections, figures with alt text and captions, code, results as code blocks (Medium has no tables) |
| [images/](images/) | Figures 01 to 05 (PNG, 1,320 px wide). `make_figures.py` redraws them from the harness run |
| [draft-v1.md](draft-v1.md) | The scaffold the article was written from: story settings (SEO title, description, slug, tags, publication), beats, and the pre-publish checklist |
| [research-notes.md](research-notes.md) | The numbers and how they were measured |

Numbers come from my own [harness](../../harness/README.md) (personal keys): DeepSeek V4.1 Flash 1017 on Together and inference.net, run 3 Nov 2026 23:03 to 23:33 from Sydney, 600 paired turns plus 600 live races (`harness/results/2026-11-03_sydney_deepseek_infnet`). The MiniMax M3.1 Flash run on the same two providers is only quoted for the "thinking off" point.

**Before publishing:** make the harness public on GitHub (the article links to `bnhquang/voice-agent-medium-blogs/tree/main/harness`), set the story settings from draft-v1.md, and run the playbook's pre-publish checklist.
