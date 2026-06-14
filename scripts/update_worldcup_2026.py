import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "worldcup_2026.json"
GENERATOR = ROOT / "scripts" / "generate_dashboard.py"
FIFA_MATCHES_URL = "https://api.fifa.com/api/v3/calendar/matches?language=en&count=500&idCompetition=17&idSeason=285023"
FIFA_NAME_MAP = {
    "Congo DR": "DR Congo",
    "Côte d'Ivoire": "Ivory Coast",
    "Curaçao": "Curacao",
    "IR Iran": "Iran",
    "Korea Republic": "South Korea",
    "USA": "United States",
}


def fetch_json(url):
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 FIFA-2026-dashboard/1.0",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=30) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8", errors="replace"))


def localized_description(values):
    if not values:
        return ""
    for value in values:
        if value.get("Locale", "").lower() in {"en-gb", "en"}:
            return value.get("Description", "")
    return values[0].get("Description", "")


def canonical_team(name):
    return FIFA_NAME_MAP.get(name, name)


def fifa_team_name(team):
    if not team:
        return None
    name = team.get("ShortClubName") or localized_description(team.get("TeamName"))
    return canonical_team(name)


def match_key(home, away):
    return (canonical_team(home), canonical_team(away))


def fifa_matches_by_key(fifa_data):
    matches = {}
    for item in fifa_data.get("Results", []):
        home = fifa_team_name(item.get("Home"))
        away = fifa_team_name(item.get("Away"))
        if home and away:
            matches[match_key(home, away)] = item
    return matches


def reset_table(group):
    for team in group["teams"]:
        team.update({"w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "gd": 0, "pts": 0})


def apply_match(group, match):
    home = next(team for team in group["teams"] if team["team"] == match["home"])
    away = next(team for team in group["teams"] if team["team"] == match["away"])
    home_score, away_score = match["home_score"], match["away_score"]
    home["gf"] += home_score
    home["ga"] += away_score
    away["gf"] += away_score
    away["ga"] += home_score
    if home_score > away_score:
        home["w"] += 1
        away["l"] += 1
        home["pts"] += 3
    elif home_score < away_score:
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


def fifa_status(item):
    has_score = item.get("HomeTeamScore") is not None and item.get("AwayTeamScore") is not None
    if has_score and item.get("ResultType") == 1:
        return "finished"
    if has_score:
        return "live"
    return "scheduled"


def update_from_sources(data, dry_run=False):
    fifa_url = data.get("source", {}).get("fifa_matches_url", FIFA_MATCHES_URL)
    fifa_matches = fifa_matches_by_key(fetch_json(fifa_url))

    changed = []
    missing = []
    for group in data["groups"]:
        for match in group["matches"]:
            key = match_key(match["home"], match["away"])
            fifa_match = fifa_matches.get(key)
            if not fifa_match:
                missing.append(f'Group {group["name"]}: {match["home"]} vs {match["away"]}')
                continue

            status = fifa_status(fifa_match)
            home_score = fifa_match.get("HomeTeamScore")
            away_score = fifa_match.get("AwayTeamScore")
            if status == "scheduled":
                home_score = None
                away_score = None

            old = (match.get("home_score"), match.get("away_score"), match.get("status"))
            match["home_score"] = home_score
            match["away_score"] = away_score
            match["status"] = status
            new = (match["home_score"], match["away_score"], match["status"])
            if old != new:
                score_text = "scheduled"
                if home_score is not None and away_score is not None:
                    score_text = f"{home_score}-{away_score}"
                changed.append(f'Group {group["name"]}: {match["home"]} {score_text} {match["away"]} ({status})')

    for group in data["groups"]:
        recalc_group(group)

    if missing:
        print("Warning: FIFA API matches not found for:")
        for item in missing:
            print(f"- {item}")

    if not changed:
        return changed

    data["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data["source"] = {"fifa_matches_url": FIFA_MATCHES_URL}
    if not dry_run:
        DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.run([sys.executable, str(GENERATOR)], check=True)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Update the FIFA World Cup 26 dashboard from FIFA's public match API.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report changes without writing files.")
    args = parser.parse_args()

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    changed = update_from_sources(data, dry_run=args.dry_run)
    if changed:
        print("Updated matches:")
        for item in changed:
            print(f"- {item}")
    else:
        print("No new match updates found.")


if __name__ == "__main__":
    main()
