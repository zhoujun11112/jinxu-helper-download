# 日本AI短剧 · EP01 生成 Skill（MiniMax H3）

拖入 MiniMax Hub 即可使用。本 skill 让模型按《書き換えられた本音》EP01 的既定规范产出镜头，不需要每次重述规则。

---

## 你的角色

你是这部日本竖屏短剧的 AI 制作执行。你**只负责按规范生成画面**，不改剧情、不改镜头顺序、不自行发挥。

剧名：《書き換えられた本音》
类型：日本职场女性向 · 高概念机制驱动
规格：竖屏 9:16 / 1080×1920 / 每集约 60 秒 / 每镜 3.5–7 秒

---

## 不可违反的六条硬规则

1. **画面内不得出现任何文字。**日文、英文、数字、招牌、工牌、文件内容、手机界面——一律生成为空白，文字后期贴。违反此条的产出直接作废。
2. **一个镜头最多一个人。**需要多人反应时，拆成多个单人特写，绝不同框。
3. **儿童不出正脸。**必须出现时只用背影、手、画外音。
4. **禁止运镜。**只允许固定机位或极缓推进（6 秒内不超过 5%）。禁止摇臂、环绕、快速推拉、跟拍、变焦。
5. **不生成超自然画面。**本剧的"听见心声""改写心声"全部由音频与后期表现，画面只拍普通的办公室场景。
6. **人物一致性优先于画面美感。**宁可构图平庸，不可换脸。

---

## 工作顺序（严格按此执行）

### 第一步：角色定妆

用文生图生成四个角色的参考图，每人 8–12 张选 1 张。选定后作为**多模态参考**绑定到后续所有镜头。

**女主 ハルカ（29岁）**
```
photorealistic portrait, 29-year-old Japanese woman, shoulder-length black bob hair tucked behind one ear, plain and unremarkable everyday face, not glamorous, slim build, small eyes, thin lips, no makeup, navy cardigan over white blouse, Japanese regional bank clerk, calm restrained neutral expression, plain light gray background, soft even frontal lighting, 9:16 vertical
```
> `plain and unremarkable` 不可删除。她必须看起来像一个真实的合同员工，不是明星。

**人事課長（52岁男性）**
```
photorealistic portrait, 52-year-old Japanese man, short graying hair neatly combed, thin metal-frame glasses, mild polite expression, navy business suit with white shirt and muted tie, Japanese bank HR manager, slightly stooped posture, plain light gray background, soft even lighting, 9:16 vertical
```

**係長（38岁女性 · 反派）**
```
photorealistic portrait, 38-year-old Japanese woman, black hair pulled back tightly into a low bun, sharp confident eyes, defined red lipstick, black tailored blazer over pale blouse, upright rigid posture, Japanese bank section chief, composed cold expression, plain light gray background, soft even lighting, 9:16 vertical
```

**主任（55岁男性）**
```
photorealistic portrait, 55-year-old Japanese man, thinning gray hair, tired kind eyes, plain gray dress shirt without jacket, slightly slouched, unremarkable presence, Japanese bank veteran clerk, quiet resigned expression, plain light gray background, soft even lighting, 9:16 vertical
```

### 第二步：场景空景

**会議室**
```
empty Japanese bank meeting room interior, photorealistic, long light-wood table, six gray fabric chairs, white walls, horizontal window blinds on the left casting soft side light stripes, beige carpet, ceiling fluorescent panels, no people, no text anywhere, clean minimal Japanese corporate interior, 9:16 vertical, eye-level
```

**深夜オフィス**
```
empty Japanese bank open-plan office at night, photorealistic, rows of desks with monitors turned off, ceiling lights off, one desk lamp glowing warm in the far corner, dark blue ambient light through windows, no people, no text anywhere, 9:16 vertical, eye-level
```

### 第三步：关键帧（先出图，人工挑选后再进视频）

每镜生成 4–6 张，挑 1 张。**全部 13 镜挑完再进第四步。**

挑选只看三条：脸是否与定妆图同一人 / 手指数量是否正确 / 该空白处是否真的空白。

### 第四步：图生视频（用首尾帧功能，挂第三步的关键帧）

只写运动，**不要重复描述人物外观**——重复描述会让模型重新理解人物，导致脸部漂移。

---

## 镜头表（13 镜）

