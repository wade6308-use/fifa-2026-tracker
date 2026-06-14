import json
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "worldcup_2026.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "update-dashboard.yml"

sys.path.insert(0, str(ROOT / "scripts"))
import generate_dashboard  # noqa: E402


def cron_for(dt):
    return f'{dt.minute} {dt.hour} {dt.day} {dt.month} *'


def ascii_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def build_schedules(data):
    schedules = {}
    missing = []
    for group in data["groups"]:
        for match in group["matches"]:
            iso = generate_dashboard.kickoff_iso(match)
            label = ascii_text(f'Group {group["name"]}: {match["home"]} vs {match["away"]}')
            if not iso:
                missing.append(label)
                continue

            kickoff = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            for offset, suffix in ((0, "kickoff"), (3, "kickoff +3h")):
                dt = kickoff + timedelta(hours=offset)
                schedules.setdefault(cron_for(dt), []).append(f"{suffix} - {label}")

    return dict(sorted(schedules.items(), key=lambda item: tuple(map(int, item[0].split()[:4]))[3::-1])), missing


def replace_schedule_block(workflow, schedules):
    lines = [
        "  schedule:",
        "    # Auto-generated from group-stage kickoff times.",
        "    # Runs at every match kickoff and again 3 hours after kickoff.",
        "    # Times are UTC because GitHub Actions cron uses UTC.",
    ]
    for cron, labels in schedules.items():
        sample = labels[0]
        extra = f" (+{len(labels) - 1} more)" if len(labels) > 1 else ""
        lines.append(f'    # {sample}{extra}')
        lines.append(f'    - cron: "{cron}"')
    new_block = "\n".join(lines)

    start = workflow.index("  schedule:")
    end = workflow.index("\n\npermissions:", start)
    return workflow[:start] + new_block + workflow[end:]


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    schedules, missing = build_schedules(data)
    if missing:
        print("Missing kickoff times:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    WORKFLOW_PATH.write_text(replace_schedule_block(workflow, schedules), encoding="utf-8", newline="\n")
    print(f"Updated {WORKFLOW_PATH} with {len(schedules)} unique cron schedules.")


if __name__ == "__main__":
    main()
