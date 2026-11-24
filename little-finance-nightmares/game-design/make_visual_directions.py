"""Generate three 16:9 mockups with identical gameplay content and state."""
from pathlib import Path

out = Path(__file__).resolve().parent
directions = [
    ("01-shadow-storybook", "暗色童話", "#0b1c2c", "#183c48", "#f6cf81", "#a0e4dd", "#fff4da"),
    ("02-paper-cut", "紙雕探險", "#d8f1e9", "#93cec1", "#ef855e", "#355c6b", "#183947"),
    ("03-night-blueprint", "夜色藍圖", "#171b39", "#323970", "#f3ba68", "#a8a7ed", "#f4edff"),
]
for filename, label, bg, panel, accent, second, text in directions:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<rect width="1280" height="720" fill="{bg}"/>
<rect x="25" y="22" width="1230" height="74" rx="16" fill="{panel}"/>
<text x="55" y="69" fill="{text}" font-size="28" font-family="Noto Sans TC, sans-serif">第 1 關｜零用錢的房間</text>
<text x="1010" y="69" fill="{accent}" font-size="26" font-family="Noto Sans TC, sans-serif">得分 80 / 100</text>
<rect x="24" y="120" width="1232" height="545" rx="18" fill="{panel}" opacity=".48"/>
<path d="M 130 560 L 130 240 L 392 240 L 392 560 Z" fill="{bg}" stroke="{second}" stroke-width="9"/>
<path d="M 928 568 L 928 205 Q 1080 110 1186 205 L 1186 568 Z" fill="{bg}" stroke="{accent}" stroke-width="12"/>
<circle cx="1107" cy="391" r="15" fill="{accent}"/>
<circle cx="650" cy="444" r="43" fill="{accent}"/>
<path d="M 602 575 L 607 485 L 695 485 L 703 575 Z" fill="{accent}"/>
<rect x="265" y="162" width="730" height="344" rx="28" fill="{bg}" stroke="{accent}" stroke-width="4"/>
<text x="303" y="210" fill="{second}" font-size="22" font-family="Noto Sans TC, sans-serif">{label}｜互動單元</text>
<text x="303" y="266" fill="{text}" font-size="31" font-family="Noto Sans TC, sans-serif">預算 100 元：午餐 45 元，想存 30 元</text>
<text x="303" y="313" fill="{text}" font-size="23" font-family="Noto Sans TC, sans-serif">怎麼安排剩下的錢，才能取得鑰匙？</text>
<rect x="305" y="348" width="645" height="62" rx="14" fill="{accent}"/>
<text x="504" y="389" fill="{bg}" font-size="25" font-family="Noto Sans TC, sans-serif">重新安排預算</text>
<text x="304" y="454" fill="{second}" font-size="22" font-family="Noto Sans TC, sans-serif">超出預算 5 元，門仍鎖著；請修正選擇。</text>
<text x="54" y="701" fill="{text}" font-size="16" font-family="Noto Sans TC, sans-serif">原創教學遊戲視覺方案｜相同玩法、內容與遊戲狀態</text>
</svg>'''
    (out / f"{filename}.svg").write_text(svg, encoding="utf-8")
