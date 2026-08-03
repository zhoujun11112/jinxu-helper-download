#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EP01 日语配音生成器（离线合成）

引擎：pyopenjtalk（Open JTalk / HTS）+ mei_normal 声库，完全离线，不联网。
四个角色共用一个声库，靠音高与语速区分——这是单声库条件下的标准做法。

⚠️ 授权：mei_normal 随 MMDAgent 发布，附带其自身许可条款。
   本产物仅供**内部试听与节奏验证**。正式发布前必须改用有明确商用授权的
   TTS 声库或真人配音，并留存授权凭证（见 T4 合规基线）。

产出：pipeline/voice/ep01/bXX.wav
用法：FFMPEG_BIN=<ffmpeg> python3 tools/make_voice.py
"""

import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import pyopenjtalk

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "pipeline/voice/ep01"
TMP = Path(os.environ.get("EP_TMP", "/tmp/claude-0/ep01")) / "raw"
FFMPEG = os.environ.get(
    "FFMPEG_BIN",
    "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/"
    "ffmpeg-linux-x86_64-v7.0.2")

sys.path.insert(0, str(ROOT / "tools"))
from make_ep01 import BEATS  # noqa: E402

# 角色声音参数：pitch 为音高系数（<1 更低沉），tempo 为语速系数
VOICE = {
    "人事課長": dict(pitch=0.78, tempo=0.98, gain=1.00),  # 52岁男性，事务性
    "課長":     dict(pitch=0.78, tempo=0.96, gain=0.95),  # 同上（心声更慢）
    "係長":     dict(pitch=1.08, tempo=1.08, gain=0.95),  # 38岁女性，锋利
    "母":       dict(pitch=0.93, tempo=0.88, gain=1.00),  # 温和，日常
    "":         dict(pitch=1.00, tempo=0.94, gain=1.00),  # 女主独白，偏慢克制
}


def synth(text: str, dst: Path) -> None:
    """离线合成为 48k 单声道 wav。"""
    x, sr = pyopenjtalk.tts(text)
    x = x / max(1e-9, np.abs(x).max()) * 0.92
    pcm = (x * 32767).astype(np.int16)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def shape(src: Path, dst: Path, pitch: float, tempo: float, gain: float,
          reverb: bool) -> float:
    """变调不变速 + 语速调整 + 心声混响；返回成品时长（秒）。"""
    sr = 48000
    # asetrate 改变采样率实现变调，aresample 复原，atempo 补回时长
    chain = (f"asetrate={int(sr*pitch)},aresample={sr},"
             f"atempo={1/pitch:.4f},atempo={tempo:.4f}")
    if reverb:
        # 心声：轻混响（短延迟叠加）+ 高频略削，听感"不在这个房间里"
        chain += ",aecho=0.8:0.85:28|46:0.28|0.18,lowpass=f=7000"
    chain += f",volume={gain},afade=t=in:st=0:d=0.05"
    subprocess.run([FFMPEG, "-y", "-i", str(src), "-af", chain,
                    "-ar", "44100", "-ac", "1", str(dst)],
                   check=True, capture_output=True)
    out = subprocess.run(
        [FFMPEG, "-i", str(dst), "-f", "null", "-"],
        capture_output=True, text=True)
    for tok in out.stderr.split():
        if tok.startswith("time="):
            h, m, s = tok[5:].split(":")
            return int(h) * 3600 + int(m) * 60 + float(s.rstrip(","))
    return 0.0


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    total = 0.0
    print(f"{'文件':<10}{'角色':<10}{'时长':>7}  台词")
    print("-" * 78)
    for i, b in enumerate(BEATS):
        if b["kind"] not in ("line", "inner", "mono"):
            continue
        who = b["who"]
        v = VOICE.get(who, VOICE[""])
        text = b["text"].replace("|", "").replace("——", "、")
        text = text.replace("〇〇", "ハルカ")          # 占位符换角色名
        text = re.sub(r"^[、。…\s]+", "", text)        # 句首停顿会让引擎报警
        raw = TMP / f"b{i:02d}_raw.wav"
        dst = OUT / f"b{i:02d}.wav"
        synth(text, raw)
        dur = shape(raw, dst, v["pitch"], v["tempo"], v["gain"],
                    reverb=(b["kind"] == "inner"))
        total += dur
        print(f"b{i:02d}.wav  {who or '女主':<10}{dur:>6.2f}s  {text}")
    print(f"\n合成完成：{OUT}  （语音总时长 {total:.1f}s）")
    print("⚠️ mei 声库仅供内部试听，正式发布前须换商用授权声库或真人配音。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
