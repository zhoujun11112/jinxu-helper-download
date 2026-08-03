#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本AI短剧 · 第一阶段流水线（人工调用工具 + 台账纪律）

设计原则（四轮讨论共识）：
  不建后台、不建数据库、不建 RAG。单一真相源是一张 CSV。
  这一阶段自动化的只有三件事：文件命名、台账记录、成本统计——
  也就是人最容易偷懒、偷懒后果最严重的三件事。

命令：
  init      建立标准目录树
  prompts   导出批量提交用的提示词 CSV
  log       记录一次生成尝试（抽数、成本、通过与否）
  status    看板：进度、通过率、成本、按当前速率的预测总额
  gate      检查当前是否满足进入下一环节的条件
"""

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "pipeline"
SHOTS = PIPE / "shots.csv"
GENLOG = PIPE / "generations.csv"

# T1 十环节，目录树按此建立
STAGES = [
    "01_script", "02_audio_temp", "03_animatic", "04_keyframes",
    "05_video", "06_rough_cut", "07_audio_final", "08_lipsync",
    "09_titles", "10_master",
]

GENLOG_HEADER = ["ts", "ep", "shot", "kind", "attempts",
                 "usable", "cost_cny", "model", "note"]


def _read_shots() -> list:
    with SHOTS.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_shots(rows: list) -> None:
    with SHOTS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def name(ep: str, shot: str, kind: str, ver: int, ext: str) -> str:
    """统一文件命名：EP01_S04_keyframe_v3.png —— 全流程唯一标识。"""
    return f"{ep}_{shot}_{kind}_v{ver}.{ext}"


def cmd_init(args) -> int:
    eps = sorted({r["ep"] for r in _read_shots()})
    made = 0
    for ep in eps:
        for st in STAGES:
            d = PIPE / "production" / ep / st
            d.mkdir(parents=True, exist_ok=True)
            made += 1
    for d in ("assets/characters", "assets/scenes", "assets/audio", "delivery"):
        (PIPE / d).mkdir(parents=True, exist_ok=True)
        made += 1
    if not GENLOG.exists():
        with GENLOG.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(GENLOG_HEADER)
    print(f"目录树就绪：{made} 个目录 → {PIPE}")
    print(f"命名规范示例：{name('EP01', 'S04', 'keyframe', 3, 'png')}")
    return 0


def cmd_prompts(args) -> int:
    """导出批量提交表。提示词正文在 S2 生成包里，这里只出可批处理的骨架。"""
    rows = _read_shots()
    out = PIPE / "prompt_batch.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ep", "shot", "kind", "duration_s", "size", "camera",
                    "scene", "characters", "ref_images", "outfile", "prompt"])
        for r in rows:
            refs = "|".join(f"assets/characters/{c}.png"
                            for c in r["characters"].split("/") if c)
            for kind, ext in (("keyframe", "png"), ("video", "mp4")):
                w.writerow([
                    r["ep"], r["shot"], kind, r["duration_s"], r["size"],
                    r["camera"], r["scene"], r["characters"],
                    refs + f"|assets/scenes/{r['scene']}.png",
                    name(r["ep"], r["shot"], kind, 1, ext), "",
                ])
    print(f"批量提交表 → {out}（{len(rows)*2} 行，prompt 列从 S2 生成包填入）")
    return 0


def cmd_log(args) -> int:
    GENLOG.parent.mkdir(parents=True, exist_ok=True)
    if not GENLOG.exists():
        with GENLOG.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(GENLOG_HEADER)
    with GENLOG.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            args.ep, args.shot, args.kind, args.attempts,
            "Y" if args.ok else "N", f"{args.cost:.2f}",
            args.model or "", args.note or "",
        ])
    if args.ok:
        rows = _read_shots()
        for r in rows:
            if r["ep"] == args.ep and r["shot"] == args.shot:
                r["status"] = "done" if args.kind == "video" else "keyframe_ok"
                r["attempts"] = str(int(r["attempts"] or 0) + args.attempts)
                r["cost_cny"] = f"{float(r['cost_cny'] or 0) + args.cost:.2f}"
        _write_shots(rows)
    print(f"已记录 {args.ep}_{args.shot} {args.kind}："
          f"{args.attempts} 抽 / {args.cost:.2f} 元 / "
          f"{'通过' if args.ok else '未通过'}")
    return 0


def cmd_status(args) -> int:
    rows = _read_shots()
    total = len(rows)
    done = sum(1 for r in rows if r["status"] == "done")
    kf_ok = sum(1 for r in rows if r["status"] in ("keyframe_ok", "done"))
    spent = sum(float(r["cost_cny"] or 0) for r in rows)
    attempts = sum(int(r["attempts"] or 0) for r in rows)

    gens = []
    if GENLOG.exists():
        with GENLOG.open(encoding="utf-8") as f:
            gens = list(csv.DictReader(f))
    tries = sum(int(g["attempts"]) for g in gens) or 0
    passes = sum(1 for g in gens if g["usable"] == "Y")
    pass_rate = (passes / len(gens) * 100) if gens else 0
    per_usable = (tries / passes) if passes else 0

    print(f"\n{'='*58}")
    print(f" 进度看板 · {rows[0]['ep'] if rows else '-'}")
    print(f"{'='*58}")
    print(f"  镜头总数            {total}")
    print(f"  关键帧通过          {kf_ok}/{total}")
    print(f"  成片完成            {done}/{total}")
    print(f"  累计抽数            {attempts}")
    print(f"  单次通过率          {pass_rate:.0f}%"
          + (f"（等效 {per_usable:.1f} 抽/可用）" if per_usable else ""))
    print(f"  已花费              {spent:,.2f} 元")
    if done:
        print(f"  按当前速率预测本集  {spent / done * total:,.2f} 元")
    print(f"\n  难度分布：", end="")
    for d in ("最易", "易", "中", "难"):
        n = sum(1 for r in rows if r["difficulty"] == d)
        if n:
            print(f"{d} {n}  ", end="")
    lip = sum(1 for r in rows if r["lipsync"] == "Y")
    print(f"\n  口型镜头：{lip}/{total}（{lip/total*100:.0f}%）")
    pending = [r["shot"] for r in rows if r["status"] == "pending"]
    if pending:
        print(f"\n  待生成：{' '.join(pending)}")
    print()
    return 0


def cmd_gate(args) -> int:
    """检查是否满足进入下一环节的条件（T1 三道硬门的自动化部分）。"""
    rows = _read_shots()
    total = len(rows)
    kf_ok = sum(1 for r in rows if r["status"] in ("keyframe_ok", "done"))
    checks = [
        ("关键帧全部通过盲评后方可进入视频生成",
         kf_ok == total, f"{kf_ok}/{total}"),
        ("口型镜头占比 ≤30%",
         sum(1 for r in rows if r["lipsync"] == "Y") / total <= 0.30,
         f"{sum(1 for r in rows if r['lipsync']=='Y')/total*100:.0f}%"),
        ("无「难」级镜头",
         not any(r["difficulty"] == "难" for r in rows),
         f"{sum(1 for r in rows if r['difficulty']=='难')} 个"),
        ("每镜时长 ≤8 秒",
         all(float(r["duration_s"]) <= 8 for r in rows),
         f"最长 {max(float(r['duration_s']) for r in rows):.1f}s"),
        ("总时长落在 45–75 秒",
         45 <= sum(float(r["duration_s"]) for r in rows) <= 75,
         f"{sum(float(r['duration_s']) for r in rows):.1f}s"),
    ]
    print()
    ok = True
    for label, passed, detail in checks:
        print(f"  [{'✓' if passed else '×'}] {label:<32} {detail}")
        ok &= passed
    print(f"\n  → {'可以进入下一环节' if ok else '有未满足项，不得推进'}\n")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="日本AI短剧第一阶段流水线")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="建立标准目录树")
    sub.add_parser("prompts", help="导出批量提交表")
    sub.add_parser("status", help="进度与成本看板")
    sub.add_parser("gate", help="检查能否进入下一环节")

    lg = sub.add_parser("log", help="记录一次生成尝试")
    lg.add_argument("ep")
    lg.add_argument("shot")
    lg.add_argument("--kind", default="keyframe",
                    choices=["keyframe", "video", "lipsync", "upscale"])
    lg.add_argument("--attempts", type=int, required=True)
    lg.add_argument("--cost", type=float, required=True)
    lg.add_argument("--model", default="")
    lg.add_argument("--note", default="")
    g = lg.add_mutually_exclusive_group(required=True)
    g.add_argument("--ok", action="store_true")
    g.add_argument("--fail", dest="ok", action="store_false")

    args = ap.parse_args()
    return {"init": cmd_init, "prompts": cmd_prompts,
            "log": cmd_log, "status": cmd_status, "gate": cmd_gate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
