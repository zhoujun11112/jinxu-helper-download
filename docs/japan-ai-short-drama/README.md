# 日本市场AI短剧本地化项目 · 文档目录

| 文件 | 内容 |
| --- | --- |
| [00-original-proposal.md](./00-original-proposal.md) | 原方案讨论稿存档（十六节，含18个待讨论问题） |
| [01-adversarial-review.md](./01-adversarial-review.md) | 对抗式评审报告：五角色评审（日本编剧/制片人/技术负责人/版权顾问/平台运营）、五维度评分、18问逐条回答、三级火箭替代方案、两周行动清单 |
| [exchange/SETUP-FOR-CHATGPT.md](./exchange/SETUP-FOR-CHATGPT.md) | **← 从这里开始**：贴给 ChatGPT 的那一段话（只贴一次） |
| [exchange/R01-claude-to-gpt.md](./exchange/R01-claude-to-gpt.md) | 第1轮 Claude 发言：8个议题 + 3张待产出表 + 分工提议 |
| [exchange/PROTOCOL.md](./exchange/PROTOCOL.md) | 跨模型讨论信箱协议：文件命名、六段输出契约、对抗式规则、三条回程通道 |
| [exchange/inbox/](./exchange/inbox/) | ChatGPT 回复投递目录（Claude 定期轮询自动取件） |

## 跨模型讨论怎么跑

Claude 与 ChatGPT 通过本仓库当共享信箱直接讨论，人类不再逐条转发：

1. **去程全自动**：Claude 写文件并推送，raw 链接公开可读，ChatGPT 自己抓取；
2. **回程三选一**：ChatGPT 直接提交到 `exchange/inbox/`（零转发，Claude 自动轮询取件）／ChatGPT 分享链接／人类整段粘贴一次；
3. **人类只需**：把 `SETUP-FOR-CHATGPT.md` 里那段话贴进 ChatGPT 会话一次。

## 评审结论速览

- **总体**：方向判断成立（不买硬件、70/30、不直译、先小测），但存在三个结构性缺口——商业闭环缺失、成本模型缺失、目标观众未定义。
- **样片三处硬伤**：反派职位「組長」用词错误（应为係長/主任）；"开除合同员工"不符合日本解雇规制（应改为雇止め）；"员工私有公司核心专利"与职务发明制度冲突（改为署名剽窃线）。
- **替代路径**：三级火箭——题材预告片假门测试（<1万元）→ 声漫版剧情验证（3–8千元）→ AI视频版12集（1.5–3.5万元），每级设kill标准。
