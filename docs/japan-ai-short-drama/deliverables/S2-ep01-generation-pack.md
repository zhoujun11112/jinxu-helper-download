# S2 · EP01 生成包（可直接复制粘贴）

《書き換えられた本音》EP01 ｜ 11 镜 / 60 秒
**用法：按 STEP 0 → 1 → 2 → 3 顺序执行，不要跳步。角色定妆没做完就生成镜头，一致性必崩。**

提示词一律用英文（多数平台对英文理解更稳），画面内**绝对不出现任何文字**——所有日文后期贴。

---

## 通用负向词（每次生成都带上）

```
text, letters, words, watermark, signature, logo, subtitles, captions, writing, kanji, hiragana, katakana, chinese characters, multiple people, crowd, extra fingers, deformed hands, mutated hands, extra limbs, distorted face, asymmetrical eyes, exaggerated expression, open mouth wide, western facial features, caucasian, oversaturated, HDR, plastic skin, beauty filter, anime, cartoon, illustration, low quality, blurry, jpeg artifacts
```

---

# STEP 0 · 角色定妆（先做这一步，产出参考图）

每个角色生成 **正面 / 四分之三侧 / 侧面 / 表情四宫格**，共 4 张，挑出最稳的一套作为全剧参考图。**定妆图一旦选定就不再改**。

### 女主（HARUKA / 主角）

```
character reference sheet, photorealistic, 29-year-old Japanese woman, shoulder-length black bob hair tucked behind one ear, natural everyday face, plain and unremarkable beauty, slim build, small eyes, thin lips, no makeup, wearing navy cardigan over white blouse, Japanese regional bank clerk, calm restrained neutral expression, plain light gray studio background, soft even frontal lighting, sharp focus, full body and bust shots, 9:16 vertical
```

> **关键：不要美颜、不要网红脸。**"平凡"是这个角色的核心设定，也是日本观众相信她是合同员工的前提。prompt 里的 `plain and unremarkable beauty` 不能删。

### 課長（人事課長 / 50代男性）

```
character reference sheet, photorealistic, 52-year-old Japanese man, short graying hair neatly combed, thin metal-frame glasses, mild polite expression, navy business suit with white shirt and muted tie, Japanese bank human resources manager, slightly stooped posture, plain light gray studio background, soft even lighting, front and three-quarter views, 9:16 vertical
```

### 係長（反派 / 38歳女性）

```
character reference sheet, photorealistic, 38-year-old Japanese woman, black hair pulled back tightly into a low bun, sharp confident eyes, defined red lipstick, black tailored blazer over pale blouse, upright rigid posture, Japanese bank section chief, composed cold expression, plain light gray studio background, soft even lighting, front and three-quarter views, 9:16 vertical
```

### 主任（老員工 / 50代男性）

```
character reference sheet, photorealistic, 55-year-old Japanese man, thinning gray hair, tired kind eyes, plain gray dress shirt without jacket, slightly slouched, unremarkable presence, Japanese bank veteran clerk, quiet resigned expression, plain light gray studio background, soft even lighting, front and three-quarter views, 9:16 vertical
```

---

# STEP 1 · 场景底图（2 个场景，各生成 1 张空景）

空景用于锁定空间、家具与光线，后续所有镜头都在同一空间里发生。

### 会議室（主场景）

```
empty Japanese bank meeting room interior, photorealistic, long light-wood table, six gray fabric chairs, white walls, horizontal window blinds on the left casting soft side light stripes, beige carpet, ceiling fluorescent panel lights, no people, no text anywhere, no posters, clean minimal Japanese corporate interior, 9:16 vertical, eye-level camera
```

### 深夜オフィス（S06 回想用）

```
empty Japanese bank open-plan office at night, photorealistic, rows of desks with monitors turned off, all ceiling lights off, only one desk lamp glowing warm in the far corner, dark blue ambient darkness through windows, no people, no text anywhere, 9:16 vertical, eye-level camera
```

---

# STEP 2 · 11 镜关键帧（图生图，绑定角色参考图）

**每条 prompt 前都要挂上对应角色的参考图。**平台若支持多参考图，同时挂角色图 + 场景底图。

### S01 ｜ 0–3.5s ｜ 特写 ｜ 課長の口元と下げた頭

```
extreme close-up of a 52-year-old Japanese man's lower face and bowed head, only mouth and chin visible, head lowered in a formal apologetic bow, navy suit shoulder in frame, meeting room背景 blurred, side window light from the left, shallow depth of field, photorealistic, no text, 9:16 vertical
```
> 只要嘴和低头，**不要拍全脸**——避免与 S08 的一致性对比暴露差异。

### S02 ｜ 3.5–7s ｜ 大特写 ｜ 女主の目

```
extreme close-up of a 29-year-old Japanese woman's eyes, [女主参考图], black bob hair edge visible, eyes wide and unblinking, pupils slightly dilated, subtle fear held back, soft side window light from the left, blurred meeting room background, shallow depth of field, photorealistic, no makeup, no text, 9:16 vertical
```

