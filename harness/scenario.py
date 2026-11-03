"""A made-up outbound voice-agent call, sized like a real one: a ~12k-token system prompt (script plus knowledge base),
a call in progress, and a rotating last caller line. Nothing here is from a real business or a real caller."""

import random

AGENT = "Mia"
COMPANY = "Brightline Solar"

SCRIPT = f"""You are {AGENT}, calling on behalf of {COMPANY}, a residential solar and battery installer in New South Wales.
You are on a live phone call. Everything you write is spoken aloud by a text-to-speech voice, so:
- Reply in one or two short sentences, the way people talk on the phone. Never more than about 30 words.
- No lists, no markdown, no emojis, no URLs. Say numbers the way a person would ("about six and a half kilowatts").
- Ask one question at a time and wait for the answer.
- Never quote a price, a rebate amount or a payback period as a promise. Say a consultant will confirm it.
- If the caller asks to stop, says they are busy, or asks not to be called again, thank them and call end_call.
- If you did not catch what they said, ask them to repeat it briefly. Never guess an address or a number.

The call has five steps. Move through them in order, but follow the caller if they jump ahead.
1. Confirm you are speaking with the person who asked for a quote, and that now is an OK time.
2. Confirm the property: suburb, whether they own it, roof type, and roughly how many storeys.
3. Understand their usage: their last quarterly power bill, whether someone is home during the day, any EV or pool.
4. Gauge interest in a battery and their rough timing.
5. Book a free roof assessment with a consultant, or arrange a callback time. Then close warmly and call end_call.

Tone: friendly, relaxed, Australian, never pushy. Use the caller's first name now and then, not every turn.
Use the knowledge base below to answer questions. If the answer is not in it, say the consultant will cover it."""


def _catalogue(rng):
    panels = ["Aurora", "Kestrel", "Meridian", "Tasman", "Coral", "Summit", "Harbour", "Outback"]
    kinds = [("panel", "W", (400, 480)), ("inverter", "kW", (3, 10)), ("battery", "kWh", (5, 20))]
    rows = []
    for i in range(48):
        kind, unit, (lo, hi) = kinds[i % 3]
        name = f"{rng.choice(panels)} {kind.title()} {rng.randint(100, 999)}"
        size = rng.randint(lo, hi)
        warranty = rng.choice([10, 12, 15, 20, 25])
        rows.append(
            f"- {name}: {size} {unit} {kind}. Product warranty {warranty} years. "
            f"{rng.choice(['Tier one manufacturer.', 'Made in Asia, assembled in Australia.', 'Popular for small roofs.', 'Best seller this year.'])} "
            f"{rng.choice(['Works with all our inverters.', 'Needs a hybrid inverter for battery backup.', 'Comes with a monitoring app.', 'Rated for coastal areas.'])} "
            f"Typical lead time {rng.randint(1, 6)} weeks."
        )
    return "PRODUCT CATALOGUE\n" + "\n".join(rows)


def _faq(rng):
    topics = [
        ("How long does an install take?", "Most homes take one day. Two-storey homes or tile roofs can take two."),
        ("Do I need council approval?", "Usually not for a standard rooftop system. The consultant checks heritage areas."),
        ("What happens on a cloudy day?", "Panels still produce, just less. The battery covers the evening peak."),
        ("Can I add a battery later?", "Yes. We fit a battery-ready inverter so adding one later is simple."),
        ("Is there a rebate?", "There may be federal and state incentives. The consultant confirms what applies to you."),
        ("Do you offer finance?", "Yes, through partner lenders. The consultant walks through the options, no obligation."),
        ("What maintenance is needed?", "Very little. A visual check each year and a clean if the panels get dusty."),
        ("Will it work in a blackout?", "Only with a battery and backup circuit. Panels alone switch off for safety."),
        ("How do I monitor it?", "Through the app. You see what the panels make and what the house uses."),
        ("Who does the install?", "Our own accredited electricians. We do not subcontract installs."),
        ("What about my roof warranty?", "We use mounting systems approved for each roof type and seal every penetration."),
        ("How much will I save?", "It depends on usage and timing. The consultant models it from your bills."),
    ]
    out = []
    for i in range(72):
        q, a = topics[i % len(topics)]
        detail = rng.choice([
            "Mention this only if they ask.", "Keep it to one sentence on the phone.",
            "If they push for numbers, say the consultant will confirm.", "This comes up a lot with retirees.",
            "Young families often ask this.", "Landlords ask this for rentals.",
        ])
        out.append(f"Q{i + 1}. {q}\nA. {a} {detail} (Region note {rng.randint(1, 40)}: install crews cover this area {rng.choice(['daily', 'twice a week', 'weekly'])}.)")
    return "FREQUENTLY ASKED QUESTIONS\n" + "\n".join(out)


