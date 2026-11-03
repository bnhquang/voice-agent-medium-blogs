# Medium technical article playbook (late 2026)

Researched and checked on 3 Nov 2026. Medium changes its programs often: anything marked "may be out of date" or "unverified" should be rechecked before you rely on it.

**Confidence tags used throughout**

- **(Official)**: a current Medium, Google, Hacker News or Reddit rule or staff statement.
- **(Data)**: backed by a measured study (sample size given where known).
- **(Expert)**: consensus of experienced technical writers or editors.
- **(Anecdote)**: one person's report or a single example.
- **(Inference)**: my own conclusion from the sources, not stated by any of them.

Medium's rules are paraphrased closely rather than quoted at length (copyright limits on quoting). The link next to each rule goes to the exact wording.

---

## Summary

1. **Medium has three distribution levels**: Network (your followers only), General (matched to interested readers) and Boost (human-picked, highest priority). The guidelines were last updated on 29 Jun 2026. [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473) (Official)
2. **AI-written prose is the biggest risk.** It is classed as low-value, so it misses General Distribution. Undisclosed AI text is capped at Network only. Boost requires that the story does not read as AI-generated. Grammar, spelling, outlining and fact-check tools are fine and need no disclosure. [AI policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy) (Official)
3. **Boost nominations by editors ended on 31 May 2026.** Curators still Boost at the same rate. Medium says your best route is still a high-quality publication and an editor. [Medium blog, 6 May 2026](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a) (Official)
4. **Partner Program pay now rewards readers who arrive from outside Medium.** There are bonuses for external traffic, Google search and subscriber emails. A read-ratio adjustment penalises titles that do not deliver. [Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193) (Official)
5. **Clickbait and vague titles both block Boost.** The title, subtitle and cover must tell a feed reader exactly what they are getting. (Official)
6. **Set the SEO title and SEO description in More settings.** Put the search phrase first. The custom URL can only be set before publishing. (Official)
7. **Nobody searches "LLM hedging" or "model racing" yet.** People do search "hedged requests", "request hedging", "time to first token", "llm latency" and "voice agent latency". Own the intersection of those terms. (Data: Google autocomplete, 3 Nov 2026)
8. **The closest competing post is HOAi's "A simple fix for LLM tail latency"** (June 2026, 54 points on Hacker News). It is short, uses one provider and 50 replayed requests, and has no cancellation or cost maths. Your gap is cross-provider hedging, production-scale numbers, hedge-after-delay versus race-always, cancellation and the real bill. (Data)
9. **For promotion, Hacker News is the biggest lever.** Submit as a normal story, not Show HN, with the original title and no upvote requests. On Reddit, post a tailored version to two or three subreddits, not the same post to many. (Official)
10. **Several facts could not be verified.** They are listed at the end.

---

## Pre-publish checklist

**Content**
- [ ] I wrote every sentence of the prose myself. If any AI-generated text or image is left in, I disclosed it in the first two paragraphs or in the image caption. (Official)
- [ ] The title plus the first three sentences answer who this is for and what they get. (Expert)
- [ ] Every number is measured and sourced. No claim I cannot back up. (Official: hallucinated stats are a rules violation)
- [ ] It says what did not work and what I am unsure about. (Expert)
- [ ] Every term is explained once, in plain words, without relying on a link. (Expert)
- [ ] No more than one or two self-promo links at the end, and no "please clap/follow" out of nowhere. (Official, staff)
- [ ] No sponsor, affiliate or provider promo framing. Any relationship with Together AI or Wafer is disclosed. (Official)

**Formatting**
- [ ] The title uses the big T, the subtitle the small T, section heads the big T and sub-sections the small T. Never use bold as a header. (Official, staff)
- [ ] Code is in native code blocks, not screenshots. Longer code goes in a linked gist or repo. (Official / Expert)
- [ ] Charts are original PNGs at least 1,200 px wide, each with alt text and a caption that states the takeaway. (Official)
- [ ] Links sit on descriptive anchor text, not pasted raw URLs. (Official, staff)
- [ ] I read it once on a phone and once out loud. No em dashes. (Expert; your style guide)

**Story settings (three-dot menu, then More settings)**
- [ ] Custom story link (slug) set before publishing. It cannot be changed after. (Official)
- [ ] SEO title: about 60 characters or fewer, search phrase first. (Official, staff)
- [ ] SEO description: main point within the first 156 characters, search phrase included naturally. (Official, staff)
- [ ] Five topics (tags), all accurate, matching the target publication's topics. (Official)
- [ ] Preview image and focal point checked. Display title and subtitle checked in the preview. (Official)
- [ ] Canonical link set only if the story first appeared somewhere else. (Official)
- [ ] Paywall decision made (see 1.8). "Email to subscribers" left ticked. (Official)

**Publication**
- [ ] Submitted to one fitting, active publication. If it is declined or the response window passes, try the next. (Official / Inference)

---

## 1. Medium's own rules for distribution

