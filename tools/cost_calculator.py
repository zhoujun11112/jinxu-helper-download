#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本AI短剧 · 参数化成本计算器
交付编号 T3（应 ChatGPT R01 要求）

用法：
    python3 tools/cost_calculator.py              # 跑乐观/基准/悲观三档
    python3 tools/cost_calculator.py --t6         # 跑 T6 指定的统一假设
    python3 tools/cost_calculator.py --sens       # 敏感度分析：哪个变量最致命

设计要点：
  1. 「通过率」与「平均抽数」是同一个变量的两种写法（抽数 = 1/通过率）。
     本计算器只接受通过率作为输入，抽数为派生值，避免双重计价。
  2. 所有单价均为 2026 年初量级的估计，标注 [需核实]。
     计算器的价值在结构与敏感度，不在绝对值。
  3. 人工按「若外包需支付的现金」计入；内部承担时用 --internal 扣除。
"""

import argparse
from dataclasses import dataclass, field, asdict


@dataclass
class Params:
    """全部可调变量。单位：人民币元、秒、小时、字。"""

    # ---- 规模 ----
    episodes: int = 12                    # 集数
    sec_per_episode: int = 60             # 每集秒数
    effective_shots: int = 120            # 有效镜头数（成片里真正用上的）
    sec_per_shot: float = 5.0             # 单镜头平均秒数

    # ---- 生成通过率（抽数 = 1/通过率，不单独输入抽数）----
    video_pass_rate: float = 0.20         # 视频单次生成可用率
    keyframe_pass_rate: float = 0.30      # 关键帧单次生成可用率
    complex_shot_ratio: float = 0.10      # 复杂镜头占比（通过率打折）
    complex_penalty: float = 0.5          # 复杂镜头通过率折扣系数

    # ---- 单价 [需核实] ----
    price_video_per_gen: float = 2.5      # 每次视频生成（5秒档，批量档平台）
    premium_shot_ratio: float = 0.08      # 高端模型镜头占比（每集1-2个情绪镜头）
    price_video_premium: float = 18.0     # 高端模型每次生成
    price_keyframe_per_gen: float = 0.35  # 每张关键帧图片
    keyframes_per_shot: float = 1.6       # 每镜头需要的关键帧数（首帧/首尾帧）

    lipsync_shot_ratio: float = 0.30      # 需要口型同步的镜头占比
    price_lipsync_per_shot: float = 2.5   # 每镜头口型
    upscale_shot_ratio: float = 1.0       # 需要高清放大的镜头占比
    price_upscale_per_shot: float = 0.8   # 每镜头放大

    # ---- 配音 ----
    tts_price_per_min: float = 45.0       # 日语TTS每分钟成片语音（含重录）
    tts_retake_factor: float = 1.8        # 重录系数

    # ---- 剧本与监修 ----
    script_cost: float = 6000.0           # 母剧拆解+日本化改编+分镜脚本
    jp_review_chars: int = 12000          # 日语监修字数
    price_review_per_char: float = 0.30   # 每字单价
    review_rounds: float = 2.0            # 监修轮数（含成片终审折算）

    # ---- 资产 ----
    asset_cost: float = 2500.0            # 角色定妆+场景底图+道具

    # ---- 人工 ----
    edit_hours: float = 70.0              # 剪辑/字幕/贴字/合成工时
    price_edit_per_hour: float = 120.0    # 外包时薪

    # ---- 锁定后变更（T1 三级变更控制）----
    l1_changes_per_ep: float = 2.0        # 每集 L1 修改数（时长中性，单句重录）
    l1_hours_each: float = 0.4            # 每处 L1 的重录+替换工时
    l2_changes_total: float = 2.0         # 全片 L2 修改总数（结构性，回退animatic）
    l2_hours_each: float = 3.5            # 每处 L2 的回退返工工时（含重生成受影响镜头）
    l2_regen_shots_each: float = 3.0      # 每处 L2 平均牵连需重生成的镜头数

    # ---- 投放测试 ----
    audience_groups: int = 3              # 测试人群分组数
    creatives_per_group: int = 2          # 每组素材版本数
    budget_per_creative: float = 1200.0   # 每素材达到显著样本的预算
    test_rounds: float = 1.0              # 测试轮数

    # ---- 其他 ----
    music_cost: float = 700.0             # 商用曲库+音效
    overhead_cost: float = 1800.0         # 云盘、备份、项管、质检
    option_fee: float = 0.0               # 版权开发期权费（单列，不计入主合计）

    label: str = "基准"


def compute(p: Params) -> dict:
    """返回逐项成本与合计。"""

    # --- 视频生成：按通过率反推总生成次数 ---
    normal_shots = p.effective_shots * (1 - p.complex_shot_ratio)
    complex_shots = p.effective_shots * p.complex_shot_ratio

    normal_gens = normal_shots / max(p.video_pass_rate, 1e-6)
    complex_gens = complex_shots / max(p.video_pass_rate * p.complex_penalty, 1e-6)
    total_gens = normal_gens + complex_gens

    premium_gens = total_gens * p.premium_shot_ratio
    batch_gens = total_gens - premium_gens
    video_cost = batch_gens * p.price_video_per_gen + premium_gens * p.price_video_premium

    # --- 关键帧 ---
    keyframe_gens = (p.effective_shots * p.keyframes_per_shot) / max(p.keyframe_pass_rate, 1e-6)
    keyframe_cost = keyframe_gens * p.price_keyframe_per_gen

    # --- 口型与放大 ---
    lipsync_cost = p.effective_shots * p.lipsync_shot_ratio * p.price_lipsync_per_shot
    upscale_cost = p.effective_shots * p.upscale_shot_ratio * p.price_upscale_per_shot

    # --- 配音 ---
    total_minutes = p.episodes * p.sec_per_episode / 60.0
    tts_cost = total_minutes * p.tts_price_per_min * p.tts_retake_factor

    # --- 监修 ---
    review_cost = p.jp_review_chars * p.price_review_per_char * p.review_rounds

    # --- 剪辑 ---
    edit_cost = p.edit_hours * p.price_edit_per_hour

    # --- 锁定后变更返工（T1 三级变更控制）---
    l1_hours = p.episodes * p.l1_changes_per_ep * p.l1_hours_each
    l2_hours = p.l2_changes_total * p.l2_hours_each
    change_labor = (l1_hours + l2_hours) * p.price_edit_per_hour
    l2_regen = (p.l2_changes_total * p.l2_regen_shots_each
                / max(p.video_pass_rate, 1e-6) * p.price_video_per_gen)
    change_cost = change_labor + l2_regen

    # --- 投流 ---
    ad_cost = (p.audience_groups * p.creatives_per_group
               * p.budget_per_creative * p.test_rounds)

    rows = {
        "剧本：母剧拆解＋日本化改编＋分镜": p.script_cost,
        "日语母语监修": review_cost,
        "角色与场景资产": p.asset_cost,
        "关键帧生成": keyframe_cost,
        "视频生成": video_cost,
        "口型同步": lipsync_cost,
        "高清放大": upscale_cost,
        "日语配音": tts_cost,
        "音乐与音效": p.music_cost,
        "剪辑／字幕／贴字／合成": edit_cost,
        "锁定后变更返工（L1+L2）": change_cost,
        "投流测试": ad_cost,
        "项管／存储／质检": p.overhead_cost,
    }
    subtotal = sum(rows.values())

    derived = {
        "总成片分钟": round(total_minutes, 1),
        "视频总生成次数": round(total_gens),
        "等效平均抽数": round(total_gens / p.effective_shots, 2),
        "关键帧总生成次数": round(keyframe_gens),
        "投放测试单元数": p.audience_groups * p.creatives_per_group,
        "每分钟成片成本": round(subtotal / total_minutes),
        "每有效镜头成本": round(subtotal / p.effective_shots),
        "纯API现金（生成+口型+放大+配音）": round(
            video_cost + keyframe_cost + lipsync_cost + upscale_cost + tts_cost),
    }

    return {"label": p.label, "rows": rows, "subtotal": subtotal,
            "option_fee": p.option_fee, "derived": derived}


def render(res: dict) -> str:
    out = [f"\n{'='*62}", f" 场景：{res['label']}", f"{'='*62}"]
    for k, v in res["rows"].items():
        out.append(f"  {k:<32}{v:>12,.0f}")
    out.append(f"  {'-'*44}")
    out.append(f"  {'合计（不含版权）':<32}{res['subtotal']:>12,.0f}")
    if res["option_fee"]:
        out.append(f"  {'版权开发期权费（单列）':<32}{res['option_fee']:>12,.0f}")
        out.append(f"  {'含期权总额':<32}{res['subtotal']+res['option_fee']:>12,.0f}")
    out.append(f"  {'-'*44}")
    for k, v in res["derived"].items():
        out.append(f"  · {k:<30}{v:>12,}")
    return "\n".join(out)


def scenarios() -> list:
    """乐观／基准／悲观三档。差异集中在通过率、单价、人工和投流。"""
    opt = Params(
        label="乐观",
        video_pass_rate=0.33, keyframe_pass_rate=0.45,
        price_video_per_gen=1.8, premium_shot_ratio=0.05,
        lipsync_shot_ratio=0.20, edit_hours=45, price_edit_per_hour=90,
        script_cost=4000, jp_review_chars=10000, price_review_per_char=0.25,
        asset_cost=1500, budget_per_creative=800, complex_shot_ratio=0.06,
        overhead_cost=1000, music_cost=300,
    )
    base = Params(label="基准")
    pes = Params(
        label="悲观",
        video_pass_rate=0.12, keyframe_pass_rate=0.20,
        price_video_per_gen=3.5, premium_shot_ratio=0.12,
        price_video_premium=25.0,
        lipsync_shot_ratio=0.40, edit_hours=110, price_edit_per_hour=180,
        script_cost=9000, jp_review_chars=15000, price_review_per_char=0.45,
        review_rounds=3.0, asset_cost=4500,
        budget_per_creative=2200, test_rounds=1.5, complex_shot_ratio=0.18,
        overhead_cost=3000, music_cost=1200, tts_price_per_min=70,
    )
    return [opt, base, pes]


def t6_assumptions() -> list:
    """ChatGPT 在 T6 中指定的统一假设，用于双方对账。"""
    common = dict(
        effective_shots=120, sec_per_shot=5.0,
        video_pass_rate=0.20,          # 平均5次生成 = 通过率20%
        lipsync_shot_ratio=0.30,
        complex_shot_ratio=0.10,
        edit_hours=70,
        audience_groups=3, creatives_per_group=2,
    )
    lo = Params(label="T6统一假设·下沿", **common,
                price_video_per_gen=1.8, price_edit_per_hour=90,
                script_cost=4000, jp_review_chars=10000,
                price_review_per_char=0.25, asset_cost=1500,
                budget_per_creative=800, keyframe_pass_rate=0.45,
                premium_shot_ratio=0.05, overhead_cost=1000, music_cost=300)
    hi = Params(label="T6统一假设·上沿", **common,
                price_video_per_gen=3.5, price_edit_per_hour=180,
                script_cost=9000, jp_review_chars=15000,
                price_review_per_char=0.45, review_rounds=3.0,
                asset_cost=4500, budget_per_creative=2200,
                keyframe_pass_rate=0.20, premium_shot_ratio=0.12,
                price_video_premium=25.0, overhead_cost=3000,
                music_cost=1200, tts_price_per_min=70)
    return [lo, hi]


def sensitivity() -> str:
    """单变量敏感度：各变量 ±50% 对总额的影响，找出最致命的假设。"""
    base = Params()
    base_total = compute(base)["subtotal"]
    knobs = [
        ("视频通过率", "video_pass_rate", 0.5),
        ("视频单价", "price_video_per_gen", 1.5),
        ("剪辑工时", "edit_hours", 1.5),
        ("剪辑时薪", "price_edit_per_hour", 1.5),
        ("每素材投流预算", "budget_per_creative", 1.5),
        ("有效镜头数", "effective_shots", 1.5),
        ("口型镜头占比", "lipsync_shot_ratio", 1.5),
        ("监修单价", "price_review_per_char", 1.5),
        ("高端模型镜头占比", "premium_shot_ratio", 1.5),
    ]
    lines = [f"\n{'='*62}", " 敏感度分析：单变量恶化后总额变化（基准 = "
             f"{base_total:,.0f} 元）", f"{'='*62}"]
    results = []
    for name, attr, factor in knobs:
        p = Params(**asdict(base))
        p.label = name
        setattr(p, attr, getattr(base, attr) * factor)
        total = compute(p)["subtotal"]
        delta = total - base_total
        results.append((name, factor, total, delta, delta / base_total * 100))
    results.sort(key=lambda r: abs(r[3]), reverse=True)
    for name, factor, total, delta, pct in results:
        arrow = "↑" if delta > 0 else "↓"
        lines.append(f"  {name:<18}×{factor:<5}→ {total:>10,.0f}  "
                     f"{arrow}{abs(delta):>8,.0f}  ({pct:+.1f}%)")
    lines.append("")
    lines.append("  结论：排在最前的变量决定预算生死，必须优先用实测数据替换估计值。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t6", action="store_true", help="跑 T6 指定的统一假设")
    ap.add_argument("--sens", action="store_true", help="敏感度分析")
    ap.add_argument("--internal", action="store_true",
                    help="剧本与剪辑由内部承担，从现金支出中扣除")
    args = ap.parse_args()

    if args.sens:
        print(sensitivity())
        return

    plist = t6_assumptions() if args.t6 else scenarios()
    for p in plist:
        if args.internal:
            p.script_cost = 0.0
            p.edit_hours = 0.0
        print(render(compute(p)))

    print("\n注：全部单价为 2026 年初量级估计 [需核实]。")
    print("    计算器的价值在结构与敏感度排序，不在绝对值。")
    print("    通过率与平均抽数是同一变量（抽数=1/通过率），只输入通过率。\n")


if __name__ == "__main__":
    main()
