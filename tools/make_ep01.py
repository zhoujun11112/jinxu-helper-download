#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EP01《書き換えられた本音》· 文字ドラマ版 成片生成器

形态说明：
  不使用 AI 生成画面。全片由排版 + 音频设计构成——这与本剧机制天然契合：
  "说出口的话" 与 "没说出口的心声" 用两套字体样式区分，观众一眼就懂规则。
  日本 TikTok/Shorts 的スカッと系、文字ドラマ是成熟品类，此形态可直接上线测试。

产出：assets/ep01/EP01_typography.mp4（1080x1920 / 60s / 含音频设计）
用法：FFMPEG_BIN=<full ffmpeg> python3 tools/make_ep01.py
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/japan-ai-short-drama/assets/ep01"
TMP = Path(os.environ.get("EP_TMP", "/tmp/claude-0/ep01"))
CHROME = os.environ.get(
    "CHROME_BIN", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
FFMPEG = os.environ.get(
    "FFMPEG_BIN",
    "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/"
    "ffmpeg-linux-x86_64-v7.0.2")

W, H, FPS = 1080, 1920, 30

# ---------------------------------------------------------------------------
# 时间线。kind 决定视觉样式：
#   scene  场景提示（小字灰）
#   line   说出口的台词（白，带说话人标签）
#   inner  心声（金，带「心の声」标签，发光）
#   mono   女主独白（白，居中，无标签）
#   shift  改写瞬间（金字扭曲＋闪白）
#   title  片名/结尾
# ---------------------------------------------------------------------------
BEATS = [
    dict(t=2.5, kind="scene", who="", text="会議室・午後三時"),
    dict(t=4.0, kind="line", who="人事課長",
         text="次回の更新は、|ございません。"),
    dict(t=3.5, kind="inner", who="課長",
         text="これで係長の失点は消える。"),
    dict(t=4.0, kind="mono", who="",
         text="今、この人が|言わなかった言葉が聞こえた。"),
    dict(t=3.5, kind="mono", who="",
         text="三年間、一度も遅刻しなかった。|それだけだった。"),
    dict(t=4.0, kind="inner", who="係長",
         text="この報告書、名前さえ変えれば|私の実績。"),
    dict(t=3.5, kind="mono", who="", text="あの報告書を書いたのは、私だ。"),
    dict(t=3.5, kind="mono", who="", text="三か月、毎晩ひとりで。"),
    dict(t=3.0, kind="mono", who="", text="そのとき、気づいた。"),
    dict(t=3.0, kind="mono", who="", text="——聞こえるだけじゃない。"),
    dict(t=2.5, kind="shift", who="", text="書き換える"),
    dict(t=4.5, kind="line", who="人事課長",
         text="……いや、彼女の契約は、|継続で。"),
    dict(t=3.0, kind="scene", who="", text="会議室が、静かになった。"),
    dict(t=3.5, kind="mono", who="", text="本音は、書き換えられる。"),
    dict(t=2.5, kind="scene", who="", text="着信 ── 母"),
    dict(t=3.5, kind="line", who="母", text="もしもし、〇〇？"),
    dict(t=3.5, kind="mono", who="", text="……この声、誰？"),
    dict(t=2.0, kind="title", who="", text="書き換えられた本音"),
]

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%(w)dpx; height:%(h)dpx; overflow:hidden; }
body {
  background: radial-gradient(120%% 80%% at 50%% 38%%, #18202c 0%%, #0b0f16 100%%);
  font-family:"IPAPGothic","IPAGothic","Noto Sans JP",sans-serif;
  display:flex; flex-direction:column; justify-content:center;
  align-items:flex-start; padding:0 92px 240px 92px;
}
.label {
  font-size:34px; color:#8b96a5; letter-spacing:.18em;
  margin-bottom:34px;
}
.label.inner { color:#c8a45c; }
.txt { white-space:nowrap; line-height:1.6; letter-spacing:.01em; }

/* 说出口的话：白，冷静 */
.line .txt { color:#f2f0ec; font-size:%(fs)dpx;
  text-shadow:0 2px 26px rgba(0,0,0,.6); }

/* 心声：金，发光，视觉上"不属于这个房间" */
.inner .txt { color:#e8c67a; font-size:%(fs)dpx;
  text-shadow:0 0 34px rgba(232,198,122,.45), 0 2px 18px rgba(0,0,0,.6); }

/* 独白：白，略小，靠内 */
.mono .txt { color:#e6e3dd; font-size:%(fs)dpx;
  text-shadow:0 2px 22px rgba(0,0,0,.6); }

/* 场景提示：灰，小 */
.scene .txt { color:#7d879a; font-size:%(fs)dpx; letter-spacing:.14em; }

/* 改写瞬间 */
.shift .txt { color:#fff6e0; font-size:%(fs)dpx;
  text-shadow:0 0 60px rgba(255,246,224,.85), 0 0 120px rgba(232,198,122,.5); }

/* 片名 */
.title { align-items:center; }
.title .txt { color:#f2f0ec; font-size:%(fs)dpx; letter-spacing:.22em; }

.rule { width:88px; height:4px; background:#c8a45c; margin-bottom:52px; }
"""

HTML = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<style>%(css)s</style></head>
<body class="%(kind)s">%(rule)s%(label)s<div class="txt">%(text)s</div></body>
</html>"""

CONTENT_W = W - 92 * 2


def _w(line: str) -> float:
    return sum(0.5 if ord(c) < 0x2E80 else 1.0 for c in line)


def fontsize(text: str, kind: str) -> int:
    hi = {"scene": 46, "title": 66, "shift": 92}.get(kind, 72)
    lo = {"scene": 32, "title": 48, "shift": 60}.get(kind, 42)
    longest = max(_w(l) for l in text.split("|"))
    return max(lo, min(hi, int(CONTENT_W / longest * 0.96)))


def render(beat: dict, path: Path, idx: int) -> None:
    kind = beat["kind"]
    fs = fontsize(beat["text"], kind)
    label = ""
    if beat["who"]:
        cls = "label inner" if kind == "inner" else "label"
        suffix = "（心の声）" if kind == "inner" else ""
        label = f'<div class="{cls}">{beat["who"]}{suffix}</div>'
    rule = '<div class="rule"></div>' if kind in ("mono", "title") else ""
    html = HTML % dict(
        css=CSS % dict(w=W, h=H, fs=fs),
        kind=kind, rule=rule, label=label,
        text=beat["text"].replace("|", "<br>"),
    )
    hf = TMP / f"b{idx:02d}.html"
    hf.write_text(html, encoding="utf-8")
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        f"--screenshot={path}", f"--window-size={W},{H}", f"file://{hf}",
    ], check=True, capture_output=True)


def build_audio(dst: Path) -> None:
    """音频设计：底噪room tone；心声处叠 200Hz 低频耳鸣；改写处上扬音。"""
    total = sum(b["t"] for b in BEATS)
    inner_starts, shift_start, acc = [], None, 0.0
    for b in BEATS:
        if b["kind"] == "inner":
            inner_starts.append(acc)
        if b["kind"] == "shift":
            shift_start = acc
        acc += b["t"]

    inputs, parts, labels = [], [], []
    # 底噪
    inputs += ["-f", "lavfi", "-t", f"{total}",
               "-i", "anoisesrc=color=brown:amplitude=0.05"]
    parts.append("[0:a]lowpass=f=420,volume=0.09[base]")
    labels.append("[base]")
    # 心声耳鸣
    for i, st in enumerate(inner_starts):
        idx = len(inputs) // 6 + i  # 占位，实际用枚举顺序
    n = 1
    for st in inner_starts:
        inputs += ["-f", "lavfi", "-t", "3.2", "-i", "sine=frequency=200"]
        parts.append(
            f"[{n}:a]volume=0.10,afade=t=in:st=0:d=0.5,"
            f"afade=t=out:st=2.4:d=0.8,adelay={int(st*1000)}|{int(st*1000)}"
            f"[in{n}]")
        labels.append(f"[in{n}]")
        n += 1
    # 改写上扬音
    if shift_start is not None:
        inputs += ["-f", "lavfi", "-t", "2.2",
                   "-i", "sine=frequency=120:sample_rate=44100"]
        parts.append(
            f"[{n}:a]volume=0.14,afade=t=in:st=0:d=1.6,"
            f"afade=t=out:st=1.8:d=0.4,"
            f"adelay={int(shift_start*1000)}|{int(shift_start*1000)}[sh]")
        labels.append("[sh]")
        n += 1

    fc = ";".join(parts) + ";" + "".join(labels) + \
        f"amix=inputs={len(labels)}:duration=longest:normalize=0," \
        f"volume=1.6,aformat=sample_fmts=fltp:sample_rates=44100:" \
        f"channel_layouts=stereo[aout]"
    subprocess.run([FFMPEG, "-y", *inputs, "-filter_complex", fc,
                    "-map", "[aout]", "-t", f"{total}", str(dst)],
                   check=True, capture_output=True)


def build_video(pngs: list, audio: Path, dst: Path) -> None:
    """每拍淡入淡出 + 极缓推进，串接后配音。"""
    inputs, parts, labels = [], [], []
    for i, (png, beat) in enumerate(zip(pngs, BEATS)):
        d = beat["t"]
        inputs += ["-loop", "1", "-t", f"{d}", "-i", str(png)]
        fo = max(0.0, d - 0.45)
        parts.append(
            f"[{i}:v]fps={FPS},scale={W}:{H},setsar=1,"
            f"zoompan=z='min(1+0.00022*on,1.04)':d=1"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
            f"fade=t=in:st=0:d=0.45,fade=t=out:st={fo:.2f}:d=0.45,"
            f"format=yuv420p[v{i}]")
        labels.append(f"[v{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + \
        f"concat=n={len(labels)}:v=1:a=0[vout]"
    subprocess.run([
        FFMPEG, "-y", *inputs, "-i", str(audio),
        "-filter_complex", fc, "-map", "[vout]", "-map", f"{len(BEATS)}:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "21",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", str(dst),
    ], check=True, capture_output=True)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, b in enumerate(BEATS):
        p = TMP / f"b{i:02d}.png"
        render(b, p, i)
        pngs.append(p)
    print(f"  排版渲染完成：{len(pngs)} 拍")
    audio = TMP / "bed.wav"
    build_audio(audio)
    print(f"  音频设计完成：{audio.stat().st_size//1024}KB")
    dst = OUT / "EP01_typography.mp4"
    build_video(pngs, audio, dst)
    total = sum(b["t"] for b in BEATS)
    print(f"\n成片：{dst}")
    print(f"  时长 {total:.1f}s ／ {dst.stat().st_size//1024}KB ／ {W}x{H}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