### 1.1 The three levels (Official)
Source: [Medium's Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473), updated 29 Jun 2026.

- **Network Distribution**: shown to people who follow you, and the publication's followers if it is in one. This is the baseline for any story that does not break the Medium Rules.
- **General Distribution**: also matched to readers based on their interests and on related writers and publications they follow.
- **Boost**: especially high-quality stories that meet the Boost Guidelines. They get higher priority in matching, plus General and Network distribution.
- **Off Medium**: the levels only matter inside Medium's app, website and Digest emails. Search engines, social media and direct links reach every story regardless of level.
- **Who reviews**: a human curation team reviews stories seven days a week, found through Medium's own internal curation tools.

### 1.2 What gets a story Boosted (Official)
Same source. Medium says this is not a checklist; the story is judged on the overall spirit. The hallmarks:

- **Writer's experience.** There is a clear reason why this writer is writing about this topic. Credible first-hand experience counts for more than credentials. The story is human-created and does not appear to be AI-generated.
- **Value and impact.** Reading it is time well spent. The reader uses a skill from it, or wants to share it, or is glad they pay for Medium.
- **Respect for the reader.** It is not a sales pitch or a bid for attention.
- **Non-derivative.** It brings something new. It does not paraphrase, recombine or rehash what is easy to find elsewhere. Republishing your own work from another site is fine (Medium actively encourages syndicating your own work). Republished translations are not eligible.
- **Writing and craftsmanship.** Well written, error-free, properly sourced. Length suits the story. Images add value, with alt text and credits. Formatting is correct.

Programming examples Medium itself lists as Boosted:
- A detailed, original LLM-app how-to.
- "How modern browsers work" by Chrome's developer-experience lead.
- A computer-vision study built on the writer's own data plus how to repeat it.

The pattern: first-hand expertise, original data, and a how-to the reader can apply. (Official)

**What disqualifies an otherwise good story from Boost:**
- A title, subtitle or cover that does not represent the story. A tabloid-style sensational headline is out, and so is an overly generic, mysterious or formulaic one.
- A cover image that hurts. Original covers work best and careful stock is fine. AI-generated cover art must be credited, and Medium says it often puts readers off. No cover beats a poor one.
- Content that is not safe for work.
- Stories that are not in English.

### 1.3 What limits a story to Network only (Official)
Same source. These things block General Distribution:

- A clickbait title, subtitle or cover.
- Unconstructive negativity: rants, outrage, private disputes.
- **Low-value content.** This includes:
  - AI-generated content
  - sponsored content, content marketing and PR
  - stories whose main point is gathering sign-ups or traffic, or selling
  - unoriginal or generic content, summaries of other sources, and link round-ups
  - writing too poor to follow
- NSFW content and misinformation.
- **Topic spamming** (tags that do not fit the story) and **mass mentions** (Medium's example is tagging 20 users).
- Rules violations, for example copyrighted images used without permission.
- Community shout-outs, such as "write for us" posts.
- **Stories about Medium itself.** Pieces about the Partner Program, making money on Medium or Boost are always Network only.

### 1.4 AI content policy (Official)
Source: [Artificial Intelligence (AI) content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy), live on 3 Nov 2026. The page itself is undated.

- **What counts as AI-generated writing:** the majority of the content was produced by an AI tool with little or no editing or fact-checking.
- **Undisclosed AI writing:** in the policy's own words, "Undisclosed AI-generated writing will be given Network Only distribution."
- **Paywall:** AI-generated writing cannot be paywalled, whether it is disclosed or not. Accounts that paywall it can lose Partner Program enrollment. The [paywall content policy](https://help.medium.com/hc/en-us/articles/31090080813591) says the same.
- **AI-assisted text** must be clearly labelled. Unlabelled AI-assisted text is also restricted to your own network.
- **No disclosure needed** for grammar or spell checkers, outlining help or fact verification.
- **How to disclose:** one sentence within the first two paragraphs. AI-generated images need a caption saying so.
- **Detection:** Medium uses detection tools plus human review.
- **Also banned:** easily disprovable AI-hallucinated statistics or events.

**What this means for you (Inference).** If Claude drafts any of the prose, even disclosed, the story is classed as "AI-generated content". That is low-value under 1.3, so it is not eligible for General Distribution, let alone Boost. Use AI for research, outlines, grammar and fact checks only, and write the sentences yourself. Several places you might promote it also ban LLM-written copy (r/LocalLLaMA, r/programming; see section 6).

### 1.5 How Boost works now (Official)
- **The Boost Nomination Program closed on 31 May 2026.** It let publication editors nominate stories. Medium says the way stories are reviewed for Boost has not changed, and curators keep reviewing at the same rate. Publications remain one of the main sources curators use. [Medium blog, 6 May 2026](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a)
- **The Editor Partner Program opened to all qualifying publications on 1 Jul 2026.** Editors who assign themselves to a submitted story earn 25% of what that story earns, from a separate budget; writers keep 100%. [Medium blog](https://medium.com/blog/new-a-program-to-pay-publication-editors-d9c4f1ed40d8)
- **Qualifying publications** must have open submissions. They must also meet monthly criteria, including $200 in paywalled earnings and consistently landing stories in General or Boost (Medium names low-effort AI content as what drags a publication down). Over 100 publications and 300 editors qualified in July 2026. [Editor newsletter, 14 Jul 2026](https://medium.com/medium-handbook/editor-newsletter-the-editor-partner-program-is-now-open-to-all-qualifying-publications-cdf35b56f56c)
- **Editors only earn on paywalled stories (Inference).** They may favour paywalled submissions. None of the publications checked requires it.
- **Boost is not the only path.** Medium said in 2024 that five times as many un-Boosted stories reach large readerships as Boosted ones. [Stories that almost get Boosted](https://medium.com/medium-handbook/stories-that-almost-get-boosted-99be07d01779) (Official, may be out of date)

### 1.6 Why good stories narrowly miss Boost (Official, June 2024)
Source: [Zulie @ Medium, "Stories that almost get Boosted"](https://medium.com/medium-handbook/stories-that-almost-get-boosted-99be07d01779), quoting Medium's curators. The parts about nominations are out of date; the reasons below still match the 2026 guidelines.

- **Too much self-promotion.** Keep it to one or two story links, or one website link, at the end. Do not ask for engagement without giving a reason.
- **Lack of context and development.** A list of links with little explanation reads like a draft outline.
- **Shocking cover images, or images you lack rights to.** Medium's examples include watermarked or "all rights reserved" images.
- **Lack of craft.** Raw pasted links, more text inside images than outside them, gratuitous profanity.
- **Anyone could have written it.** Curators want a story only you could write. Their test: could someone have written it from Wikipedia?
- **Use five accurate tags**, so curators can find the story.

### 1.7 How the Partner Program pays now (Official)
Source: [Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193), current method, read 3 Nov 2026. Earnings come only from paying members on paywalled stories:

- **Member reading time.** Reading and listening are combined. A read counts after 30 seconds or more, and idle time is excluded.
- **Engagement points.** Reading time plus member claps, highlights and replies.
- **Boost bonus.** Boosted stories earn at a higher rate. Medium says non-Boosted stories now get a larger share than before.
- **External traffic bonus.**
  - Member reads that come from outside Medium earn 5% extra.
  - Reads found through search engines get an additional share on top of that.
  - Reads from your email notifications earn more than reads from the feed.
  - Medium tells writers to share externally, fill in SEO settings and send the email.
- **New member conversions.** A one-time payment when a non-member subscribes to read your paywalled story. This replaced the 2021 to 2025 referral programme.
- **Member read ratio adjustment.** Member reads divided by member views. Below-average stories are adjusted down. Medium says this targets stories that do not deliver on their title, and it does not penalise long stories.
- **Friend Links.** Member reads through a Friend Link count; non-member reads do not.
- **Publications.** Being in a publication does not change earnings.

**Eligibility** ([help](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)):
- an active paid Medium membership
- at least one published story
- a complete profile
- age 18 or over
- a bank and tax residence in a supported country (Australia is listed)

**Not allowed behind the paywall:** Medium-meta stories and fully AI-generated writing. [Paywall policy](https://help.medium.com/hc/en-us/articles/31090080813591)

### 1.8 Member-only (paywalled) versus free
- **Paywalled: what you gain.** Earnings and the Boost bonus. (Official)
- **Paywalled: what it costs.** Non-members arriving from Google, Hacker News or Reddit see only a preview unless you share a Friend Link, and their reads earn nothing. (Official)
- **Paywall and Google.** Medium staff point out that a paywalled story ranking in Google blocks non-member searchers; Zulie kept her search-focused stories free as a portfolio. [Medium Handbook, 2025](https://medium.com/medium-handbook/how-to-use-medium-seo-settings-to-reach-more-readers-97facde95e83) (Official, staff)
- **Paywall and Reddit/HN.**
  - r/Python bans paywalled and Medium links. (Official, subreddit rule, via mirror)
  - Hacker News accepts paywalled stories when a workaround such as a Friend Link exists. (Official)
- **Paywall and distribution.** The current Distribution Guidelines do not list paywall status as a factor for General or Boost. An older help page said paywall status was not considered for Boost, but it now returns 404, so this is unverified for 2026.
- **Recommendation (Inference).** Publish this first article **free**. The goals are reach, Google traffic and reputation, and every off-Medium channel works better without the paywall. If you want earnings, paywall it and share only the Friend Link off Medium. Revisit for later posts once you have followers.

---

## 2. On-page mechanics

### Title and subtitle
- **Formatting.** Big T for the title, small T for the subtitle on the line below. Medium staff say bolded or wrongly sized titles may disqualify a story from curation. [Formatting tips](https://medium.com/blog/tips-for-formatting-your-title-and-headers-1ff1a016ef75) (Official, staff, updated 2022)
- **Display title and subtitle.** You can set a different title and subtitle for previews on Medium and social cards. [Help](https://help.medium.com/hc/en-us/articles/214895188-Custom-titles-subtitles) (Official)
- **Length.**
  - Medium sets no title length rule that I could find.
  - For Google, Medium's SEO lead said titles over about 60 characters get cut in results. (Official, staff, 2020)
  - Google itself says there is no limit; it truncates to fit the device. [Google title links](https://developers.google.com/search/docs/appearance/title-link) (Official)
  - Hacker News titles max out at 80 characters (not re-checked this session).
- **Keyword placement.** Put the words people search near the start, especially in the SEO title. (Official, staff)
- **Write titles for humans.** Keep the on-page title written for Medium readers and put the search phrase in the SEO title. Medium's advice is that Medium readers click on expertise, while searchers click on the literal answer. (Official, staff 2025)

### SEO title and SEO description (More settings)
- **Where they show.** They control what search engines show; the on-Medium title and subtitle stay as written. [How to use Medium SEO settings](https://medium.com/medium-handbook/how-to-use-medium-seo-settings-to-reach-more-readers-97facde95e83), Medium Handbook (Official, staff, 2025)
- **What goes in them.** Include the target phrase naturally in both. (Official, staff)
- **SEO title.** About 60 characters, most important words first. [SEO tips](https://medium.com/medium-handbook/seo-tips-to-make-your-stories-discoverable-and-grow-your-readership-b0c8230a8200) (Official, 2020/2021, may be dated)
- **SEO description.** Google usually cuts after about 156 characters. Medium's older advice is to put the main idea in the first 156 characters; it allows 200 to 300 in total. Google says there is no limit, and it may ignore the description and build a snippet from the page. [Google snippets](https://developers.google.com/search/docs/appearance/snippet) (Official)
- **After publishing.** One writer reports the SEO title could not be edited after publishing. [r/Medium](https://www.reddit.com/r/Medium/comments/1kzln34/is_there_a_way_to_edit_the_seo_title_in_medium/) (Anecdote) Set it before you publish.

### Custom URL slug
- **When to set it.** In More settings, under Advanced Settings, then Customize Story Link. It can only be set before publishing. [Help](https://help.medium.com/hc/en-us/articles/360039393374-Set-a-custom-link) (Official)
- **What to use.** A short, keyword-led slug. (Expert)

### Canonical link
- **Where to set it.** More settings, then Advanced Settings, then "This story was originally published elsewhere". Medium's import tool sets it automatically. Only the author can set it. [Help](https://help.medium.com/hc/en-us/articles/360033930293) (Official)
- **Google's view on syndication.** Since May 2023 Google says rel=canonical is not recommended for avoiding duplication across syndication partners; it prefers the partner copy to be noindexed. Google still treats a cross-domain canonical as a hint. [Search Engine Land summary](https://searchengineland.com/google-no-longer-recommends-canonical-tags-for-syndicated-content-406491) (Official, via secondary report)
- **dev.to and Hashnode** both let you set the canonical yourself (`canonical_url`, or "Add Original URL"). (Official)
- **Practical rule (Expert/Inference).** Wherever the original lives, point every copy's canonical at it.
  - If you have no personal blog, Medium is the original. Cross-post to dev.to later with its canonical pointing to Medium.
  - Hacker News moderators prefer the original source and sometimes swap Medium URLs for the author's own site.

### Tags (Medium calls them topics)
- **How many.** Up to five per story. [Help](https://help.medium.com/hc/en-us/articles/214741038-Using-topics) (Official) Medium staff advise using all five, relevant and popular, and never off-topic (off-topic tags count as topic spam). (Official)
- **Topic pages.** Redesigned on 23 Oct 2026: AI clusters stories into subtopics and adds a context note to each. [Medium blog](https://medium.com/blog/new-use-the-new-topic-pages-to-explore-your-fascinations-on-medium-6e03d5856434) (Official)
- **Publication fit.** Publication editors now see a yellow "off-topic" badge when your tags do not match the publication's ten chosen topics, so match them. [Editor newsletter, Jul 2026](https://medium.com/medium-handbook/editor-newsletter-the-editor-partner-program-is-now-open-to-all-qualifying-publications-cdf35b56f56c) (Official)
- **Tag size versus competition (Inference).** Big tags put you in front of many followers but among tens of thousands of stories. Small exact tags keep you visible longer on a quiet topic page. Mix two big, two mid and one exact.

Tag sizes as shown on Medium tag pages on 3 Nov 2026 (Data; small follower numbers look odd, see "Could not verify"):

| Tag | Followers | Stories |
|---|---|---|
| Software Engineering | 4.5M | 180K |
| AI Agent | 708K | 69K |
| LLM | 616K | 82K |
| Large Language Models | 12.3K | 26K |
| Distributed Systems | 7.1K | 18K |
| System Design Concepts | 6.1K | 11K |
| Conversational AI | 5.1K | 4.2K |
| Performance | 1.4K | 29K (mostly web/JS) |
| Voice Ai | 66 | 899 |
| Latency | 27 | 749 |
| Ai Voice Agent | 59 | 305 |
| Voice Agent | 8 | 60 |

### Featured / preview image and cover
- **Image size.** Images must be at least 1,192 px wide for all placement options. Supported formats are JPG, PNG and GIF, up to 25 MB. [Using images](https://help.medium.com/hc/en-us/articles/215679797-Using-images) (Official) Medium's SEO guidance says 1,200 px or wider. (Official)
- **Focal point.** Editors and writers can adjust the focal point on the pre-publish page. (Official, Jul 2026)
- **Cover choice.** Original beats stock, and stock beats a bad AI image. AI covers need a caption crediting the AI. (Official)
- **For a technical post (Expert/Inference).** A clean, original diagram or your headline latency chart is the most honest cover. It also passes the "represents the story" test.

### Alt text and captions
- **Alt text.** Click the image, then the Alt text button. Medium's Boost guidelines ask for it, and Medium's SEO team says search engines use it. (Official)
- **Captions.** Use them to state the takeaway of each chart. Captions cannot be italic. (Official / Expert)

### Headings
- **Two levels.** Use the big T for section headers and the small T for sub-sections; do not bold lines to fake headers. (Official, staff)
- **Table of contents.** Medium on the web now builds a native table of contents from your headings. (Official, Jul 2026)
- **Front-load headings.** Start each heading with its most informative words; readers scan the first two words of headings. [NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) (Data)

### Code blocks
- **How to add them.** Type three backticks on a new line, or use the { } button. Code blocks now have syntax highlighting. For inline code, use single backticks. [Help](https://help.medium.com/hc/en-us/articles/35756844492439-Using-code-blocks-and-inline-code) (Official)
- **Never put code in screenshots.** Curators mark down stories with more text inside images than outside them. (Official, staff)
- **Gists versus native blocks (Expert).** Keep snippets short (about 10 to 30 lines) and native, so they are readable on phones and indexable. Link the full implementation in a GitHub repo or gist.

### Embeds and charts
- **How embeds work.** Paste a supported URL on its own line and press Enter. Medium uses Embed.ly, which covers GitHub Gists, CodePen, Twitter/X and over 300 providers. Embed codes and scripts are not supported. [Using embeds](https://help.medium.com/hc/en-us/articles/214981378-Using-embeds) (Official)
- **Charts (Expert).** Interactive charts are not native. Export static PNG charts, 1,200 px or wider, with large fonts for phones, and link an interactive version or the raw data if you have one.

### Read time
- **How Medium computes it.** At about 275 words per minute, with extra time per image (images after the tenth count as 3 seconds). [Read Time and You](https://medium.com/blog/read-time-and-you-bc2048ab620c) (Official)
- **The "7 minutes" study.** Medium's 2013 Data Lab study found total reading time peaked at about 7-minute posts. [Medium Data Lab, 2013](https://medium.com/data-lab/74b9f41509b) (Data, but old: pre-paywall, all genres)
- **Is it still current?** I found no 2024 to 2026 study that replaces it. Medium's current guidance is that length should suit the story. The 2026 read-ratio adjustment explicitly does not penalise long stories. (Official)
- **Elsewhere.** Chartbeat data (date unclear) shows engaged time rising up to about 2,000 words. (Data, not Medium-specific)
- **Practical target for a deep technical post (Inference).** Roughly 1,800 to 2,600 words (8 to 11 minutes with charts), cutting anything that carries no number, decision or lesson.

### Bold, pull quotes and links
- **Bold.** Bold one key phrase per section at most. NN/g's eyetracking work recommends bolding key words for scanners. (Data)
- **Quotes.** Medium curators count proper use of blockquotes as craft. (Official) There is no data on pull quotes: use at most one, for the headline number. (Expert)
- **Links.** Put links on descriptive anchor text. Too many inline links, or raw URLs, hurt Boost chances. (Official, staff)

---

## 3. Publications

### Does submitting still help in 2026? Yes. (Official)
- **Medium's advice.** After closing nominations, Medium wrote that publications are one of its main sources for finding stories to Boost. Your best bet remains a high-quality publication and an editor. [Medium blog, May 2026](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a)
- **Extra reach.** A publication also sends your story to its followers' feeds and Digest emails, and to its newsletter subscribers. [Help](https://help.medium.com/hc/en-us/articles/360018677974-What-happens-to-your-story-when-you-publish-on-Medium)
- **Etiquette.** Medium asks writers to pick the best-fit publication and to respect closed submissions. [Publication guidelines](https://help.medium.com/hc/en-us/articles/41530252213655-Medium-Publications-Best-Practices-and-Guidelines)
- **Editor limits.** The same guidelines bar editors from making major changes without your input, adding large footers, or removing your story from the paywall without agreement.

### Gone or not viable (verified 3 Nov 2026)
- **Towards Data Science** left Medium on 3 Feb 2025. It is independent and takes submissions only through its own portal, not via Medium. [TDS announcement](https://towardsdatascience.com/towards-data-science-is-launching-as-an-independent-publication/)
- **TDS Archive** (medium.com/data-science) has been frozen since then.
- **Better Programming** was put on hiatus by Medium in Nov 2023. It has not reopened.
- **No dedicated voice-AI publication on Medium.** None is active; Voice Tech Podcast has been dead since Jan 2021.
- **Dormant:** Chatbots Life (no submission route found), Analytics Vidhya (last post Dec 2025) and Geek Culture.

### Active publications that fit this article
All were on Medium and posting as of late Oct or early Nov 2026, and none requires a paywall. Response times are as each publication states them.

| Publication | Followers | How to submit | Notes |
|---|---|---|---|
| [Data Science Collective](https://medium.com/data-science-collective/data-science-collective-submissions-guidelines-1fa4fa358ec3) | ~963K | Notion form first time, then "Add to publication" | Replies in 3 to 5 days, then ~24h. No fully AI-generated stories. Prior publication elsewhere OK. Medium's CEO is an editor. |
| [Level Up Coding](https://levelup.gitconnected.com/how-to-get-published-on-gitconnected-dac547ef556b) | ~369K | Email submit@gitconnected.com with draft link | Up to 1 week. Cross-posts allowed; do not delete after publishing. |
| [Towards AI](https://pub.towardsai.net/submit-your-medium-story-to-towards-ai-a4fa7e8b141d) | ~151K | Form at contribute.towardsai.net (draft link plus LinkedIn) | 24 to 72h; silence means no. **Unpublished drafts only.** Image credits and alt text required. |
| [AI Advances](https://aiadvances.org/write-for-ai-advances-1c617ad8b28a) (was ai.gopubby.com) | ~116K | Follow, then "Submit to publication" | ~24h. No LLM-written text. Featured image required. Says it is in the Editor Partner Program. |
| [Generative AI](https://generativeai.pub/a-new-publication-focused-on-generative-ai-write-for-us-9fdc95660934) | ~111K | Comment your username on the write-for-us post | 2 days; silence means no. |
| [ITNEXT](https://itnext.io/write-for-itnext-4dea1fd3adf) | ~87K | Email submit@itnext.io | No AI-written articles. Cover required. Good fit for distributed systems and SRE angles. |
| Stackademic / AI in Plain English | ~88K / ~50K | Follow the publication to get submit access | The parent brand moved its main site off Medium; these Medium sub-publications are still live. |

**Choosing one (Inference).**
- First choice: **AI Advances** (explicitly in the Editor Partner Program, AI engineering focus, fast reply) or **Towards AI**.
- If you want a pure engineering frame: **ITNEXT** or **Level Up Coding**.
- Submit to one at a time, and wait out its stated response window before trying the next.

There is no public list of Editor Partner Program publications. Medium keeps a general directory: [publications accepting submissions](https://medium.com/@MediumStaff/list/7c0ec8037e61). (Official)

---

## 4. Google and SEO

### 4.1 How Medium stories rank now
- **Domain authority.** Medium staff say medium.com's high domain authority lets unoptimised stories reach page one, and that the SEO fields add only a small extra lift. [Medium Handbook, 2025](https://medium.com/medium-handbook/how-to-use-medium-seo-settings-to-reach-more-readers-97facde95e83) (Official, staff; self-interested)
- **New writers may not be indexed straight away.** Medium withholds stories from Google until an account passes internal trust signals, which can take days to weeks. Medium says engaging with the community helps. [About SEO and Medium](https://help.medium.com/hc/en-us/articles/217991468-About-SEO-and-Medium) (Official)
  - Consequence: build a little activity (follows, thoughtful replies) before launch day.
- **Traffic trend.** Third-party estimates put medium.com's organic search traffic up 4.7% month on month in Feb 2026, with Google the largest referrer. ChatGPT and Gemini also send meaningful visits. [Semrush](https://www.semrush.com/website/medium.com/overview/) (Data, rough estimate)
- **AI Overviews take clicks on generic questions.**
  - Pew (900 US adults, March 2025): people clicked a result in 8% of visits with an AI summary, versus 15% without. [Pew](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/) (Data; Google disputes the method)
  - Ahrefs: an AI Overview correlates with 58% lower click-through for the top result (Dec 2025 data). [Ahrefs](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/) (Data, correlation)
  - Implication (Inference): do not chase "what is time to first token". Target specific, experience-heavy queries that a summary cannot answer, and aim to be the source cited.

### 4.2 Google rules that matter here (Official)
- **Helpful content.** Google's self-assessment asks:
  - Does it show first-hand expertise?
  - Is it original analysis?
  - Is it obvious who wrote it?
  - Is any AI or automation use clear to readers?
  - Was it made mainly to attract search visits (a warning sign)?
  - [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- **Titles.** Descriptive and concise, no repeated keywords, no boilerplate. Google may rewrite them from the H1, og:title or headings. [Title links](https://developers.google.com/search/docs/appearance/title-link)
- **Descriptions.** Unique, specific summaries, not keyword strings. [Snippets](https://developers.google.com/search/docs/appearance/snippet)
- **Syndication.** See canonical, section 2.

### 4.3 What people actually search
Google autocomplete, captured 3 Nov 2026. Autocomplete shows that a query exists, not how many people search it. I had no keyword-volume tool. (Data)

| Seed typed | What Google suggests |
|---|---|
| hedged requests | meaning, clickhouse hedged requests |
| request hedging | pattern, dynamodb, grpc, google, envoy, istio, http |
| llm hedging | nothing related (term barely searched) |
| tail latency llm | nothing beyond itself |
| the tail at scale | pdf, paper, dean & barroso, google, jeff dean, communications of the acm |
| time to first token | meaning, (ttft), benchmark, llm, vs latency, latency, openai, bedrock |
| ttft llm | benchmark, meaning, leaderboard, tpot, comparison, fastest ttft llm |
| llm latency | benchmark, leaderboard, optimization, metrics, comparison, vs throughput, reduction |
| reduce llm latency | only generic "how to reduce latency" |
| lowest latency llm | api, models, provider; low latency llm inference / api |
| voice agent latency | ai voice agent latency, elevenlabs ..., livekit voice agent latency |
| voice ai latency | lagging, delay, delay fix, low latency, agent latency |
| pipecat latency | latency observer, low latency, pipecat vs livekit latency |
| llm fallback | litellm fallback, llm gateway fallback, livekit llm fallback, llm api fallback |
| parallel llm calls | concurrent llm calls, langchain parallel llm calls |
| p99 latency | meaning, explained, vs p95, spikes, calculation |

**Reading of the data (Inference).**
- "Hedged requests" and "request hedging" are searched, but in a classic infrastructure context (gRPC, DynamoDB, Envoy).
- LLM people search "time to first token", "ttft", "llm latency" and "voice agent latency".
- Nobody searches "LLM hedging", "model racing" or "LLM request racing" yet.
- So name the technique "hedged requests" (the searched term) and say "racing" only as the plain-English explanation. Pair it with "LLM", "time to first token" and "voice agent" in the SEO title, headings and alt text.

### 4.4 What ranks now
From Firecrawl and web search on 3 Nov 2026. This is not a logged-in or Australian Google results page, so treat it as a rough guide. (Data)

- **"hedged requests":**
  - the gRPC request-hedging guide
  - a Medium post, "Request Hedging vs Request Coalescing"
  - blogs (alexoglou, 1pkg)
  - AWS's DynamoDB case study with Global Payments
  - InfoQ's May 2026 adaptive-hedging article
  - the bhope/hedge Go library
  - an r/golang thread
  - the USENIX NSDI 2021 paper "When to Hedge in Interactive Services"
  - Only InfoQ touches LLMs.
- **"reduce LLM latency":**
  - OpenAI's latency optimization guide (ranked first; mentions parallelising, not hedging)
  - a beginner Medium guide
  - an r/LLMDevs thread
  - Azure's LLM Latency Guidebook
  - vendor posts (Runpod, Maxim, Latitude)
- **"voice agent latency":**
  - vendor guides: Twilio, LiveKit, Cresta, AssemblyAI (Vapi build), Retell, SignalWire
  - a Show HN sub-500 ms build
  - a personal blog (rnikhil)
  - All cover latency budgets, streaming and faster models. None covers hedging across providers.

### 4.5 Existing work on hedging or racing LLM requests (read these before writing)
1. **[HOAi, "A simple fix for LLM tail latency"](https://engineering.myhoai.com/posts/a-simple-fix-for-llm-tail-latency/)** (Zhixuan Lai, 10 Jun 2026).
   - On HN on 14 Aug 2026 it got 54 points and 18 comments. [HN thread](https://news.ycombinator.com/item?id=49295179)
   - **What it did:** a phone voice agent that sends every request twice on OpenAI's standard tier, compared with the 2x-priced priority tier, using 50 replayed production requests. TTFT p99 fell from 4.2 s to 1.2 s and complete-response p99 from 9.8 s to 3.5 s.
   - **What it leaves out:** model not named, no cancellation, no cost arithmetic, no hedge-after-delay, single provider.
   - **What HN commenters asked for:**
     - hedge only after a p95 delay, as in Tail at Scale
     - trigger the backup when no first token arrives within about a second
     - why not three copies
     - performance per dollar
     - benchmarks beyond voice
2. **Reddit, June 2025, "How I cut voice chat latency by 23% using parallel LLM API calls".**
   - Raced Gemini 2.5 Flash against GPT-4o. Self-reported average 3.7 s to 2.84 s and P95 24.7 s to 7.8 s (the figures vary between versions of the post).
   - Cross-posted to about five subreddits.
   - Commenters asked about cancelling the loser. (Anecdote)
3. **[InfoQ, "Stragglers, Not Failures"](https://www.infoq.com/articles/adaptive-hedged-requests-p99-latency/)** (Prathamesh Bhope, 28 May 2026).
   - Adaptive hedging: a DDSketch p90 threshold plus a 10% token-bucket budget.
   - Its LLM-streaming section argues you must time the first token, not the response headers.
   - Simulation only; the author says it is not in production.
4. **Libraries and issues.**
   - [bhope/hedge](https://github.com/bhope/hedge) (Go)
   - [hedge-python](https://pypi.org/project/hedge-python/)
   - [hedge-llm](https://github.com/mykolapodpriatov/hedge-llm) (an OpenAI-compatible proxy that races providers and cancels losers)
   - a [SynapseKit HedgedLLM PR](https://github.com/SynapseKit/SynapseKit/pull/1082)
   - a [TTFT-hedging issue](https://github.com/ai-process/ktms/issues/30)
5. **Voice latency measurement.**
   - [Cekura on P99 for voice agents](https://www.cekura.ai/discover/p99-latency-voice-ai-agents)
   - [AssemblyAI on TTFT for voice agents](https://www.assemblyai.com/blog/time-to-first-token-voice-agents)
   - [tianpan.co on time-to-first-audio versus TTFT](https://tianpan.co/blog/2026-06-02-the-voice-agent-slo-defined-in-time-to-first-audio-your-provider-measured-in-time-to-first-token) (2 Jun 2026)
6. **Pipecat.** `LLMSwitcher` and `ServiceSwitcher` support failover when a service errors. They do not race or hedge on slowness. [Docs](https://docs.pipecat.ai/api-reference/server/utilities/service-switchers/llm-switcher), [issue #1795](https://github.com/pipecat-ai/pipecat/issues/1795) (Official)
7. **Gateways.** I found documented fallbacks, retries and priority or latency routing for OpenRouter, LiteLLM and Portkey, but no official hedging feature. (Low confidence: only secondary sources checked)

---

## 5. What makes technical posts succeed

**Backed by Medium's rules (Official)**
- **First-hand experience and original data** are the core of Boost. Medium's own Boosted programming examples are an original how-to, an insider explainer, and a study built on the author's own data.
- **Delivering on the title** now affects pay directly, through the member read-ratio adjustment.
- **Images** should add information, carry alt text, and never replace text.
- **Craft:** develop every point, cite sources, format properly.

**Backed by data**
- **People scan.** NN/g eyetracking (2006, revisited 2017 with 47 participants, reviewed Aug 2026) finds the F-pattern still holds. NN/g's advice: put the key point in the first two paragraphs, start headings with the informative words, bold key phrases, use lists for steps. [NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) (Data)
- **Length.** Total reading time peaked at about 7-minute posts in Medium's 2013 data (old). Chartbeat shows engaged time rising to about 2,000 words. Neither supports padding. (Data, dated)
- **Generic explainers lose search clicks to AI summaries.** See 4.1. (Data)

**Expert consensus**
- **Answer two questions fast**, in the title and first three sentences: is this for me, and what do I get? [Michael Lynch, Refactoring English, Mar 2025](https://refactoringenglish.com/excerpts/write-blog-posts-developers-read/) (Expert: 30+ HN front pages, but one author)
- **Plan the route to readers before writing.** Pick the subreddits, HN and search terms first, and check that similar posts succeed there. (Expert, Lynch)
- **Pictures are the biggest cheap win.** Diagrams, graphs and screenshots, ideally not AI-generated. (Expert, Lynch)
- **Make the post work for skimmers.** The headings and images alone should tell the story. (Expert, Lynch; consistent with NN/g data)
- **Avoid these anti-patterns:** meandering intros, misjudging what readers know, assuming they read earlier posts, stiff formality (Lynch says to write the way you talk), and links used instead of explanations. [Lynch, Oct 2026](https://refactoringenglish.com/blog/anti-patterns-software-blogging/) (Expert)
- **Use a problem, approach, numbers, trade-offs, takeaways structure.** Show the measurement method, so readers can trust and repeat it. Lynch recommends it, and Medium's Boost examples praise how-tos that anticipate readers' questions. (Expert)
- **Be honest about what didn't work.** Humility is praised in Medium's Boost examples, and HN commenters on HOAi immediately probed cost and edge cases. Answer them before they ask. (Expert / Anecdote)
- **Calls to action.** One line at the end: follow, or a link to the code. Medium curators penalise heavy promo blocks. Reads from your subscriber emails pay more, so a light "follow for the next one" is worth it. (Official, staff)

**Popular opinion with weak evidence (use with care)**
- "Numbers in titles get more clicks." Headline studies come mostly from marketing content and suffer from survivorship bias. Numbers are fine on HN when meaningful. (Anecdote)
- "Personal 'I' titles plus data plus screenshots hit the HN front page." Based on 500 surviving posts with no controls. (Anecdote)
- "7 minutes is the magic length" read as a word count. A misreading of 2013 data. (Anecdote)
- "Best time of day to publish on Medium." No data found. (Unverified)

---

## 6. Promotion after publishing

**On Medium (Official)**
- **Email your subscribers.** "Email a link to my subscribers" is pre-selected at publish, and each story can only be emailed once. Reads from email earn at a higher rate. [Help](https://help.medium.com/hc/en-us/articles/360059837393)
- **Friend Links.** If paywalled, use the Friend Link everywhere off Medium. Never put a Friend Link inside the story itself (publication rule). [Help](https://help.medium.com/hc/en-us/articles/360006543813)
- **Track "Presentations".** This stat shows how often Medium suggested your story, which tells you whether you got General or Boost reach. [Help](https://help.medium.com/hc/en-us/articles/360018677974-What-happens-to-your-story-when-you-publish-on-Medium)

**Hacker News (Official unless marked)**
- **Posting your own work.** Allowed occasionally; an account that only submits its own work is treated as promotional. [Guidelines](https://news.ycombinator.com/newsguidelines.html)
- **Title.** Use the article's original title. No editorialising or linkbait; meaningful numbers are fine. So write a Medium title that works on HN as-is.
- **Show HN.** It does not apply to blog posts. Submit as a normal story. [Show HN rules](https://news.ycombinator.com/showhn.html)
- **Paywalls.** OK when a workaround exists, such as a Friend Link. [FAQ](https://news.ycombinator.com/newsfaq.html)
- **Voting.** Never ask anyone to upvote or comment; vote rings get accounts and sites penalised.
- **If it sinks.** You may email hn@ycombinator.com to suggest it for the second-chance pool, or repost after it got no attention. Do not delete and repost. (Official, moderator statements)
- **Timing (Data, conflicting).**
  - [Syften, Oct 2026](https://syften.com/blog/best-time-to-post-on-hacker-news/) (216,816 posts, measured by replies): best was 15:00 to 16:00 UTC, Sundays. That is 2 to 3 am Sydney.
  - A [2019 study](https://chanind.github.io/2019/05/07/best-time-to-submit-to-hacker-news.html) (2018 to 2019 BigQuery data, share of posts reaching 50+ points): Sunday 06:00 UTC was best, because there is less competition. That is 5 pm Sunday Sydney.
  - Either way, be awake for the first two hours to answer comments. (Expert)
- **Medium links on HN (Anecdote).** In 2015 a moderator said medium.com links were mildly down-weighted pending review. That is old.

**Reddit**
- **Sitewide rule.** Mass-posting the same content for exposure counts as spam, and Reddit asks people who mostly post their own links to be thoughtful about frequency. [Reddit Help, Spam](https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam) (Official) The June 2025 five-subreddit cross-post pattern is a risk.
- **Subreddit rules.** Read from a mirror last checked 27 Oct 2026, because Reddit blocked direct access. Recheck each sidebar before posting.

| Subreddit | Rule summary | Fit |
|---|---|---|
| r/LocalLLaMA | Self-promo under 1 in 10 of your posts, disclose affiliation, no LLM-written post text. Karma minimum (undisclosed) since about Apr 2026. | Good, if you write a real self-contained summary |
| r/programming | Bans LLM-written content. AI/LLM topics off-topic unless deeply technical. Technical write-ups OK, product promo not. | Good: this is deeply technical |
| r/LLMDevs | Self-promo rule revised; details unverified | Check first |
| r/MachineLearning | Self-promotion only in the recurring self-promo thread | Thread only |
| r/devops | Self-promo only in the weekly thread. Posts should not just link external blogs. | Weak |
| r/Python | Medium and paywalled links can be banned | Avoid |
| r/AI_Agents | Weekly "Project Display" thread | Thread only |

- **How to post on Reddit (Expert).** Pick two or three subreddits. Write a different post for each: the problem, the chart, the key number, the caveat, then the link. Space them a few days apart, and stay to reply.

**LinkedIn and X (Data, conflicting)**
- **LinkedIn, studies that say links cost reach.**
  - Richard van der Blom's 2026 report (1.3M posts): one body link costs about 19% median reach. Seen secondhand only.
  - Ordinal (900K posts): about 27% less reach with links. Ordinal sells a link-in-comment tool.
- **LinkedIn, evidence the other way.**
  - Saywhat Q1 2026 (397K posts): link posts did better.
  - LinkedIn says it does not deliberately limit link posts.
  - Practical (Inference): post the chart and the story in the post itself, and put the link in the post or first comment. Do not overthink it.
- **X.**
  - Buffer (18.8M posts, Aug 2024 to Aug 2025): non-Premium link posts had 0% median engagement from March 2025. [Buffer](https://buffer.com/resources/links-on-x/)
  - X's head of product said in Apr 2026 that links were never deboosted, and that an in-app browser change now gives link posts the same chance.
  - Practical (Inference): a short thread with the chart, link in a reply.

**Newsletters and communities (Official, each source's own page)**
- **Pipecat Discord:** has a place to share projects. Best-fit audience.
- **SRE Weekly:** accepts human-written submissions by email. Tail latency is squarely on topic.
- **Latent Space "AI News":** submissions at news.latent.space/submit; disclosed self-promotion allowed.
- **PyCoder's Weekly:** submission form; only if the code is Python.
- **Curated with no submission route:** Hacker Newsletter (picks from HN, so HN traction is the way in), TLDR AI and Ben's Bites.

**Cross-posting**
- **When.** After one to two weeks, cross-post to dev.to with `canonical_url` pointing at the Medium story. Optionally Hashnode, with "Add Original URL". (Official mechanics; timing is Inference)
- **Publication rules.** Towards AI and AIGuys want unpublished drafts, so publish on Medium first. AI Advances, Level Up Coding and Data Science Collective accept previously published work. (Official, publication rules)

---

## 7. Pitfalls that throttle or bury an article

1. **AI-written prose, disclosed or not.** Disclosed, it is low-value and kept out of General Distribution. Undisclosed, it is Network only and cannot be paywalled. Reddit's biggest relevant subreddits ban it too. (Official)
2. **Clickbait, or the opposite.** A sensational, vague, "mysterious" or formulaic title or cover blocks Boost. Clickbait blocks General. A title that oversells also gets your pay adjusted down via read ratio. (Official)
3. **Looking like marketing.** Provider praise, sign-up pushes, "sponsored" feel or content marketing count as low-value. Third-party sponsorship inside stories is banned. Naming Together AI and Wafer is fine; selling them is not. (Official)
4. **Promo clutter.** More than one or two self-links at the end, or asking for claps and follows out of nowhere. (Official, staff)
5. **Tag and mention spam.** Off-topic tags, or mass @mentions. (Official)
6. **Image problems.** Copyrighted or watermarked images. AI images without a caption. Text or code inside images. A shocking cover. (Official)
7. **Bad formatting.** Bold lines as headers, raw pasted links, walls of text. (Official, staff)
8. **Unsupported numbers.** Hallucinated or unsourced stats break the rules. Unexplained benchmarks lose HN readers fast. (Official / Expert)
9. **Medium-meta topics.** Network only, and cannot be paywalled. Not relevant here, but avoid asides about Medium. (Official)
10. **Settings you cannot fix later.** The custom slug is locked at publish (Official). The SEO title may be too (Anecdote).
11. **Expecting instant Google traffic.** New accounts can take days to weeks to be indexed. (Official)
12. **Promotion mistakes.**
    - HN: vote rings, an editorialised title, or Show HN for a blog post.
    - Reddit: identical posts to many subreddits, links into subreddits that ban them (r/Python), or link-only posts.
    - (Official)
13. **Buying traffic.** Medium says purchased traffic will not help and can harm a story's standing on Medium and in search. (Official)
14. **Wrong publication.** Submitting to a closed or dormant publication, or one whose topics do not match your tags (the editor sees an off-topic badge). (Official)

---

## For the hedge requests article

**One-line positioning:** the production follow-up to HOAi's post. Same model on two independent providers, hedge-after-delay measured against race-always, real p50/p95/p99 time to first token at production scale, cancellation, and the actual bill.

### Title and subtitle options
All are under 80 characters, so each works unchanged on HN. Replace [X] and [Y] with your real numbers, and use a number only if it is big and solid.

1. **Hedged Requests for LLMs: Cutting Tail Latency in a Production Voice Agent**
   Subtitle: I send each phone-call turn to the same model on two providers and keep whichever streams first. Here are the p50, p95 and p99 numbers, and the bill.
2. **Same Model, Two Providers: Racing LLM Requests to Cut p99 Time to First Token**
   Subtitle: DeepSeek on Together AI and Wafer, first token wins, the loser is cancelled. What it did to latency, what it cost, and where it didn't help.
3. **Race Every Turn or Hedge at p95? LLM Tail Latency in a Real Phone Agent**
   Subtitle: Two ways to apply "The Tail at Scale" to LLM streaming, measured in production: the latency each one buys and the tokens each one burns.
4. **The Caller Remembers the Slowest Turn: Hedging LLM Calls in a Voice Agent**
   Subtitle: Applying Dean and Barroso's hedged requests to time to first token, with production numbers from a real phone agent.
   This is the most "Andy" title, but it leans mysterious, so rely on the SEO title for search.
5. **Hedged LLM Requests: p99 Time to First Token from [X] s to [Y] ms**
   Subtitle: What I learned racing one model across two inference providers in a production voice agent.

**Recommended:** option 1 or 2. They are literal, keyword-led and honest, and they suit Medium's feed, Google and HN's original-title rule. (Inference)

Use the provider's exact model ID (for example "DeepSeek V4.1 Flash") in the body, not necessarily in the title. Google autocomplete currently shows "deepseek v4 flash" variants, so check the exact current name.

### SEO settings
- **SEO title (54 characters):** Hedged Requests for LLMs: Cut Voice Agent Tail Latency
  - Alternative (50 characters): Hedged LLM Requests: Lower p99 Time to First Token
- **SEO description (151 characters):** How I hedge LLM requests across two inference providers to cut p99 time to first token in a production voice agent, with real latency and cost numbers.
- **Custom slug:** hedged-requests-llm-voice-agent-latency

### Tags (five)
1. **LLM** (616K followers): big feed reach.
2. **AI Agent** (708K): big feed reach.
3. **Distributed Systems** (7.1K followers, 18K stories): where hedging readers live.
4. **Voice Ai** (899 stories): an exact, uncrowded tag.
5. **Software Engineering** (4.5M): broad engineering reach.

Swaps if the target publication's topics differ: Large Language Models, Conversational AI, System Design Concepts or Latency. Check the publication's ten topics first to avoid the off-topic badge.

### Target keywords
- **Primary:** hedged requests (+ LLM)
- **Secondary:** time to first token / TTFT, voice agent latency, LLM tail latency / p99 latency, request hedging
- **Long tail, for headings, alt text and body:**
  - reduce LLM latency
  - LLM latency optimization
  - lowest latency LLM provider
  - Pipecat latency
  - voice AI latency
  - LLM fallback (to contrast with hedging)
  - The Tail at Scale

Put the primary and one secondary term in the SEO title, the first paragraph, one H2 and one alt text. Do not stuff them anywhere else.

### The content gap
What nobody has published yet, in priority order:

1. **Production scale.** Thousands of real turns, not 50 replays or a simulation. Show the full distribution (a CDF or histogram), not just three percentiles.
2. **Cross-provider, same model.** This isolates provider variance from model variance. Explain why that matters: identical behaviour and tool calls, so the winner's answer is interchangeable.
3. **Race-always versus hedge-after-delay.** Measured side by side: latency gained against extra requests and tokens. This is the question HN commenters asked HOAi, and nobody has answered it with LLM data.
4. **The real bill.**
   - What a cancelled stream still costs: prompt or prefill tokens, plus output tokens generated before the cancel, per provider.
   - Cost per call and per minute of conversation.
5. **Measuring correctly.** Time the first content token, not response headers or keep-alives; InfoQ shows header timing misleads. Keep connections warm.
6. **Failure modes.** Correlated slowness (both providers slow at once), rate limits doubling, one provider erroring, and how hedging interacts with fallbacks.
7. **Pipecat integration.** Pipecat's switchers fail over on errors only. Show where a hedging wrapper sits in the pipeline.
8. **Where else it pays off.** STT and TTS: report only what you measured, and say what you have not tested.

### Recommended outline (~2,200 words, 9 to 10 minutes)
1. **Hook** (60 to 80 words). The caller remembers the slowest turn, not the average one.
   - One real number: how often a turn stalled, and for how long.
   - One sentence on the result.
   - Optionally the HOAi-style maths: with N turns per call, a 1% slow rate means about a 1 - 0.99^N chance per call of hitting one.
2. **The problem in production numbers** (250 words).
   - Your TTFT distribution before hedging, as a chart.
   - Define TTFT and p95/p99 once, plainly.
3. **The idea, from "The Tail at Scale"** (200 words).
   - Dean and Barroso (2013): send a backup copy after about the p95 latency and take whichever answers first.
   - A plain analogy, such as joining a second checkout queue when yours stalls.
   - Credit HOAi's post and say how yours differs.
4. **What I built** (350 words).
   - A diagram: Pipecat pipeline, then the hedge wrapper, then Together AI and Wafer; the first token wins and the loser is cancelled.
   - A 20 to 30 line code snippet, with the full code linked.
   - Why the same model on two providers, not two models.
5. **Race every turn versus hedge after a delay** (400 words).
   - One small table: p50, p95 and p99 TTFT, % of turns hedged, extra tokens, cost per call.
   - A CDF chart of the two strategies against the baseline.
6. **Cancelling the loser, and what you still pay** (250 words).
   - What each provider bills for a cancelled stream, measured or from their docs (cite them).
   - How cancellation works mid-stream.
7. **What didn't work, and the surprises** (250 words).
   - Correlated slow periods, rate limits, header-versus-token timing, cold connections.
   - Be specific and honest.
8. **Where else it might pay off** (150 words). STT and TTS: what you tried, and what you have not.
9. **Should you do it?** (150 words).
   - Your plain recommendation and when not to bother: low traffic, a single-provider contract, tight budgets.
   - A three-line checklist.
10. **Takeaways** (three lines). One line inviting a follow or linking the repo.

**Visuals** (all original, 1,200 px or wider, alt text and a takeaway caption on each):
- the TTFT distribution before and after (cover candidate)
- a hedge timeline diagram (two lanes, a cancel marker)
- the cost per call comparison

### Publication and paywall plan (Inference)
- **Paywall:** free (not paywalled) for this first article. See 1.8.
- **Publication:**
  - First, submit to **AI Advances** or **Towards AI**. Towards AI needs it unpublished, so submit before publishing anywhere.
  - Fallbacks: **ITNEXT** or **Level Up Coding**.
  - If nobody accepts within about a week, self-publish on your profile. Distribution rules are the same; you just lose the publication's followers.
- **Before launch day:** spend a week following and leaving a few genuine replies on Pipecat and LLM-latency stories. It helps the Google indexing threshold. (Official: Medium says engagement helps)

### Launch sequence (Inference, built from sections 6 and 7)
1. **Day 0, when the publication publishes:** subscriber email goes out. Post the native chart-led version on LinkedIn and X.
2. **Day 0 or 1:** submit to HN with the exact title, then stay for two hours to answer the cost and threshold questions.
3. **Days 1 to 5:** one tailored post each on r/LocalLLaMA and r/programming, then r/LLMDevs if its rules allow. Post in the Pipecat Discord showcase, email SRE Weekly, and submit to Latent Space AI News.
4. **Days 7 to 14:** cross-post to dev.to with the canonical pointing at Medium. Check "Presentations" and Google Search indexing.

---

## Could not verify, or may be out of date

- **SEO field limits inside Medium's More settings.** Not checked logged in. The 60/156 figures come from Medium's 2020 and 2021 guidance.
- **Whether the paywall affects Boost in 2026.** The help page saying it did not was removed with the nomination programme.
- **Editor Partner Program help page.** Behind a sign-in wall. There is no public list of member publications, and only AI Advances says publicly that it is in.
- **Tag follower counts.** These are as Medium displayed them. Voice Ai at 66 followers for 899 stories looks low, but may be right.
- **Search volumes.** I had no keyword tool. Autocomplete shows demand exists, not size. "What ranks" came from non-Google, non-Australian search results.
- **Reddit rules.** Read via a mirror (checked 27 Oct 2026); Reddit blocked direct access. r/LLMDevs, r/ExperiencedDevs, r/softwarearchitecture, r/sre and the voice-agent subreddits are unverified.
- **LinkedIn link-reach effect.** The studies conflict, and the van der Blom 2026 figure was seen secondhand.
- **SEO title after publishing.** Whether it is locked is one Reddit report.
- **Hedging in OpenRouter, LiteLLM and Portkey.** No official hedging feature found; secondary sources only.
- **HN's 80-character title limit.** Not re-checked this session.
- **Medium's Google traffic trend.** Third-party estimates only.
- **Publication response times and "open" status.** As each publication states them; untested.
