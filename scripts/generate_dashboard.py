import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "worldcup_2026.json"
HTML_PATH = ROOT / "index.html"

TEAM_ZH = {
    "Mexico": "墨西哥",
    "South Korea": "韓國",
    "Czechia": "捷克",
    "South Africa": "南非",
    "Canada": "加拿大",
    "Bosnia and Herzegovina": "波士尼亞與赫塞哥維納",
    "Qatar": "卡達",
    "Switzerland": "瑞士",
    "Brazil": "巴西",
    "Morocco": "摩洛哥",
    "Haiti": "海地",
    "Scotland": "蘇格蘭",
    "United States": "美國",
    "Paraguay": "巴拉圭",
    "Australia": "澳洲",
    "Turkiye": "土耳其",
    "Türkiye": "土耳其",
    "T羹rkiye": "土耳其",
    "Germany": "德國",
    "Curacao": "庫拉索",
    "Ivory Coast": "象牙海岸",
    "Ecuador": "厄瓜多",
    "Netherlands": "荷蘭",
    "Japan": "日本",
    "Sweden": "瑞典",
    "Tunisia": "突尼西亞",
    "Belgium": "比利時",
    "Egypt": "埃及",
    "Iran": "伊朗",
    "New Zealand": "紐西蘭",
    "Spain": "西班牙",
    "Cabo Verde": "維德角",
    "Saudi Arabia": "沙烏地阿拉伯",
    "Uruguay": "烏拉圭",
    "France": "法國",
    "Senegal": "塞內加爾",
    "Iraq": "伊拉克",
    "Norway": "挪威",
    "Argentina": "阿根廷",
    "Algeria": "阿爾及利亞",
    "Austria": "奧地利",
    "Jordan": "約旦",
    "Portugal": "葡萄牙",
    "DR Congo": "剛果民主共和國",
    "Uzbekistan": "烏茲別克",
    "Colombia": "哥倫比亞",
    "England": "英格蘭",
    "Croatia": "克羅埃西亞",
    "Ghana": "迦納",
    "Panama": "巴拿馬",
}

