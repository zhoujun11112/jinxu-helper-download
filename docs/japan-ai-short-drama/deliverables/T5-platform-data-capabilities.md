# T5 · 平台数据能力核查

交付编号 T5 ｜ 应 ChatGPT R01 要求 ｜ 核查日期 2026-08-03

**标注口径**：`已核实` = 有平台官方文档或多方一致的公开报道；`第三方来源` = 仅见于行业媒体/第三方工具商，未见官方文档，需后台实测确认；`需商务询问` = 公开渠道查不到，必须直接问平台或采购方。

---

## 核查结果总表

| 能力 | TikTok（日本区） | YouTube Shorts | 短剧App |
|---|---|---|---|
| 逐秒/分段留存曲线 | `第三方来源` 多家报道 2026 版创作者后台提供逐秒留存曲线（含回看点、完播比例） | `第三方来源` 提供 Shorts 留存图与 **Viewed vs Swiped away**（Content 标签下按 Shorts 筛选） | `需商务询问` |
| 观众年龄/性别 | `第三方来源` 账号级粉丝画像可得；**单条视频级受众拆分需实测确认** | `第三方来源` Studio 提供人口统计 | `需商务询问` |
| 系列/下一集点击 | `需商务询问` 合集功能数据粒度未见官方说明 | `第三方来源` 播放列表数据可得 | `需商务询问` |
| **同素材 A/B 测试** | **`已核实` 广告端支持**：Ads Manager Split Testing，四类（创意/定向/出价/版位），要求 ≥7天、90%置信度；2026 版增加 campaign 级与多变量测试。**自然流不支持** | **`已核实` 不支持 Shorts**：Test & Compare 仅限长视频缩略图；2026-07-25 开放 Shorts 自定义封面时**明确排除 A/B 测试** | `需商务询问` |
| **替换已发布视频** | **`已核实` 不支持**：仅可在有限时间内改描述/话题/封面；改动画面内容必须删除重传 | **`已核实` 不支持**：官方仅提供裁剪、改标题描述、加卡片；替换视频文件会产生新 URL。（有零星报道称部分账号有未公开的替换功能，无官方文档，不可作为方案依据） | `需商务询问` |
| AI内容标识 | `已核实` 有 AIGC 标注机制 | `已核实` 要求对写实且有实质性生成/修改的内容披露 | `需商务询问` |
| 投放中版本实验 | `已核实` 广告账户内可做（同 Split Testing） | `已核实` 广告端可做，Shorts 自然流不可 | 不适用 |

---

## 对方案的三个直接后果

### 后果1：「发布后定点重拍」在自然流不成立——被平台机制否决

两大平台都**不支持替换已发布视频的画面内容**。删了重传等于：原有播放量、评论、收藏、追更链条全部清零，重新进入冷启动。所以"哪一秒流失就换掉哪个镜头、48小时替换重发"这个动作，在自然流里**没有承载它的平台机制**。

这一条证实了 ChatGPT 在 R01 对我的攻击（其第3点），我在 R02 中正式撤回该主张的自然流部分。

### 后果2：「发布前多版本测试」在自然流同样不成立

YouTube 的 Test & Compare 明确不支持 Shorts；TikTok 自然流也没有官方 A/B 机制。所以 ChatGPT 提出的替代主张——"发布前多版本测试"——如果指的是自然流，**同样没有平台机制支撑**。

**双方的主张在自然流场域都不成立。**

### 后果3：唯一成立的实验场是广告账户

TikTok Ads Manager 的 Split Testing 是本次核查中**唯一有官方文档支撑的变量实验能力**：四类测试、90%置信度、≥7天窗口。

因此正确结论不是"发布前 vs 发布后"，而是：

> **所有变量实验（钩子、镜头、台词、结尾）必须在广告账户内完成；自然流只承担最终发布与长尾。**

这同时也改写了预算结构——投流预算不再只是"买样本"，而是**唯一的实验基础设施成本**，属于研发费而非市场费。

---

## 对 KPI 门槛的连带修正

TikTok 官方 Split Test 要求 **≥7天** 才能形成有效结论。这与我在 R01 提的"48小时迭代"直接冲突。修正为：

- **7天** = 一个有效实验周期（受平台机制约束，不可压缩）
- 一轮题材测试 = 7天，不是 48 小时
- 三级火箭的第0级"1–2周"因此是合理的，但只够跑 **1–2 个实验周期**，不够跑三个题材各两版

→ 这一条直接支持我在 R02 中对"25–44岁测试池过宽"的攻击：分组越多，7天窗口内能测的变量越少。

---

## 仍需商务询问的清单（无法从公开渠道解决）

必须在接触日本短剧 App 采购方时一并问清：

1. 后台是否提供逐集留存与追看漏斗，粒度到第几秒
2. 是否接受 AI 写实风/2.5D/AI 配音，各自的质量线
3. 最低集数、单集时长、交付规格（分辨率、字幕格式、母版要求）
4. 能否先采购 12 集，后续补足 60–80 集
5. 买断 / 保底＋分成 / 纯分成，各自的价格区间
6. 对中国母剧版权链的证明要求（要到哪一层）
7. AI 内容标识与声音授权的合规要求
8. 平台自身的用户年龄结构（这是解决 D1 分歧最直接的证据源）

第 8 条尤其关键：**它能一次性终结我和 ChatGPT 关于目标年龄层的事实分歧**，而且只需要一次商务对话，成本远低于任何一轮广告测试。

---

## 来源

- [About Split Testing | TikTok Ads Manager](https://ads.tiktok.com/help/article/split-testing?lang=en)
- [Split Test Best Practices | TikTok Ads Manager](https://ads.tiktok.com/help/article/split-test-best-practices?lang=en)
- [Replace or delete your video - YouTube Help](https://support.google.com/youtube/answer/55770?hl=en&co=GENIE.Platform%3DDesktop)
- [YouTube ends 2-year wait for Shorts thumbnails but blocks A/B testing](https://ppc.land/youtube-ends-2-year-wait-for-shorts-thumbnails-but-blocks-a-b-testing/)
- [Viewed vs. Swiped Away: The Only YouTube Shorts Metric That Matters](https://reelrise.app/guide/viewed-vs-swiped-away-the-only-youtube-shorts-metric-that-matters/)
- [YouTube Shorts Analytics Metrics Explained](https://retensis.com/blog/youtube-shorts-analytics-metrics-explained)
- [TikTok Analytics: The Complete 2026 Guide for Creators](https://socialhunt.co/resources/tiktok-analytics-complete-guide)
- [TikTok Retention Rate Benchmarks 2026](https://retensis.com/blog/tiktok-retention-rate-benchmarks-2026)
- [How to Edit a TikTok Video After Posting](https://async.com/blog/how-to-edit-a-tiktok-video-after-posting/)
