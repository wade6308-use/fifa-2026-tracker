import json
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
    "Türkiye": "土耳其",
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


def signed(value):
    return f"+{value}" if value > 0 else str(value)


def team_name(name):
    return TEAM_ZH.get(name, name)


def fmt_score(match):
    if match.get("status") == "finished":
        return f'{match["home_score"]} - {match["away_score"]}'
    return "對"


def render_group(group):
    rows = []
    for index, team in enumerate(group["teams"], start=1):
        advance = "advance" if index <= 2 else ("third" if index == 3 else "")
        rows.append(
            f"""
            <tr class="{advance}">
              <td><span class="rank">{index}</span></td>
              <td class="team-name">{team_name(team["team"])}</td>
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
              <span class="date">{match["date"][5:]}</span>
              <span class="fixture">{team_name(match["home"])}</span>
              <strong>{fmt_score(match)}</strong>
              <span class="fixture right">{team_name(match["away"])}</span>
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
    leaders = " / ".join(team_name(team["team"]) for team in data["groups"][0]["teams"][:2])

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
    .brand-ribbon {{
      height: 8px;
      background: linear-gradient(90deg, var(--red), var(--gold-soft), var(--green), var(--blue));
    }}
    header {{
      position: relative;
      padding: 28px clamp(18px, 4vw, 54px) 18px;
      border-bottom: 1px solid var(--line);
      overflow: hidden;
    }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: end;
      max-width: 1480px;
      margin: 0 auto;
    }}
    .mark {{
      font-size: clamp(86px, 13vw, 190px);
      line-height: .78;
      font-weight: 950;
      letter-spacing: 0;
      color: transparent;
      -webkit-text-stroke: 2px rgba(255,255,255,.9);
      text-shadow: 0 0 34px rgba(201,162,75,.28);
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: clamp(28px, 5vw, 74px);
      line-height: .96;
      letter-spacing: 0;
      max-width: 900px;
    }}
    .subline {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      color: var(--muted);
      font-size: 14px;
    }}
    .pill {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 7px 10px;
      background: rgba(255,255,255,.06);
    }}
    main {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 22px clamp(14px, 3vw, 42px) 44px;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }}
    .metric {{
      min-height: 96px;
      padding: 16px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.07);
      backdrop-filter: blur(16px);
    }}
    .metric small {{ display: block; color: var(--muted); }}
    .metric strong {{ display: block; margin-top: 8px; font-size: clamp(24px, 4vw, 42px); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(340px, 1fr));
      gap: 14px;
    }}
    .group-card {{
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255,255,255,.12), rgba(255,255,255,.055));
      backdrop-filter: blur(18px);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 18px 40px rgba(0,0,0,.22);
    }}
    .group-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 16px;
      background: linear-gradient(90deg, rgba(201,162,75,.32), rgba(255,255,255,.04));
      border-bottom: 1px solid var(--line);
    }}
    .group-head p {{ margin: 0; color: var(--muted); text-transform: uppercase; font-size: 12px; }}
    .group-head h2 {{ margin: 0; font-size: 34px; line-height: 1; color: var(--gold-soft); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      padding: 9px 7px;
      text-align: center;
      border-bottom: 1px solid rgba(255,255,255,.08);
      white-space: nowrap;
    }}
    th {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      background: rgba(0,0,0,.18);
    }}
    .team-name {{ text-align: left; font-weight: 750; }}
    .rank {{
      display: inline-grid;
      place-items: center;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: rgba(255,255,255,.09);
      font-weight: 800;
    }}
    tr.advance .rank {{ background: var(--gold-soft); color: var(--ink); }}
    tr.third .rank {{ border: 1px solid var(--gold); color: var(--gold-soft); }}
    .points {{ font-size: 16px; font-weight: 900; color: var(--gold-soft); }}
    .match-list {{
      list-style: none;
      margin: 0;
      padding: 10px 12px 14px;
      display: grid;
      gap: 7px;
    }}
    .match-list li {{
      display: grid;
      grid-template-columns: 44px minmax(0, 1fr) 48px minmax(0, 1fr);
      align-items: center;
      gap: 8px;
      min-height: 34px;
      padding: 7px 8px;
      border: 1px solid rgba(255,255,255,.1);
      background: rgba(0,0,0,.18);
      border-radius: 6px;
      font-size: 12px;
    }}
    .match-list li.final {{ border-color: rgba(246,223,154,.42); }}
    .date {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
    .fixture {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .right {{ text-align: right; }}
    .match-list strong {{ color: var(--gold-soft); text-align: center; font-variant-numeric: tabular-nums; }}
    footer {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 0 clamp(14px, 3vw, 42px) 28px;
      color: var(--muted);
      font-size: 12px;
    }}
    a {{ color: var(--gold-soft); }}
    @media (max-width: 1120px) {{
      .grid {{ grid-template-columns: repeat(2, minmax(320px, 1fr)); }}
    }}
    @media (max-width: 740px) {{
      .hero {{ grid-template-columns: 1fr; }}
      .mark {{ font-size: 96px; }}
      .summary {{ grid-template-columns: 1fr; }}
      .grid {{ grid-template-columns: 1fr; }}
      th, td {{ padding: 8px 5px; font-size: 12px; }}
      .match-list li {{ grid-template-columns: 42px 1fr 42px 1fr; }}
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
          <span class="pill">前二名直接晉級</span>
          <span class="pill">8 個最佳第三名晉級 32 強</span>
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
    </section>
    <section class="grid">
      {groups_html}
    </section>
  </main>
  <footer>
    資料來源：<a href="{data["source"]["standings_url"]}">排名</a> · <a href="{data["source"]["schedule_url"]}">賽程</a>
    <script type="application/json" id="dashboard-data">{payload}</script>
  </footer>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"已產生 {HTML_PATH}")


if __name__ == "__main__":
    main()