TEAM_FLAG_CODE = {
    "Mexico": "mx",
    "South Korea": "kr",
    "Czechia": "cz",
    "South Africa": "za",
    "Canada": "ca",
    "Bosnia and Herzegovina": "ba",
    "Qatar": "qa",
    "Switzerland": "ch",
    "Brazil": "br",
    "Morocco": "ma",
    "Haiti": "ht",
    "Scotland": "gb-sct",
    "United States": "us",
    "Paraguay": "py",
    "Australia": "au",
    "Turkiye": "tr",
    "Türkiye": "tr",
    "Germany": "de",
    "Curacao": "cw",
    "Ivory Coast": "ci",
    "Ecuador": "ec",
    "Netherlands": "nl",
    "Japan": "jp",
    "Sweden": "se",
    "Tunisia": "tn",
    "Belgium": "be",
    "Egypt": "eg",
    "Iran": "ir",
    "New Zealand": "nz",
    "Spain": "es",
    "Cabo Verde": "cv",
    "Saudi Arabia": "sa",
    "Uruguay": "uy",
    "France": "fr",
    "Senegal": "sn",
    "Iraq": "iq",
    "Norway": "no",
    "Argentina": "ar",
    "Algeria": "dz",
    "Austria": "at",
    "Jordan": "jo",
    "Portugal": "pt",
    "DR Congo": "cd",
    "Uzbekistan": "uz",
    "Colombia": "co",
    "England": "gb-eng",
    "Croatia": "hr",
    "Ghana": "gh",
    "Panama": "pa",
}
KICKOFF_ET = {
    ("2026-06-11", "Mexico", "South Africa"): "15:00",
    ("2026-06-11", "South Korea", "Czechia"): "22:00",
    ("2026-06-12", "Canada", "Bosnia and Herzegovina"): "15:00",
    ("2026-06-12", "United States", "Paraguay"): "21:00",
    ("2026-06-13", "Qatar", "Switzerland"): "15:00",
    ("2026-06-13", "Brazil", "Morocco"): "18:00",
    ("2026-06-13", "Haiti", "Scotland"): "21:00",
    ("2026-06-14", "Australia", "Turkiye"): "00:00",
    ("2026-06-14", "Australia", "Türkiye"): "00:00",
    ("2026-06-14", "Australia", "T羹rkiye"): "00:00",
    ("2026-06-14", "Germany", "Curacao"): "13:00",
    ("2026-06-14", "Netherlands", "Japan"): "16:00",
    ("2026-06-14", "Ivory Coast", "Ecuador"): "19:00",
    ("2026-06-14", "Sweden", "Tunisia"): "22:00",
    ("2026-06-15", "Spain", "Cabo Verde"): "12:00",
    ("2026-06-15", "Belgium", "Egypt"): "15:00",
    ("2026-06-15", "Saudi Arabia", "Uruguay"): "18:00",
    ("2026-06-15", "Iran", "New Zealand"): "21:00",
    ("2026-06-16", "France", "Senegal"): "15:00",
    ("2026-06-16", "Iraq", "Norway"): "18:00",
    ("2026-06-16", "Argentina", "Algeria"): "21:00",
    ("2026-06-17", "Austria", "Jordan"): "00:00",
    ("2026-06-17", "Portugal", "DR Congo"): "13:00",
    ("2026-06-17", "England", "Croatia"): "16:00",
    ("2026-06-17", "Ghana", "Panama"): "19:00",
    ("2026-06-17", "Uzbekistan", "Colombia"): "22:00",
    ("2026-06-18", "Czechia", "South Africa"): "12:00",
    ("2026-06-18", "Switzerland", "Bosnia and Herzegovina"): "15:00",
    ("2026-06-18", "Canada", "Qatar"): "18:00",
    ("2026-06-18", "Mexico", "South Korea"): "21:00",
    ("2026-06-19", "United States", "Australia"): "15:00",
    ("2026-06-19", "Scotland", "Morocco"): "18:00",
    ("2026-06-19", "Brazil", "Haiti"): "20:30",
    ("2026-06-19", "Turkiye", "Paraguay"): "23:00",
    ("2026-06-19", "Türkiye", "Paraguay"): "23:00",
    ("2026-06-19", "T羹rkiye", "Paraguay"): "23:00",
    ("2026-06-20", "Netherlands", "Sweden"): "13:00",
    ("2026-06-20", "Germany", "Ivory Coast"): "16:00",
    ("2026-06-20", "Ecuador", "Curacao"): "20:00",
    ("2026-06-21", "Tunisia", "Japan"): "00:00",
    ("2026-06-21", "Spain", "Saudi Arabia"): "12:00",
    ("2026-06-21", "Belgium", "Iran"): "15:00",
    ("2026-06-21", "Uruguay", "Cabo Verde"): "18:00",
    ("2026-06-21", "New Zealand", "Egypt"): "21:00",
    ("2026-06-22", "Argentina", "Austria"): "13:00",
    ("2026-06-22", "France", "Iraq"): "17:00",
    ("2026-06-22", "Norway", "Senegal"): "20:00",
    ("2026-06-22", "Jordan", "Algeria"): "23:00",
    ("2026-06-23", "Portugal", "Uzbekistan"): "13:00",
    ("2026-06-23", "England", "Ghana"): "16:00",
    ("2026-06-23", "Panama", "Croatia"): "19:00",
    ("2026-06-23", "Colombia", "DR Congo"): "22:00",
    ("2026-06-24", "Switzerland", "Canada"): "15:00",
    ("2026-06-24", "Bosnia and Herzegovina", "Qatar"): "15:00",
    ("2026-06-24", "Morocco", "Haiti"): "18:00",
    ("2026-06-24", "Scotland", "Brazil"): "18:00",
    ("2026-06-24", "South Africa", "South Korea"): "21:00",
    ("2026-06-24", "Czechia", "Mexico"): "21:00",
    ("2026-06-25", "Curacao", "Ivory Coast"): "16:00",
    ("2026-06-25", "Ecuador", "Germany"): "16:00",
    ("2026-06-25", "Tunisia", "Netherlands"): "19:00",
    ("2026-06-25", "Japan", "Sweden"): "19:00",
    ("2026-06-25", "Turkiye", "United States"): "22:00",
    ("2026-06-25", "Türkiye", "United States"): "22:00",
    ("2026-06-25", "T羹rkiye", "United States"): "22:00",
    ("2026-06-25", "Paraguay", "Australia"): "22:00",
    ("2026-06-26", "Norway", "France"): "15:00",
    ("2026-06-26", "Senegal", "Iraq"): "15:00",
    ("2026-06-26", "Cabo Verde", "Saudi Arabia"): "20:00",
    ("2026-06-26", "Uruguay", "Spain"): "20:00",
    ("2026-06-26", "New Zealand", "Belgium"): "23:00",
    ("2026-06-26", "Egypt", "Iran"): "23:00",
    ("2026-06-27", "Panama", "England"): "17:00",
    ("2026-06-27", "Croatia", "Ghana"): "17:00",
    ("2026-06-27", "Colombia", "Portugal"): "19:30",
    ("2026-06-27", "DR Congo", "Uzbekistan"): "19:30",
    ("2026-06-27", "Algeria", "Austria"): "22:00",
    ("2026-06-27", "Jordan", "Argentina"): "22:00",
}

