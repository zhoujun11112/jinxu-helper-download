#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-001 · 12 支机制文字卡片素材生成器

产出：
  assets/exp001-cards/<ID>_a.png   状态A：仅主文案
  assets/exp001-cards/<ID>_b.png   状态B：主文案＋副文案（可作静态图单独使用）
  assets/exp001-cards/<ID>.mp4     6 秒动效卡（0-2s主文案 / 2s交叉淡入副文案 / 缓慢推进 / 静音轨）

依赖：系统 chromium + ffmpeg（本容器路径已内置，可用环境变量覆盖）
用法：python3 tools/make_cards.py
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/japan-ai-short-drama/assets/exp001-cards"
TMP = Path(os.environ.get("CARD_TMP", "/tmp/claude-0/cards"))

CHROME = os.environ.get(
    "CHROME_BIN", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
FFMPEG = os.environ.get(
    "FFMPEG_BIN", "/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux")

W, H = 1080, 1920

# ---------------------------------------------------------------------------
# 12 支卡片。main/sub 中的 | 表示强制换行（日文排版需人工控制断行位置）。
# ---------------------------------------------------------------------------
CARDS = [
    # ---- 机制 A：心声改写 ----
    dict(id="A1", mech="A", angle="能力先行",
         main="私は、他人が言わなかった|本音を、一日一つだけ|書き換えられる。",
         sub="今日、上司の本音を書き換えた。"),
    dict(id="A2", mech="A", angle="代价先行",
         main="本音を一つ書き換えるたび、|私を愛した人の声を|一つ忘れていく。",
         sub="母の声が、もう思い出せない。"),
    dict(id="A3", mech="A", angle="情境先行",
         main="「彼女は来月で契約終了」|——課長の心の声が、|聞こえてしまった。",
         sub="だから私は、その一言を|書き換えることにした。"),
    dict(id="A4", mech="A", angle="疑问先行",
         main="本音を一つだけ|書き換えられるとしたら、|誰の、どの一言を変えますか。",
         sub="代償は、あなたの記憶です。"),
    # ---- 机制 B：明日来电 ----
    dict(id="B1", mech="B", angle="能力先行",
         main="毎晩3時、|24時間後の私から|電話がかかってくる。",
         sub="発信者番号は、私の内線だった。"),
    dict(id="B2", mech="B", angle="代价先行",
         main="未来からの電話を聞くたび、|私に近い誰かが、|私を24時間忘れる。",
         sub="昨日まで、妹は私を|「お姉ちゃん」と呼んでいた。"),
    dict(id="B3", mech="B", angle="情境先行",
         main="「18時10分、|妹を駅に行かせないで」|——電話の声は、私自身だった。",
         sub="あと4時間しかない。"),
    dict(id="B4", mech="B", angle="疑问先行",
         main="明日の自分から|警告の電話が来たら、|あなたは出ますか。",
         sub="出た瞬間、誰かが|あなたを忘れます。"),
    # ---- 机制 C：记忆典当 ----
    dict(id="C1", mech="C", angle="能力先行",
         main="この店では、自分の記憶を|質に入れて、誰かが|隠した真実を買える。",
         sub="深夜のコインランドリー、営業中。"),
    dict(id="C2", mech="C", angle="代价先行",
         main="夫が消えた夜の真実と|引き換えに、娘が初めて|「ママ」と呼んだ日を手放した。",
         sub="後悔はしていない。まだ。"),
    dict(id="C3", mech="C", angle="情境先行",
         main="娘が「ママ」と呼んだ。|私は、その子が|誰なのか分からなかった。",
         sub="昨夜、その記憶を質に入れたから。"),
    dict(id="C4", mech="C", angle="疑问先行",
         main="一番大切な記憶と|引き換えにしてでも、|知りたい真実はありますか。",
         sub="この店は、深夜だけ開いています。"),
]

# 三个机制各用一种底色，但字体/字号/版式/动效完全一致——
# 底色是机制的视觉标识，不是被测变量（12 支的唯一变量是文案）。
PALETTE = {
    "A": ("#0d1117", "#161d27"),   # 冷灰 · 职场
    "B": ("#0b0f1a", "#141b2e"),   # 深蓝 · 深夜来电
    "C": ("#12100d", "#1e1a15"),   # 暖褐 · 洗衣店
}

HTML = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{w}px; height:{h}px; overflow:hidden; }}
  body {{
    background: linear-gradient(160deg, {c1} 0%, {c2} 100%);
    font-family: "IPAPGothic", "IPAGothic", "Noto Sans JP", sans-serif;
    display:flex; flex-direction:column; justify-content:center;
    padding: 0 96px 260px 96px;   /* 底部留出 TikTok UI 安全区 */
  }}
  .rule {{
    width:96px; height:5px; background:#c8a45c;
    margin-bottom:64px; opacity:{rule_op};
  }}
  .main {{ white-space:nowrap;
    color:#f5f3ef; font-size:{fs_main}px; line-height:1.58;
    letter-spacing:0.01em;
    text-shadow:0 2px 24px rgba(0,0,0,.55);
  }}
  .sub {{ white-space:nowrap;
    color:#c8a45c; font-size:{fs_sub}px; line-height:1.72;
    margin-top:72px; letter-spacing:0.01em;
    opacity:{sub_op};
  }}
