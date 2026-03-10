import os
import httpx


def search(keywords: list[str], max_results: int = 5) -> list[dict]:
    query = " ".join(keywords)
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": max_results}

    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
    except Exception as e:
        return [{"error": str(e)}]

    results = []
    for item in items:
        results.append({
            "name": item.get("full_name"),
            "stars": item.get("stargazers_count", 0),
            "description": item.get("description") or "",
            "last_push": item.get("pushed_at", "")[:10],
            "url": item.get("html_url"),
            "language": item.get("language") or "unknown",
            "archived": item.get("archived", False),
        })

    return results
