# FIFA World Cup 26 對戰與排名儀表板

這是一個靜態 HTML 儀表板，用來查看 2026 FIFA World Cup 小組賽對戰、比分與排名。

## 檔案

- `index.html`：GitHub Pages 會顯示的主頁
- `data/worldcup_2026.json`：賽事資料
- `scripts/update_worldcup_2026.py`：從公開比分頁更新資料並重新產生 HTML
- `watch_worldcup_2026.ps1`：本機持續輪詢更新腳本

## 本機更新

```powershell
.\watch_worldcup_2026.ps1
```

資料來源目前為公開賽程與排名頁面；更新速度取決於來源頁面更新時間。