</style></head><body>
  <div class="rule"></div>
  <div class="main">{main}</div>
  <div class="sub">{sub}</div>
</body></html>"""


CONTENT_W = W - 96 * 2   # 左右留白后的可用宽度


def _width(line: str) -> float:
    """全角计 1，ASCII 计 0.5，估算行宽（单位：em）。"""
    return sum(0.5 if ord(c) < 0x2E80 else 1.0 for c in line)


def autofit(text: str, lo: int, hi: int) -> int:
    """按最长行反算字号，保证不触发自动换行。"""
    longest = max(_width(l) for l in text.split("|"))
    return max(lo, min(hi, int(CONTENT_W / longest * 0.97)))


def render(card: dict, state: str, path: Path) -> None:
    """state='a' 仅主文案；state='b' 主文案＋副文案。"""
    c1, c2 = PALETTE[card["mech"]]
    fs_main = autofit(card["main"], 44, 72)
    fs_sub = autofit(card["sub"], 30, 44)
    html = HTML.format(
        w=W, h=H, c1=c1, c2=c2, fs_main=fs_main, fs_sub=fs_sub,
        rule_op="1" if state == "a" else "1",
        sub_op="0" if state == "a" else "1",
        main=card["main"].replace("|", "<br>"),
        sub=card["sub"].replace("|", "<br>"),
    )
    hf = TMP / f"{card['id']}_{state}.html"
    hf.write_text(html, encoding="utf-8")
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--default-background-color=00000000",
        f"--screenshot={path}", f"--window-size={W},{H}",
        f"file://{hf}",
    ], check=True, capture_output=True)


def animate(card: dict, a: Path, b: Path, out: Path) -> None:
    """6 秒动效：主文案定格 → 1.9s 起交叉淡入副文案 → 全程极缓推进 → 静音轨。"""
    vf = (
        "[0:v]fps=30,scale=1080:1920,setsar=1[a];"
        "[1:v]fps=30,scale=1080:1920,setsar=1[b];"
        "[a][b]xfade=transition=fade:duration=0.5:offset=1.9[x];"
        "[x]zoompan=z='min(1+0.00030*on,1.055)':d=1"
        ":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        ":s=1080x1920:fps=30,"
        "fade=t=in:st=0:d=0.45,format=yuv420p[v]"
    )
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-t", "2.4", "-i", str(a),
        "-loop", "1", "-t", "4.1", "-i", str(b),
        "-f", "lavfi", "-t", "6",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-filter_complex", vf,
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "23",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
        "-t", "6", "-movflags", "+faststart", str(out),
    ], check=True, capture_output=True)


def main() -> int:
    for p in (OUT, TMP):
        p.mkdir(parents=True, exist_ok=True)
    for c in CARDS:
        a = OUT / f"{c['id']}_a.png"
        b = OUT / f"{c['id']}_b.png"
        mp4 = OUT / f"{c['id']}.mp4"
        render(c, "a", a)
        render(c, "b", b)
        animate(c, a, b, mp4)
        print(f"  {c['id']} ({c['mech']}·{c['angle']})  "
              f"png {b.stat().st_size//1024}KB  mp4 {mp4.stat().st_size//1024}KB")
    print(f"\n完成：{len(CARDS)} 支 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
