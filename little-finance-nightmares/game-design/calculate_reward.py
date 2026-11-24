"""Recompute the game-design educational diagnostic from a locked scorecard."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / "scorecard.json").read_text(encoding="utf-8"))
p = data["profile"]
w, penalty = p["weights"], p["penalties"]
assert abs(sum(w.values()) - 1.0) < 1e-9
result = {}
for candidate in data["candidates"]:
    e = candidate["education"]
    assert all(0 <= e[k] <= 100 for k in ("L", "E", "M", "A", "G", "C"))
    value = sum(w[k] * e[k] for k in ("L", "E", "M", "A"))
    value -= penalty["G"] * e["G"] + penalty["C"] * e["C"]
    result[candidate["id"]] = round(max(0, min(100, value)), 2)
(root / "reward-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(result)