PAST_CHAMPIONS = [
    (1930, "烏拉圭", "Estadio Centenario", "蒙特維多"),
    (1934, "義大利", "Stadio Nazionale PNF", "羅馬"),
    (1938, "義大利", "Stade Olympique de Colombes", "巴黎"),
    (1950, "烏拉圭", "Maracanã Stadium", "里約熱內盧"),
    (1954, "西德", "Wankdorf Stadium", "伯恩"),
    (1958, "巴西", "Råsunda Stadium", "索爾納"),
    (1962, "巴西", "Estadio Nacional", "聖地牙哥"),
    (1966, "英格蘭", "Wembley Stadium", "倫敦"),
    (1970, "巴西", "Estadio Azteca", "墨西哥城"),
    (1974, "西德", "Olympiastadion", "慕尼黑"),
    (1978, "阿根廷", "Estadio Monumental", "布宜諾斯艾利斯"),
    (1982, "義大利", "Santiago Bernabéu", "馬德里"),
    (1986, "阿根廷", "Estadio Azteca", "墨西哥城"),
    (1990, "西德", "Stadio Olimpico", "羅馬"),
    (1994, "巴西", "Rose Bowl", "帕薩迪納"),
    (1998, "法國", "Stade de France", "聖但尼"),
    (2002, "巴西", "International Stadium Yokohama", "橫濱"),
    (2006, "義大利", "Olympiastadion", "柏林"),
    (2010, "西班牙", "Soccer City", "約翰尼斯堡"),
    (2014, "德國", "Maracanã Stadium", "里約熱內盧"),
    (2018, "法國", "Luzhniki Stadium", "莫斯科"),
    (2022, "阿根廷", "Lusail Stadium", "路薩爾"),
]


def signed(value):
    return f"+{value}" if value > 0 else str(value)


def team_name(name):
    return TEAM_ZH.get(name, name)


def flag_img(name):
    code = TEAM_FLAG_CODE.get(name)
    if not code:
        return '<span class="flag fallback" aria-hidden="true"></span>'
    return f'<img class="flag" src="assets/flags/{code}.svg" alt="" decoding="async">'


def team_label(name):
    return f'{flag_img(name)}<span>{team_name(name)}</span>'

def kickoff_iso(match):
    time_et = KICKOFF_ET.get((match["date"], match["home"], match["away"]))
    if not time_et:
        return None
    hour, minute = map(int, time_et.split(":"))
    # June dates use Eastern Daylight Time, UTC-4.
    dt_et = datetime.fromisoformat(match["date"]).replace(hour=hour, minute=minute)
    dt_utc = (dt_et + timedelta(hours=4)).replace(tzinfo=timezone.utc)
    return dt_utc.isoformat().replace("+00:00", "Z")


def kickoff_display(match):
    iso = kickoff_iso(match)
    if not iso:
        return f'{match["date"][5:]}｜時間待確認'
    dt_utc = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    tw = dt_utc.astimezone(timezone.utc).timestamp() + 8 * 3600
    dt_tw = datetime.fromtimestamp(tw, tz=timezone.utc)
    return dt_tw.strftime("%m-%d %H:%M 台灣時間")


def fmt_score(match):
    if match.get("status") == "finished":
        return f'{match["home_score"]} - {match["away_score"]}'
    return "vs"


