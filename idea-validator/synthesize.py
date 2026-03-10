import re
import anthropic
import json


def extract_keywords(client: anthropic.Anthropic, idea: str) -> list[str]:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": (
                f"Extract 3-5 short search keywords from this idea description. "
                f"Return only a JSON array of strings, nothing else.\n\nIdea: {idea}"
            ),
        }],
    )
    text = resp.content[0].text.strip()
    # extract JSON array robustly — handles fences, leading/trailing text
    match = re.search(r"\[.*?\]", text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract keyword array from response: {text}")
    return json.loads(match.group())


def synthesize(
    client: anthropic.Anthropic,
    idea: str,
    keywords: list[str],
    github_results: list[dict],
    hn_results: list[dict],
    grok_summary: str,
) -> str:
    context = f"""
IDEA: {idea}

KEYWORDS USED: {", ".join(keywords)}

GITHUB RESULTS:
{json.dumps(github_results, indent=2)}

HACKER NEWS RESULTS:
{json.dumps(hn_results, indent=2)}

REDDIT / TWITTER (via Grok):
{grok_summary}
"""

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": (
                "You are an expert at evaluating whether a software idea is novel, overcrowded, or has a real gap.\n\n"
                "Given the following research data, produce a landscape report with:\n"
                "1. Verdict: one of — Already Solved / Active Competition / Niche Gap / Wide Open / Abandoned Territory\n"
                "2. Maturity signal: how mature are existing solutions?\n"
                "3. Key existing projects or discussions worth knowing\n"
                "4. The gap: what is NOT being addressed that this idea could own?\n"
                "5. Recommended angle: 1-2 sentences on how to differentiate\n\n"
                "Be direct. No filler. Use bullet points.\n\n"
                + context
            ),
        }],
    )
    return resp.content[0].text
