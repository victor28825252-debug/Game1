# 發布紀錄

- 產品範圍：兩關，每關一個理財台互動單元、兩個相關判斷、鑰匙與門鎖、即時計分、重玩比較。
- DT／SDLC：`project-brief.md`、`decision-log.md`、`project-state.yaml`、`traceability.md` 記錄問題、代選決策、需求與驗證。使用者授權完成並發布，最終驗收仍待使用者遊玩。
- game-design：`game-design/tournament.md`、`scorecard.json`、`ranking.json`、`reward-results.json`、三張視覺方向稿及 `visual-decision.md`。選擇紀錄為 AI 依評分代選，並非真人玩家資料。
- blender-skills：套用 `turntable` 技能的 3D 模型匯入、攝影機軌道、透明背景與燈光流程，腳本為 `art/render_key_turntable.py`。技能原案使用 Blender MCP；此環境無 MCP addon，因此以 `C:\blender\blender.exe` 批次執行相同步驟。場景和模型由 `art/build_assets.py` 建立。
- 自動化：`godot/tests/test_flow.gd` 通過。
- 人員測試：尚未有小學生玩家測試；不可將分數變化解讀為已驗證學習成效。
