import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "worldcup_2026.json"
GENERATOR = ROOT / "scripts" / "generate_dashboard.py"


def fetch_text(url):
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 FIFA-2026-local-dashboard/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=30) as response:
        raw = response.read()
    return raw.decode("utf-8", errors="replace")


def compact_text(html):
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#8217;|&rsquo;", "'", text)
    text = re.sub(r"&amp;", "&", text)
    return re.sub(r"\s+", " ", text)


def find_score(text, home, away):
    # SB Nation currently formats results as "Mexico 2, South Africa 0".
    patterns = [
        rf"{re.escape(home)}\s+(\d+)\s*,\s*{re.escape(away)}\s+(\d+)",
        rf"{re.escape(away)}\s+(\d+)\s*,\s*{re.escape(home)}\s+(\d+)",
    ]
    for index, pattern in enumerate(patterns):
        match = re.search(pattern, text, flags=re.I)
        if not match:
            continue
        first, second = int(match.group(1)), int(match.group(2))
        if index == 0:
            return first, second
        return second, first
    return None


def reset_table(group):
    for team in group["teams"]:
        team.update({"w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "gd": 0, "pts": 0})


def apply_match(group, match):
    home = next(team for team in group["teams"] if team["team"] == match["home"])
    away = next(team for team in group["teams"] if team["team"] == match["away"])
    hs, away_score = match["home_score"], match["away_score"]
    home["gf"] += hs
    home["ga"] += away_score
    away["gf"] += away_score
    away["ga"] += hs
    if hs > away_score:
        home["w"] += 1
        away["l"] += 1
        home["pts"] += 3
    elif hs < away_score:
        away["w"] += 1
        home["l"] += 1
        away["pts"] += 3
    else:
        home["d"] += 1
        away["d"] += 1
        home["pts"] += 1
        away["pts"] += 1


def recalc_group(group):
    reset_table(group)
    for match in group["matches"]:
        if match.get("status") == "finished":
            apply_match(group, match)
    for team in group["teams"]:
        team["gd"] = team["gf"] - team["ga"]
    group["teams"].sort(key=lambda team: (-team["pts"], -team["gd"], -team["gf"], team["team"]))


def update_from_sources(data, dry_run=False):
    pages = []
    for url in [data["source"]["standings_url"], data["source"]["schedule_url"]]:
        pages.append(compact_text(fetch_text(url)))
    source_text = " ".join(pages)

    changed = []
    for group in data["groups"]:
        for match in group["matches"]:
            score = find_score(source_text, match["home"], match["away"])
            if not score:
                continue
            old = (match.get("home_score"), match.get("away_score"), match.get("status"))
            match["home_score"], match["away_score"] = score
            match["status"] = "finished"
            new = (match["home_score"], match["away_score"], match["status"])
            if old != new:
                changed.append(f'{group["name"]} 組：{match["home"]} {score[0]}-{score[1]} {match["away"]}')

    for group in data["groups"]:
        recalc_group(group)

    data["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if not dry_run:
        DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.run([sys.executable, str(GENERATOR)], check=True)
    return changed


def main():
    parser = argparse.ArgumentParser(description="從公開比分頁更新 FIFA World Cup 26 儀表板。")
    parser.add_argument("--dry-run", action="store_true", help="只抓取並回報變更，不寫入檔案。")
    args = parser.parse_args()

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    changed = update_from_sources(data, dry_run=args.dry_run)
    if changed:
        print("已更新賽事：")
        for item in changed:
            print(f"- {item}")
    else:
        print("目前沒有新的完賽比分。")


if __name__ == "__main__":
    main()
