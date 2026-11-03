"""The race from the article, as printed there: every host gets the turn at once, the first to send real words wins."""

import asyncio, json, httpx

async def open_reply(client, host, body):
    """Start a streamed reply on one host; return once it sends real words."""
    request = client.build_request(
        "POST", host["url"], json={**body, "model": host["model"], "stream": True},
        headers={"Authorization": f"Bearer {host['key']}"})
    response = await client.send(request, stream=True)
    response.raise_for_status()
    lines = response.aiter_lines()
    async for line in lines:
        if not line.startswith("data: ") or line == "data: [DONE]":
            continue
        choices = json.loads(line[6:]).get("choices") or [{}]
        delta = choices[0].get("delta", {})
        if (delta.get("content") or "").strip() or delta.get("tool_calls"):
            return host, response, lines, delta  # the winner keeps streaming from here
    await response.aclose()
    raise RuntimeError(f"{host['name']} sent an empty reply")


async def race(client, hosts, body, first_word_timeout=2.0):
    tasks = [asyncio.create_task(open_reply(client, h, body)) for h in hosts]
    winner = None
    try:
        for next_done in asyncio.as_completed(tasks, timeout=first_word_timeout):
            try:
                winner = await next_done
                return winner
            except Exception:
                continue  # a failed host only loses this race
        raise RuntimeError("every host failed")
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()  # still waiting: cancelling closes its stream
            elif not task.cancelled() and task.exception() is None and task.result() is not winner:
                await task.result()[1].aclose()  # finished at the same moment: close it too
