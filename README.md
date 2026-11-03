# Voice Agent Medium Blogs

Where I write articles and do the research for my Medium posts on voice agents.

Each post gets its own folder under `articles/`, numbered in the order I start them (`NN-short-slug`). A post's folder holds everything behind it: the draft, research notes, sources, and any test scripts, numbers or images.

Drafts follow [andys_writing_style.md](andys_writing_style.md), so they sound like me, and [medium_article_playbook.md](medium_article_playbook.md) for Medium's rules, SEO and promotion (researched 3 Nov 2026). The prose is always mine: Medium limits AI-written stories to the author's own followers.

## Articles

| # | Folder | Topic | Status |
|---|---|---|---|
| 1 | [`articles/01-hedge-requests`](articles/01-hedge-requests) | Hedge requests: racing models against each other on every turn | v1 written (`article-v1.md`), not published |

## Tools

| Folder | What it is |
|---|---|
| [harness/](harness/README.md) | Latency benchmark for article 1: one model on two providers, alone, raced and hedged. Personal keys from AWS Secrets Manager. Private working copy |
| [articles/01-hedge-requests/llm-race-bench/](articles/01-hedge-requests/llm-race-bench/README.md) | Submodule: the public, cleaned copy of the harness ([bnhquang/llm-race-bench](https://github.com/bnhquang/llm-race-bench)) that article 1 links to. This repo stays private |
| [ai-detector/](ai-detector/README.md) | Local AI-writing detector (Desklib's open model). `python detect.py "a paragraph"` |
| `humanizer/` | [blader/humanizer](https://github.com/blader/humanizer), a skill that rewrites AI-sounding text. Cloned, its own repo, not tracked here |