def _service_areas(rng):
    suburbs = ["Parramatta", "Penrith", "Hornsby", "Cronulla", "Blacktown", "Campbelltown", "Gosford", "Wollongong",
               "Newcastle", "Maitland", "Richmond", "Camden", "Liverpool", "Chatswood", "Manly", "Bankstown"]
    rows = []
    for i in range(64):
        s = suburbs[i % len(suburbs)]
        rows.append(f"- {s} zone {i // len(suburbs) + 1}: next assessment slot in {rng.randint(1, 9)} days, "
                    f"crew base {rng.choice(suburbs)}, {rng.choice(['tile and tin roofs', 'mostly tin roofs', 'many two-storey homes', 'strata needs approval'])}.")
    return "SERVICE AREAS AND AVAILABILITY\n" + "\n".join(rows)


def system_prompt() -> str:
    rng = random.Random(7)  # fixed, so every run sends byte-identical prompts and the hosts can cache them
    background = (f"BACKGROUND FOR THIS CALL (not said by the caller)\nYou are ringing Sam Example, who asked for a solar quote "
                  f"on the website on 28 Oct 2026. Earlier calls: none. Time now: Tuesday, 10:12 am in Sydney.")
    parts = [SCRIPT, _catalogue(rng), _faq(rng), _service_areas(rng), _faq(rng), _catalogue(rng), background]
    return "\n\n".join(parts)


HISTORY = [
    ("assistant", "Hi, is that Sam?"),
    ("user", "Yeah, speaking."),
    ("assistant", f"Hi Sam, it's {AGENT} from {COMPANY}. You asked about a solar quote on our website. Is now an OK time for a couple of minutes?"),
    ("user", "Yeah, go on."),
    ("assistant", "Great. Just so you know, this call is recorded. Which suburb is the house in?"),
    ("user", "Penrith."),
    ("assistant", "Lovely. And do you own the place?"),
    ("user", "Yep, we own it."),
    ("assistant", "Good stuff. Is it a tile roof or a tin roof?"),
    ("user", "Tile, I think. Single storey."),
    ("assistant", "No worries. Roughly what was your last quarterly power bill?"),
    ("user", "Around nine hundred bucks, maybe a bit more."),
    ("assistant", "That's a fair bit. Is someone usually home during the day?"),
]

CALLER_LINES = [
    "Yeah, my wife works from home most days.",
    "Sorry, what was that?",
    "Not really, we're both at work.",
    "We've got a pool too, if that matters.",
    "How much would a battery cost?",
    "Who did you say you were with again?",
    "Look, I'm a bit busy right now, can you call back later?",
    "We're thinking of getting an EV next year.",
]

END_CALL_TOOL = {
    "type": "function",
    "function": {
        "name": "end_call",
        "description": "Hang up after closing the call politely.",
        "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]},
    },
}


def messages(caller_line: str) -> list[dict]:
    return [{"role": "system", "content": system_prompt()}, *({"role": r, "content": c} for r, c in HISTORY),
            {"role": "user", "content": caller_line}]
