import os
from openai import OpenAI


def search(keywords: list[str]) -> str:
    """
    Uses Grok with live web search to find Reddit and Twitter/X discussions.
    Returns raw text summary from Grok.
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "XAI_API_KEY not set — skipping Grok search."

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    keyword_str = ", ".join(keywords)
    prompt = (
        f"Search Reddit and Twitter/X for discussions about: {keyword_str}\n\n"
        "Find:\n"
        "1. Reddit threads where people discuss building or wanting this kind of tool\n"
        "2. Twitter/X posts from builders, researchers, or ops people mentioning it\n"
        "3. Any strong signals that this is a solved problem, an open problem, or an ignored problem\n\n"
        "Return a short summary (5-10 bullet points max). Focus on signal, not noise."
    )

    try:
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[{"role": "user", "content": prompt}],
            search_parameters={"mode": "on"},
        )
        return response.choices[0].message.content or "No results."
    except Exception as e:
        return f"Grok search error: {e}"