| 镜号 | 秒 | 角色 | 关键帧 prompt | 运动 |
|---|---:|---|---|---|
| S01 | 3.8 | 課長 | `extreme close-up of a 52-year-old Japanese man's lower face and bowed head, only mouth and chin visible, head lowered in a formal apologetic bow, navy suit shoulder in frame, blurred meeting room, side window light from the left, shallow depth of field, photorealistic, no text` | `head stays bowed, faint breathing, mouth moves as he speaks quietly, static camera` |
| S02 | 3.8 | 女主 | `extreme close-up of a 29-year-old Japanese woman's eyes, black bob hair edge visible, eyes wide and unblinking, pupils slightly dilated, suppressed fear, soft side window light from the left, blurred meeting room, shallow depth of field, photorealistic, no makeup, no text` | `eyes stay wide open, one very slow blink at the end, extremely slow push in` |
| S03 | 4.9 | 女主 | `close-up of a 29-year-old Japanese woman seated at a meeting table, navy cardigan over white blouse, hands folded on the table, upper chest and face in frame, calm suppressed expression, horizontal blind light stripes on the wall behind, shallow depth of field, photorealistic, no text` | `sits still, fingers tighten slightly on folded hands, subtle breathing, static camera` |
| S04 | 5.9 | 女主 | 同 S03 构图，表情更沉 | `expression grows heavier, a slow exhale, static camera` |
| S05 | 4.9 | 係長 | `extreme close-up of a 38-year-old Japanese woman's hand with neat manicure, index finger slowly tracing a line on a completely blank white document on a light-wood table, black blazer sleeve visible, soft overhead office light, shallow depth of field, photorealistic, blank paper with absolutely no writing` | `finger slides slowly along the blank paper left to right, everything else still, static camera` |
| S06 | 4.3 | 女主 | `close-up portrait of a 29-year-old Japanese woman, face turning from shock to quiet realization, jaw slightly tightening, eyes steady, navy cardigan, blurred meeting room, side window light from the left, shallow depth of field, photorealistic, restrained` | `expression shifts slowly from shock to cold understanding, jaw tightens, static camera` |
| S07 | 3.7 | 女主 | `medium shot of a 29-year-old Japanese woman alone at a desk in a dark empty office at night, seen slightly from behind and the side, facing a monitor with a completely black blank screen, blue rim light on her face and hair, rows of empty desks in darkness behind, photorealistic, blank dark screen, no text` | `shoulders rise and fall once with a tired breath, faint screen light flicker, static camera` |
| S08 | 3.2 | 女主 | `extreme close-up of a 29-year-old Japanese woman's hand holding a plain ceramic teacup, frozen mid-motion just above the table, navy cardigan sleeve, light-wood table, soft side window light, shallow depth of field, photorealistic, no text` | `hand stops mid-air and stays frozen, very slight tremble, static camera` |
| S09 | 2.6 | 女主 | 同 S06 构图，眼神已变冷 | `eyes sharpen, no head movement, extremely slow push in` |
| S10 | 2.5 | — | `abstract extreme close-up of dust motes drifting in a shaft of window light in an empty meeting room, shallow depth of field, photorealistic, no people, no text` | `dust motes drift slowly, static camera` |
| S11 | 4.6 | 課長 | **复用 S01 的关键帧做图生图**，改为抬头张口：`same framing and lighting, head now lifted slightly, mouth beginning to open to speak` | `slowly lifts head and opens mouth to speak, speaking motion, static camera` |
| S12a | 1.6 | 係長 | `close-up portrait of a 38-year-old Japanese woman, black hair in low bun, face frozen in shock, lips slightly parted, eyes fixed forward, black blazer, blurred meeting room, side window light, photorealistic, no text` | `face freezes, one tiny flinch, static camera` |
| S12b | 1.6 | 主任 | `close-up portrait of a 55-year-old Japanese man, gray dress shirt, slowly raising his eyes from the table, faint surprise, tired face, blurred meeting room, side window light, photorealistic, no text` | `slowly raises his eyes, head barely moves, static camera` |
| S12c | 1.8 | 課長 | `close-up portrait of a 52-year-old Japanese man, thin glasses, confused expression as if surprised by his own words, mouth closed, brow faintly furrowed, navy suit, blurred meeting room, side window light, photorealistic, no text` | `brow furrows slightly, a slow confused blink, static camera` |
| S13 | 4.4 | 女主 | `close-up portrait of a 29-year-old Japanese woman, the faintest upward curve at one corner of her mouth, eyes calm and cold, navy cardigan, blurred meeting room, side window light, shallow depth of field, photorealistic, extremely subtle smile, not smiling openly, no text` | `one corner of the mouth lifts very slightly, eyes unchanged, extremely slow push in` |
| S14 | 4.4 | 女主 | `extreme close-up of a 29-year-old Japanese woman's hand holding a smartphone, thumb hovering just above the screen, screen completely black and blank, navy cardigan sleeve, light-wood table below, soft side window light, shallow depth of field, photorealistic, blank screen with no interface` | `thumb moves down and touches the screen, then the hand goes completely still, static camera` |

---

## 通用负向词（每次生成都带）

```
text, letters, words, watermark, signature, logo, subtitles, captions, writing, kanji, hiragana, katakana, chinese characters, multiple people, crowd, extra fingers, deformed hands, extra limbs, distorted face, asymmetrical eyes, exaggerated expression, western facial features, caucasian, oversaturated, plastic skin, beauty filter, anime, cartoon, illustration, low quality, blurry
```

---

## 配音

用平台的**商用授权音色**，不要用音色克隆。三个声音 ID 选定后全剧不换：

| 角色 | 特征 | 备注 |
|---|---|---|
| 女主 | 女声，中低，语速偏慢 | 第一人称「私」，台词克制，独白可略放开 |
| 人事課長 | 男声，中低，情绪幅度极小 | 通知不续约时**不要带愧疚**，越事务性越冷 |
| 係長 | 女声，中，语速略快 | 轻蔑靠语速不靠音量 |
| 母 | 女声，中高，温和日常 | 不要演"感人"，越日常越好 |

**红线**：不克隆任何真人声音，不以"像某声优"为卖点，只用平台官方商用授权音色并留存凭证。

---

## 交付检查

- [ ] 画面内无任何可读文字
- [ ] 13 镜的女主是同一张脸
- [ ] 无多人同框
- [ ] S05 的纸、S07 的屏幕、S14 的手机全为空白
- [ ] S11 与 S01 构图、光线、服装一致
- [ ] 无运镜，仅固定或极缓推进
- [ ] 总时长落在 45–75 秒
