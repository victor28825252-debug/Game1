# 微光理財屋

給小學生的兩關生活理財解謎遊戲。場景由 Blender 5.3 製作並渲染，互動與計分由 Godot 4.7.2 製作，`docs/` 是可直接放上 GitHub Pages 的網頁版本。美術參考《Little Nightmares》的暗色童話探索氣氛，但角色、場景、模型、題目與名稱均為本專案原創，未使用其素材。

## 遊戲內容

| 關卡 | 學習目標 | 過關條件 |
| --- | --- | --- |
| 1 零用錢的房間 | 先支付需要的費用，再規劃儲蓄與想要的支出 | 完成同一理財台的兩個預算判斷，取得鑰匙，開門 |
| 2 選擇的房間 | 保留近期必需費用，認識投資風險與分散 | 完成同一理財台的兩個風險判斷，取得鑰匙，開門 |

每關滿分 100 分。答錯一次扣 20 分，查看提示扣 10 分，最低 40 分；答錯後可繼續作答。結尾顯示兩關分數與總分。第一次完成建立基準，再玩一次顯示各關與上次同關相比的分數變化。分數是遊戲表現，尚未經實際學生測試驗證為學習成效。遊戲不推薦任何金融商品，也不要求玩家輸入個資。通關鑰匙由 Blender 原創 3D 模型渲染為旋轉影格。

## 本機執行

Godot Web 匯出需要 HTTP 伺服器；例如在 `docs/` 目錄執行：

```powershell
& 'C:\blender\5.3\python\bin\python.exe' -m http.server 8765
```

然後瀏覽 `http://127.0.0.1:8765/`。建議使用桌機瀏覽器，手機請橫向觀看。

編輯原始專案：用 `C:\Godot\Godot_v4.7.2-stable_win64.exe` 開啟 `godot/project.godot`。`art/build_assets.py` 可用 `C:\blender\blender.exe -b --python art/build_assets.py` 重建 3D 場景圖與鑰匙 GLB；重建後將輸出檔複製到 `godot/assets/`。`art/render_key_turntable.py` 使用已安裝的 blender-skills `turntable` 攝影機旋轉流程，以 Blender 批次模式重建鑰匙影格。

## 部署至 GitHub Pages

本專案部署於既有 `Game1` 儲存庫的 `/little-finance-nightmares/` 路徑。此資料夾根目錄的 `index.html` 會轉向 `docs/`，無需建置；GitHub Pages 應設為從 `main` 的 `/ (root)` 發布。

網頁版匯出檔約數十 MB，首次載入會下載 Godot WebAssembly。`docs/index.wasm` 與 `docs/index.pck` 必須與 `docs/index.html` 一起上傳，不能只上傳 HTML。

若修改 Godot 程式，重新匯出：

```powershell
& 'C:\Godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path .\godot --export-release Web ..\docs\index.html
```

## 驗證

```powershell
& 'C:\Godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path .\godot --script res://tests/test_flow.gd
```

測試涵蓋門鎖、兩步驟解題、提示與答錯扣分、兩把鑰匙、第二關切換和同關重玩比較。設計過程與技能套用證據見 `game-design/`、`project-brief.md`、`decision-log.md`、`traceability.md` 和 `release-checklist.md`。

## 授權與來源

`godot/assets/NotoSansTC.ttf` 來自 [Google Fonts 的 Noto Sans TC](https://github.com/google/fonts/tree/main/ofl/notosanstc)，以 SIL Open Font License 授權；授權全文見 `OFL-NotoSansTC.txt`。Godot 引擎另依其 MIT 授權發布，Blender 只用於製作素材，未包含 Blender 程式。Steam 參考作品的名稱和商標屬其權利人。