def render_group(group):
    rows = []
    for index, team in enumerate(group["teams"], start=1):
        advance = "advance" if index <= 2 else ("third" if index == 3 else "")
        rows.append(
            f"""
            <tr class="{advance}">
              <td><span class="rank">{index}</span></td>
              <td class="team-name"><span class="team-label">{team_label(team["team"])}</span></td>
              <td>{team["w"]}</td>
              <td>{team["d"]}</td>
              <td>{team["l"]}</td>
              <td>{team["gf"]}</td>
              <td>{team["ga"]}</td>
              <td>{signed(team["gd"])}</td>
              <td class="points">{team["pts"]}</td>
            </tr>
            """
        )

    matches = []
    for match in group["matches"]:
        status = "final" if match.get("status") == "finished" else "next"
        matches.append(
            f"""
            <li class="{status}">
              <span class="date">{kickoff_display(match)}</span>
              <span class="fixture"><span class="team-label">{team_label(match["home"])}</span></span>
              <strong>{fmt_score(match)}</strong>
              <span class="fixture right"><span class="team-label">{team_label(match["away"])}</span></span>
            </li>
            """
        )

    return f"""
    <section class="group-card">
      <div class="group-head">
        <p>小組</p>
        <h2>{group["name"]}</h2>
      </div>
      <table>
        <thead>
          <tr>
            <th>排名</th><th>隊伍</th><th>勝</th><th>和</th><th>敗</th><th>進球</th><th>失球</th><th>淨勝</th><th>積分</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
      <ol class="match-list">
        {''.join(matches)}
      </ol>
    </section>
    """


def upcoming_matches(data, limit=3):
    upcoming = []
    now = datetime.now(timezone.utc)
    for group in data["groups"]:
        for order, match in enumerate(group["matches"]):
            if match.get("status") == "finished":
                continue
            iso = kickoff_iso(match)
            if iso and datetime.fromisoformat(iso.replace("Z", "+00:00")) <= now:
                continue
            sort_key = iso or f'{match["date"]}T23:59:59Z'
            upcoming.append((sort_key, group["name"], order, match))
    return [
        (group_name, match)
        for _, group_name, _, match in sorted(upcoming, key=lambda item: (item[0], item[1], item[2]))[:limit]
    ]


def next_match(data):
    upcoming = upcoming_matches(data, 1)
    if not upcoming:
        return None
    return upcoming[0]


def current_match(data):
    now = datetime.now(timezone.utc)
    live_window = timedelta(minutes=150)
    candidates = []
    for group in data["groups"]:
        for order, match in enumerate(group["matches"]):
            if match.get("status") == "finished":
                continue
            iso = kickoff_iso(match)
            if not iso:
                continue
            start = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            if start <= now < start + live_window:
                candidates.append((start, group["name"], order, match))
    if not candidates:
        return None
    _, group_name, _, match = sorted(candidates, key=lambda item: (item[0], item[1], item[2]))[0]
    return group_name, match


def render_upcoming_panel(matches):
    if not matches:
        return '<div class="upcoming-panel" role="tooltip"><p>目前沒有接續賽事</p></div>'
    rows = []
    for index, (group_name, match) in enumerate(matches, start=1):
        rows.append(
            "\n".join(
                [
                    "            <li>",
                    f'              <span class="queue-index">{index}</span>',
                    f'              <span class="queue-meta">{group_name} 組｜{kickoff_display(match)}</span>',
                    f'              <strong><span class="team-label">{team_label(match["home"])}</span> vs <span class="team-label">{team_label(match["away"])}</span></strong>',
                    "            </li>",
                ]
            )
        )
    return "\n".join(
        [
            '        <div class="upcoming-panel" role="tooltip">',
            "          <small>接下來三場比賽</small>",
            "          <ol>",
            "\n".join(rows),
            "          </ol>",
            "        </div>",
        ]
    )