### S03 ｜ 7–12s ｜ 近景 ｜ 女主、机上で指を組む

```
close-up of a 29-year-old Japanese woman seated at a meeting table, [女主参考图], navy cardigan over white blouse, hands folded on the table, upper chest and face in frame, calm suppressed expression, horizontal window blind light stripes on the wall behind, shallow depth of field, photorealistic, no text, 9:16 vertical
```

### S04 ｜ 12–18s ｜ 特写（手）｜ 係長の指が署名欄をなぞる

```
extreme close-up of a 38-year-old Japanese woman's hand with neat manicure, index finger slowly tracing along a line on a completely blank white document lying on a light-wood table, black blazer sleeve visible, soft overhead office light, shallow depth of field, photorealistic, blank paper with absolutely no writing or text, 9:16 vertical
```
> **纸必须完全空白**，署名栏后期贴。这是全剧最省也最重要的证据镜头。

### S05 ｜ 18–24s ｜ 近景 ｜ 女主の顔、恐怖から理解へ

```
close-up portrait of a 29-year-old Japanese woman, [女主参考图], face turning from shock to quiet realization, jaw slightly tightening, eyes steady, navy cardigan, meeting room blurred behind, side window light from the left, shallow depth of field, photorealistic, restrained expression, no text, 9:16 vertical
```

### S06 ｜ 24–31s ｜ 中景 ｜ 回想・深夜に一人でモニターに向かう

```
medium shot of a 29-year-old Japanese woman alone at a desk in a dark empty office at night, [女主参考图], seen slightly from behind and the side, facing a monitor with a completely black blank screen, blue rim light on her face and hair, all other lights off, rows of empty desks in darkness behind her, photorealistic, blank dark screen with no content, no text, 9:16 vertical
```
> 屏幕内容（代码、图表）**后期合成**，生成时必须是黑屏。

### S07 ｜ 31–38s ｜ 特写（手）｜ 湯呑みを置く手が止まる

```
extreme close-up of a 29-year-old Japanese woman's hand holding a plain ceramic teacup, hand frozen mid-motion just above the table surface, navy cardigan sleeve, light-wood table, soft side window light, shallow depth of field, photorealistic, no text, 9:16 vertical
```

### S08 ｜ 38–45s ｜ 特写 ｜ 課長の口元（S01と同構図）

```
extreme close-up of a 52-year-old Japanese man's lower face and mouth, same framing and lighting as before, head now lifted slightly, mouth beginning to open to speak, navy suit shoulder in frame, side window light from the left, shallow depth of field, photorealistic, no text, 9:16 vertical
```
> **直接复用 S01 的关键帧做图生图**，只改"抬头、张口"。同构图呼应是这一集的结构支点。

### S09 ｜ 45–50s ｜ 特写 ×3 ｜ 三连快切（各生成，绝不同框）

**S09a — 係長**
```
close-up portrait of a 38-year-old Japanese woman, [係長参考图], black hair in low bun, face frozen in shock, lips slightly parted, eyes fixed forward, black blazer, meeting room blurred behind, side window light, photorealistic, no text, 9:16 vertical
```

**S09b — 主任**
```
close-up portrait of a 55-year-old Japanese man, [主任参考图], gray dress shirt, slowly raising his eyes from the table, faint surprise, tired face, meeting room blurred behind, side window light, photorealistic, no text, 9:16 vertical
```

**S09c — 課長**
```
close-up portrait of a 52-year-old Japanese man, [課長参考图], thin glasses, confused expression as if surprised by his own words, mouth closed, brow faintly furrowed, navy suit, meeting room blurred behind, side window light, photorealistic, no text, 9:16 vertical
```

### S10 ｜ 50–55s ｜ 近景 ｜ 女主、かすかに笑う

```
close-up portrait of a 29-year-old Japanese woman, [女主参考图], the faintest upward curve at one corner of her mouth, eyes calm and cold, navy cardigan, meeting room blurred behind, side window light from the left, shallow depth of field, photorealistic, extremely subtle smile, not smiling openly, no text, 9:16 vertical
```
> `extremely subtle` 和 `not smiling openly` 两句都不能删。日本式的胜利不咧嘴。

### S11 ｜ 55–60s ｜ 特写（物）｜ スマホ画面

```
extreme close-up of a 29-year-old Japanese woman's hand holding a smartphone, thumb hovering just above the screen, screen completely black and blank, navy cardigan sleeve, light-wood table below, soft side window light, shallow depth of field, photorealistic, blank screen with no interface and no text, 9:16 vertical
```
> 来电界面全部后期贴字。

---

# STEP 3 · 图生视频（挂关键帧，只描述运动）

关键帧已经锁死画面，视频阶段**只写运动，不要重复描述外观**——重复描述会让模型重新"理解"人物，导致漂移。

