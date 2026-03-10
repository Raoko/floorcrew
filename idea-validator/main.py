#!/usr/bin/env python3
"""
Idea Validator — research agent that checks if a hackathon idea already exists.
Searches GitHub, HN, and Reddit/Twitter (via Grok) in parallel, then synthesizes
a landscape report using Claude.

Usage:
  python main.py "your idea description"
  python main.py   # interactive prompt
"""

import os
import sys
import json
import hashlib
import time
import concurrent.futures
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.config' / 'keys'))
from keys import load_into_env
import anthropic
from rich.console import Console
from rich.rule import Rule
from rich.panel import Panel

from search import github, hn, grok
from synthesize import extract_keywords, synthesize

load_into_env()
console = Console()

CACHE_DIR = Path.home() / ".cache" / "idea-validator"
CACHE_TTL = 60 * 60 * 24  # 24 hours


def _cache_key(keywords: list[str]) -> str:
    return hashlib.md5("|".join(sorted(keywords)).encode()).hexdigest()


def load_cache(keywords: list[str]) -> dict | None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{_cache_key(keywords)}.json"
    if path.exists() and (time.time() - path.stat().st_mtime) < CACHE_TTL:
        return json.loads(path.read_text())
    return None


def save_cache(keywords: list[str], data: dict) -> None:
    path = CACHE_DIR / f"{_cache_key(keywords)}.json"
    path.write_text(json.dumps(data))


def run_searches(keywords: list[str]) -> tuple[list, list, str]:
    """Run GitHub, HN, and Grok searches in parallel using threads."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        gh_future = executor.submit(github.search, keywords)
        hn_future = executor.submit(hn.search, keywords)
        grok_future = executor.submit(grok.search, keywords)

        gh_results = gh_future.result()
        hn_results = hn_future.result()
        grok_summary = grok_future.result()

    return gh_results, hn_results, grok_summary


def print_github(results: list[dict]) -> None:
    console.print(Rule("[bold cyan]GitHub[/bold cyan]"))
    if not results:
        console.print("  No repos found.")
        return
    if "error" in results[0]:
        console.print(f"  [red]Error: {results[0].get('error', 'unknown')}[/red]")
        return
    for r in results:
        archived = " [ARCHIVED]" if r.get("archived") else ""
        console.print(
            f"  [bold]{r['name']}[/bold]{archived} — "
            f"stars: {r['stars']} | last push: {r['last_push']} | {r['language']}"
        )
        if r["description"]:
            console.print(f"    {r['description'][:100]}")
        console.print(f"    [dim]{r['url']}[/dim]")


def print_hn(results: list[dict]) -> None:
    console.print(Rule("[bold yellow]Hacker News[/bold yellow]"))
    if not results:
        console.print("  No posts found.")
        return
    if "error" in results[0]:
        console.print(f"  [red]Error: {results[0].get('error', 'unknown')}[/red]")
        return
    for r in results:
        console.print(
            f"  [bold]{r['title']}[/bold] "
            f"({r['date']}, {r['points']} pts, {r['comments']} comments)"
        )
        console.print(f"    [dim]{r['url']}[/dim]")


def print_grok(summary: str) -> None:
    console.print(Rule("[bold magenta]Reddit / Twitter via Grok[/bold magenta]"))
    console.print(summary)


def main():
    save_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    if args:
        idea = " ".join(args)
    else:
        console.print("[bold]Idea Validator[/bold] — paste your idea and press Enter:")
        idea = input("> ").strip()
        if not idea:
            console.print("[red]No idea provided.[/red]")
            sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    console.print()
    console.print(Panel(f"[bold]{idea}[/bold]", title="Validating Idea", border_style="blue"))
    console.print()

    # Step 1: extract keywords
    with console.status("Extracting keywords..."):
        keywords = extract_keywords(client, idea)
    console.print(f"[dim]Keywords:[/dim] {', '.join(keywords)}")
    console.print()

    # Step 2: parallel searches (with cache)
    cached = load_cache(keywords)
    if cached:
        console.print("[dim](using cached search results — run with --no-cache to refresh)[/dim]\n")
        gh_results = cached["github"]
        hn_results = cached["hn"]
        grok_summary = cached["grok"]
    else:
        with console.status("Searching GitHub, HN, and Grok in parallel..."):
            gh_results, hn_results, grok_summary = run_searches(keywords)
        save_cache(keywords, {"github": gh_results, "hn": hn_results, "grok": grok_summary})

    print_github(gh_results)
    console.print()
    print_hn(hn_results)
    console.print()
    print_grok(grok_summary)
    console.print()

    # Step 3: synthesize
    with console.status("Synthesizing landscape report..."):
        report = synthesize(client, idea, keywords, gh_results, hn_results, grok_summary)

    console.print(Rule("[bold green]Synthesis[/bold green]"))
    console.print(report)
    console.print()

    if save_json:
        output = {
            "idea": idea,
            "keywords": keywords,
            "github": gh_results,
            "hn": hn_results,
            "grok": grok_summary,
            "synthesis": report,
        }
        out_path = Path(f"report-{_cache_key(keywords)[:8]}.json")
        out_path.write_text(json.dumps(output, indent=2))
        console.print(f"[dim]JSON saved to {out_path}[/dim]")


if __name__ == "__main__":
    main()