def render_champions():
    rows = []
    for year, champion, venue, city in sorted(PAST_CHAMPIONS, reverse=True):
        rows.append(
            f"""
            <tr>
              <td>{year}</td>
              <td>{champion}</td>
              <td>{venue}</td>
              <td>{city}</td>
            </tr>
            """
        )
    return "".join(rows)


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    total_matches = sum(len(group["matches"]) for group in data["groups"])
    finished = sum(
        1
        for group in data["groups"]
        for match in group["matches"]
        if match.get("status") == "finished"
    )
    groups_html = "\n".join(render_group(group) for group in data["groups"])
    payload = json.dumps(data, ensure_ascii=False)
    source = data.get("source", {})
    if source.get("fifa_matches_url"):
        source_links = f'資料來源：<a href="{source["fifa_matches_url"]}">FIFA 官方賽程與比分 API</a> · 歷屆冠軍與決賽場地參考 FIFA World Cup finals 資料整理'
    else:
        source_links = f'資料來源：<a href="{source.get("standings_url", "#")}">排名</a> · <a href="{source.get("schedule_url", "#")}">賽程</a> · 歷屆冠軍與決賽場地參考 FIFA World Cup finals 資料整理'
    leaders = " / ".join(team_name(team["team"]) for team in data["groups"][0]["teams"][:2])
    live = current_match(data)
    if live:
        live_group, live_game = live
        if live_game.get("home_score") is not None and live_game.get("away_score") is not None:
            live_score = f'{live_game["home_score"]} - {live_game["away_score"]}'
        else:
            live_score = "即時比分待更新"
        live_text = (
            f'{live_group} 組｜{kickoff_display(live_game)}｜'
            f'<span class="team-label">{team_label(live_game["home"])}</span> vs '
            f'<span class="team-label">{team_label(live_game["away"])}</span>｜{live_score}'
        )
    else:
        live_text = "目前無進行中賽事"
    upcoming = upcoming_matches(data, 3)
    if upcoming:
        next_group, next_game = upcoming[0]
        next_iso = kickoff_iso(next_game) or ""
        next_text = (
            f'{next_group} 組｜{kickoff_display(next_game)}｜'
            f'<span class="team-label">{team_label(next_game["home"])}</span> vs '
            f'<span class="team-label">{team_label(next_game["away"])}</span>'
        )
    else:
        next_iso = ""
        next_text = "小組賽已全部完賽"
    upcoming_panel = render_upcoming_panel(upcoming)

    HTML_PATH.write_text(
        f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FIFA World Cup 26 對戰與排名儀表板</title>
  <style>
    :root {{
      --ink: #080808;
      --paper: #fbfaf7;
      --gold: #c9a24b;
      --gold-soft: #f6df9a;
      --red: #e1262f;
      --green: #00a85a;
      --blue: #1769e0;
      --line: rgba(255,255,255,.16);
      --muted: rgba(255,255,255,.68);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--paper);
      background:
        linear-gradient(125deg, rgba(225,38,47,.23), transparent 26%),
        linear-gradient(235deg, rgba(0,168,90,.22), transparent 30%),
        radial-gradient(circle at 75% 18%, rgba(23,105,224,.32), transparent 30%),
        #080808;
    }}
    .brand-ribbon {{ height: 8px; background: linear-gradient(90deg, var(--red), var(--gold-soft), var(--green), var(--blue)); }}
    header {{ padding: 28px clamp(18px, 4vw, 54px) 18px; border-bottom: 1px solid var(--line); }}
    .hero {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 24px; align-items: end; max-width: 1480px; margin: 0 auto; }}
    .mark {{ font-size: clamp(86px, 13vw, 190px); line-height: .78; font-weight: 950; letter-spacing: 0; color: transparent; -webkit-text-stroke: 2px rgba(255,255,255,.9); text-shadow: 0 0 34px rgba(201,162,75,.28); }}
    h1 {{ margin: 0 0 10px; font-size: clamp(28px, 5vw, 74px); line-height: .96; letter-spacing: 0; max-width: 900px; }}
    .subline {{ display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font-size: 14px; }}
    .pill {{ border: 1px solid var(--line); border-radius: 999px; padding: 7px 10px; background: rgba(255,255,255,.06); }}
    main {{ max-width: 1480px; margin: 0 auto; padding: 22px clamp(14px, 3vw, 42px) 44px; }}
    .summary {{ position: relative; z-index: 30; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-bottom: 18px; }}
    .metric {{ min-height: 96px; padding: 16px; border: 1px solid var(--line); background: rgba(255,255,255,.07); backdrop-filter: blur(16px); }}
    .metric small {{ display: block; color: var(--muted); }}
    .metric strong {{ display: block; margin-top: 8px; font-size: clamp(24px, 4vw, 42px); }}
    .metric.wide {{ grid-column: 1 / -1; }}
    .metric.wide strong {{ font-size: clamp(18px, 2.4vw, 30px); line-height: 1.2; }}
    .next-metric {{ position: relative; z-index: 40; }}
    .upcoming-panel {{ position: absolute; z-index: 60; left: 16px; right: 16px; top: calc(100% + 8px); opacity: 0; transform: translateY(-4px); pointer-events: none; transition: opacity .16s ease, transform .16s ease; padding: 14px; border: 1px solid rgba(246,223,154,.45); background: rgba(8,12,18,.98); box-shadow: 0 18px 36px rgba(0,0,0,.42); backdrop-filter: blur(18px); }}
    .next-metric:hover .upcoming-panel, .next-metric:focus-within .upcoming-panel {{ opacity: 1; transform: translateY(0); pointer-events: auto; }}
    .upcoming-panel small {{ color: var(--gold-soft); font-weight: 850; }}
    .upcoming-panel ol {{ list-style: none; display: grid; gap: 8px; margin: 10px 0 0; padding: 0; }}
    .upcoming-panel li {{ display: grid; grid-template-columns: 28px minmax(120px, .35fr) minmax(0, 1fr); align-items: center; gap: 10px; padding: 9px 10px; border: 1px solid rgba(255,255,255,.12); background: rgba(255,255,255,.055); }}
    .queue-index {{ display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: var(--gold-soft); color: var(--ink); font-weight: 900; }}
    .queue-meta {{ color: var(--muted); font-size: 13px; font-weight: 750; }}
    .upcoming-panel li strong {{ margin: 0; font-size: 15px; line-height: 1.25; }}
    .countdown {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
    .countdown span {{ min-width: 72px; padding: 10px 12px; border: 1px solid rgba(246,223,154,.34); background: rgba(0,0,0,.24); text-align: center; font-weight: 900; font-variant-numeric: tabular-nums; }}
    .countdown small {{ color: var(--muted); font-size: 11px; font-weight: 650; }}
    .grid {{ position: relative; z-index: 1; display: grid; grid-template-columns: repeat(3, minmax(340px, 1fr)); gap: 14px; }}
    .group-card, .history {{ border: 1px solid var(--line); background: linear-gradient(180deg, rgba(255,255,255,.12), rgba(255,255,255,.055)); backdrop-filter: blur(18px); border-radius: 8px; overflow: hidden; box-shadow: 0 18px 40px rgba(0,0,0,.22); }}
    .group-head, .history-head {{ display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; background: linear-gradient(90deg, rgba(201,162,75,.32), rgba(255,255,255,.04)); border-bottom: 1px solid var(--line); }}
    .group-head p, .history-head p {{ margin: 0; color: var(--muted); text-transform: uppercase; font-size: 12px; }}
    .group-head h2, .history-head h2 {{ margin: 0; font-size: 34px; line-height: 1; color: var(--gold-soft); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 9px 7px; text-align: center; border-bottom: 1px solid rgba(255,255,255,.08); white-space: nowrap; }}
    th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; background: rgba(0,0,0,.18); }}
    .team-name, .history td:nth-child(2), .history td:nth-child(3), .history td:nth-child(4) {{ text-align: left; font-weight: 750; }}
    .team-label {{ display: inline-flex; align-items: center; gap: 7px; min-width: 0; max-width: 100%; }}
    .flag {{ flex: 0 0 auto; width: 22px; height: 16px; display: inline-block; border-radius: 2px; object-fit: cover; box-shadow: 0 0 0 1px rgba(255,255,255,.22); background: rgba(255,255,255,.12); }}
    .flag.fallback {{ box-shadow: inset 0 0 0 1px rgba(255,255,255,.22); }}
    .rank {{ display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,.09); font-weight: 800; }}
    tr.advance .rank {{ background: var(--gold-soft); color: var(--ink); }}
    tr.third .rank {{ border: 1px solid var(--gold); color: var(--gold-soft); }}
    .points {{ font-size: 16px; font-weight: 900; color: var(--gold-soft); }}
    .match-list {{ list-style: none; margin: 0; padding: 10px 12px 14px; display: grid; gap: 7px; }}
    .match-list li {{ display: grid; grid-template-columns: 96px minmax(0, 1fr) 48px minmax(0, 1fr); align-items: center; gap: 8px; min-height: 38px; padding: 7px 8px; border: 1px solid rgba(255,255,255,.1); background: rgba(0,0,0,.18); border-radius: 6px; font-size: 12px; }}
    .match-list li.final {{ border-color: rgba(246,223,154,.42); }}
    .date {{ color: var(--muted); font-variant-numeric: tabular-nums; white-space: normal; line-height: 1.25; }}
    .fixture {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .fixture .team-label {{ max-width: 100%; }}
    .right {{ text-align: right; }}
    .match-list strong {{ color: var(--gold-soft); text-align: center; font-variant-numeric: tabular-nums; }}
    .history {{ margin-top: 18px; }}
    .history-wrap {{ overflow-x: auto; }}
    footer {{ max-width: 1480px; margin: 0 auto; padding: 0 clamp(14px, 3vw, 42px) 28px; color: var(--muted); font-size: 12px; }}
    a {{ color: var(--gold-soft); }}
    @media (max-width: 1120px) {{ .grid {{ grid-template-columns: repeat(2, minmax(320px, 1fr)); }} }}
    @media (max-width: 740px) {{
      .hero {{ grid-template-columns: 1fr; }}
      .mark {{ font-size: 96px; }}
      .summary {{ grid-template-columns: 1fr; }}
      .grid {{ grid-template-columns: 1fr; }}
      th, td {{ padding: 8px 5px; font-size: 12px; }}
      .match-list li {{ grid-template-columns: 86px 1fr 42px 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="brand-ribbon"></div>
  <header>
    <div class="hero">
      <div>
        <h1>FIFA World Cup 26 對戰與排名</h1>
        <div class="subline">
          <span class="pill">資料更新：{data["updated_at"]}</span>
          <span class="pill">賽程時間：台灣時間</span>
          <span class="pill">前二名直接晉級，8 個最佳第三名晉級 32 強</span>
        </div>
      </div>
      <div class="mark">26</div>
    </div>
  </header>
  <main>
    <section class="summary">
      <div class="metric"><small>小組</small><strong>{len(data["groups"])}</strong></div>
      <div class="metric"><small>已完賽</small><strong>{finished}/{total_matches}</strong></div>
      <div class="metric"><small>A 組目前領先</small><strong>{leaders}</strong></div>
      <div class="metric wide">
        <small>目前比賽</small>
        <strong>{live_text}</strong>
      </div>
      <div class="metric wide next-metric" tabindex="0">
        <small>下一場比賽</small>
        <strong>{next_text}</strong>
        <div class="countdown" data-kickoff="{next_iso}">
          <span><b data-days>--</b><br><small>天</small></span>
          <span><b data-hours>--</b><br><small>小時</small></span>
          <span><b data-minutes>--</b><br><small>分鐘</small></span>
          <span><b data-seconds>--</b><br><small>秒</small></span>
        </div>
        {upcoming_panel}
      </div>
    </section>
    <section class="grid">
      {groups_html}
    </section>
    <section class="history">
      <div class="history-head">
        <p>歷史</p>
        <h2>歷屆冠軍與決賽場地</h2>
      </div>
      <div class="history-wrap">
        <table>
          <thead><tr><th>年份</th><th>冠軍</th><th>決賽場地</th><th>城市</th></tr></thead>
          <tbody>{render_champions()}</tbody>
        </table>
      </div>
    </section>
  </main>
  <footer>
    {source_links}
    <script type="application/json" id="dashboard-data">{payload}</script>
  </footer>
  <script>
    const countdown = document.querySelector("[data-kickoff]");
    function pad(value) {{
      return String(value).padStart(2, "0");
    }}
    function tickCountdown() {{
      if (!countdown || !countdown.dataset.kickoff) return;
      const target = new Date(countdown.dataset.kickoff).getTime();
      const remaining = Math.max(0, target - Date.now());
      const totalSeconds = Math.floor(remaining / 1000);
      const days = Math.floor(totalSeconds / 86400);
      const hours = Math.floor((totalSeconds % 86400) / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      countdown.querySelector("[data-days]").textContent = days;
      countdown.querySelector("[data-hours]").textContent = pad(hours);
      countdown.querySelector("[data-minutes]").textContent = pad(minutes);
      countdown.querySelector("[data-seconds]").textContent = pad(seconds);
    }}
    tickCountdown();
    setInterval(tickCountdown, 1000);
  </script>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"已產生 {HTML_PATH}")


if __name__ == "__main__":
    main()
