import httpx


def search(keywords: list[str], max_results: int = 5) -> list[dict]:
    query = " ".join(keywords)
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": query, "tags": "story", "hitsPerPage": max_results}

    try:
        resp = httpx.get(url, params=params, timeout=10)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
    except Exception as e:
        return [{"error": str(e)}]

    results = []
    for hit in hits:
        results.append({
            "title": hit.get("title") or "",
            "points": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "date": (hit.get("created_at") or "")[:10],
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "author": hit.get("author") or "",
        })

    return results