| 镜号 | 时长 | 运动提示词 |
|---|---:|---|
| S01 | 4s | `the man's head stays bowed, almost motionless, only faint breathing, his mouth moves as he speaks quietly, static camera, no camera movement` |
| S02 | 4s | `the woman's eyes stay wide open, one very slow blink at the end, micro-movement only, extremely slow push in, no other motion` |
| S03 | 5s | `the woman sits still, fingers tighten slightly on her folded hands, subtle breathing, static camera` |
| S04 | 6s | `the finger slides slowly along the blank paper from left to right, everything else still, static camera` |
| S05 | 6s | `her expression shifts slowly from shock to cold understanding, jaw tightens, no head movement, static camera` |
| S06 | 7s | `her shoulders rise and fall once with a tired breath, faint flicker of screen light on her face, static camera` |
| S07 | 7s | `the hand holding the teacup stops mid-air and stays frozen, very slight tremble, static camera` |
| S08 | 7s | `the man slowly lifts his head and opens his mouth to speak, speaking motion, static camera` |
| S09a | 2s | `her face freezes, one tiny flinch, no other movement, static camera` |
| S09b | 2s | `he slowly raises his eyes, head barely moves, static camera` |
| S09c | 2s | `his brow furrows slightly, a slow confused blink, static camera` |
| S10 | 5s | `one corner of her mouth lifts very slightly, eyes unchanged, extremely slow push in` |
| S11 | 6s | `her thumb moves down and touches the screen, then her hand goes completely still, static camera` |

**统一参数**：9:16 竖屏 ／ 1080×1920 ／ 24 或 30 fps ／ 运镜强度调到最低档 ／ 关闭"自动创意增强"类选项（它会改脸）。

---

# STEP 4 · 台词与配音表（TTS）

**声音 ID 一旦选定写进角色卡，全剧不换。**每句先出配音、量出实际秒数，再按秒数生成画面（音频先行）。

| 镜号 | 说话人 | 日文台词 | 语体/情绪 | 处理 |
|---|---|---|---|---|
| S01 | 課長 | 次回の更新は、ございません。 | 最高丁寧＋事務的，**不带愧疚** | 正常 |
| S02 | 課長（心声） | これで係長の失点は消える。 | 平淡、无起伏 | **加轻混响、音量−3dB、环境音衰减30%、低频耳鸣渐入** |
| S03 | 女主（独白） | 今、この人が言わなかった言葉が聞こえた。 | 抑制、气声偏多 | 独白轨，比对白干净 |
| S04 | 係長（心声） | この報告書、名前さえ変えれば私の実績。 | 冷静、轻蔑 | 同心声处理 |
| S05 | 女主（独白） | あの報告書を書いたのは、私だ。 | 略微加重，仍克制 | 独白轨 |
| S06 | 女主（独白） | 三か月、毎晩ひとりで。 | 疲惫 | 独白轨 |
| S07 | 女主（独白） | そのとき、気づいた。——聞こえるだけじゃない。 | 转折，气息一顿 | 独白轨；★BGM 首次进入 |
| S08 | 課長 | ……いや、彼女の契約は、継続で。 | 困惑，像不受自己控制 | **前置 reverse swell 0.6s 改写音效** |
| S10 | 女主（独白） | 本音は、書き換えられる。 | 低、平、冷 | 独白轨 |
| S11 | 母 | もしもし、〇〇？ | 温和、日常 | **高频削除（去掉4kHz以上），听起来"隔了一层"** |
| S11 | 女主（独白） | ……この声、誰？ | 极轻，几乎气声 | 独白轨；说完立刻黑场 |

**角色声音参数**（写进角色卡，不再变）：

| 角色 | 第一人称 | 语速 | 音域 | 情绪幅度 |
|---|---|---|---|---|
| 女主 | 私（わたし） | 偏慢 | 中低 | 小（独白可略大） |
| 課長 | 私 | 中 | 中低 | 极小 |
| 係長 | 私 | 略快 | 中 | 小但锋利 |

---

# STEP 5 · 后期贴字清单（4 处，全部不是 AI 生成）

| 镜号 | 贴什么 | 做法 |
|---|---|---|
| S01 | 課長胸前社員証 | 做一张日文工牌图，跟踪贴合 |
| S04 | 文件署名栏（含被涂改的名字） | 做日文文件版式，透视贴合 |
| S06 | 监视器画面（代码＋图表） | 截真实 IDE 界面或自制 UI |
| S11 | 手机来电界面「母」 | 截真实 iOS/Android 来电界面重制 |

字体：Noto Sans JP（免费商用）。**S04 和 S11 是全剧的证据核心，值得多花时间做真。**

---

# 执行顺序检查表

- [ ] STEP 0 四个角色定妆完成，各选定 1 套参考图，登记进角色卡
- [ ] 30 张静态关键帧盲评通过（识别率≥95%、"换演员"镜头≤1）——**不过关不要进 STEP 3**
- [ ] STEP 4 配音先做完，量出每句实际秒数
- [ ] 按秒数剪 animatic，过节奏门
- [ ] STEP 2 关键帧 → STEP 3 图生视频
- [ ] 粗剪锁画面 → 最终配音 → S01/S08 做口型（**只这两个镜头**）
- [ ] 后期贴字 4 处 → 混音（心声处理在这一步）→ 日语母语终审
