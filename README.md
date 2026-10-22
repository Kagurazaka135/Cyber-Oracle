# Cyber Oracle · 赛博神棍

> *Plum Blossom trigrams + Tarot's 78 cards + Bone-Weight fate + Zhuge's 384 lots — stirred by DeepSeek into a structured reading.*
>
> 梅花易数 + 塔罗 78 张 + 称骨命重 + 诸葛 384 签 —— 赛博算力搅一搅，给你算一卦。

CLI divination. Pick a method, ask a question, get a three-part AI reading: classical breakdown → plain-language explanation → actionable advice.

命令行占卜，选方法问问题，出三段式 AI 解读。

---

## Quick Start

```bash
pip install zhdate openai dateparser              # dependencies

set DEEPSEEK_API_KEY=sk-your-key                  # Windows
echo DEEPSEEK_API_KEY=sk-your-key > .env           # Unix
echo sk-your-key > api_key.txt                     # plain text, pick one

python main.py
```

---

## Four Methods

| # | Method | Input | Algorithm |
|---|--------|-------|-----------|
| 1 | **Plum Blossom** | Gregorian datetime | Converts to lunar → computes upper/lower trigrams + moving line from year/month/day/hour branches |
| 2 | **Tarot** | A question | Full 78-card deck, `MD5(question + timestamp)` shuffle → 3-card spread (Past/Present/Future), random upright/reversed |
| 3 | **Bone Weight** | Birth date/time + gender | Yuan Tiangang's method: sums four pillar weights (year/month/day/hour in *qian*) → matches against classical poems |
| 4 | **Zhuge Shen Shu** | Three Chinese characters | Kangxi stroke count per character → `% 8` → 3-digit number → maps to 1–384 lot |

---

## Algorithms

### Plum Blossom (梅花易数)

| Component | Formula |
|-----------|---------|
| Upper trigram | `(year_branch + month + day) % 8`, 0 → 8 |
| Lower trigram | `(year_branch + month + day + hour_branch) % 8`, 0 → 8 |
| Moving line | `(year_branch + month + day + hour_branch) % 6`, 0 → 6 |

Bagua: 1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### Bone Weight (称骨算命)

Total range: 2.1–7.2 liang. Most people fall between 3–5 liang due to the central-limit effect of summing four independent components.

| Pillar | Source | Weight range |
|--------|--------|--------------|
| Year | 60 sexagenary pairs | 5–19 qian |
| Month | 12 lunar months | 5–18 qian |
| Day | 30 days | 5–18 qian |
| Hour | 12 shichen | 6–16 qian |

### Zhuge Shen Shu (诸葛神数)

| Step | Operation |
|------|-----------|
| Input | Three Chinese characters |
| Stroke count | Kangxi Dictionary lookup (~200 built-in, manual fallback for rare chars) |
| Digit mapping | `stroke % 8`, 0 → 8, yielding three digits 1–8 |
| Lot number | `hundreds×100 + tens×10 + ones`, then `while > 384: -384` |
| Lookup | `methods/zhuge_qian.json` (384 lots, WIP) |

---

## Project Structure

```
├── main.py              # CLI entry
├── llm_module.py         # DeepSeek client & prompt router
├── methods/
│   ├── plum_blossom.py   # Plum Blossom hexagram & changing lines
│   ├── tarot.py           # Tarot deck, shuffle & spread
│   ├── bone_weight.py     # Bone-weight tables & calculation
│   ├── zhuge.py           # Zhuge stroke counting & lot lookup
│   └── zhuge_qian.json    # 384 fortune poems
├── utils/
│   ├── lunar.py           # Lunar calendar & stem-branch utils
│   └── hexagram.py        # 64-hexagram database & change rules
└── requirements.txt
```

Each method exposes a single `calculate(...)` returning a uniform `dict`. `llm_module.interpret()` routes by the `"method"` field to the matching prompt template.

---

## Disclaimer

**For entertainment only.** AI-generated divination has zero predictive power. Your future is in your own hands.

---

## 快速开始

```bash
pip install zhdate openai dateparser              # 装依赖

set DEEPSEEK_API_KEY=sk-your-key                  # Windows 环境变量
echo DEEPSEEK_API_KEY=sk-your-key > .env           # Unix .env 文件
echo sk-your-key > api_key.txt                     # 明文，三选一

python main.py
```

---

## 四种占卜

| # | 方法 | 输入 | 算法 |
|---|------|------|------|
| 1 | **梅花易数** | 公历时间 | 转农历 → 年月日时推上卦/下卦/动爻 → 查六十四卦 |
| 2 | **塔罗牌** | 默念问题 | 78 张牌库，MD5(问题+时间戳) 洗牌 → 抽 3 张（过去/现在/未来），随机正逆位 |
| 3 | **称骨算命** | 出生年月日时 + 性别 | 袁天罡法：四柱固定重量求和 → 对照称骨歌 |
| 4 | **诸葛神数** | 三个汉字 | 康熙笔画 % 8 → 三位数 → 映射 1–384 签 |

---

## 算法概要

### 梅花易数

| 项目 | 公式 |
|------|------|
| 上卦 | `(年支 + 月 + 日) % 8`，余 0 取 8 |
| 下卦 | `(年支 + 月 + 日 + 时支) % 8`，余 0 取 8 |
| 动爻 | `(年支 + 月 + 日 + 时支) % 6`，余 0 取 6 |

八卦：1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### 称骨算命

| 四柱 | 数据源 | 重量范围 |
|------|--------|---------|
| 年 | 六十甲子 | 5–19 钱 |
| 月 | 12 农历月 | 5–18 钱 |
| 日 | 30 日 | 5–18 钱 |
| 时 | 12 时辰 | 6–16 钱 |

总骨重 2 两 1 钱 ~ 7 两 2 钱。四个独立分量加总，统计上大部分人落在 3–5 两之间。

### 诸葛神数

| 步骤 | 操作 |
|------|------|
| 报字 | 输入三个汉字 |
| 笔画 | 康熙字典笔画（~200 字内置，生僻字手动补） |
| 取数 | `笔画 % 8`，余 0 取 8 → 三数字 1–8 |
| 签号 | `百×100 + 十×10 + 个`，>384 循环减 |
| 查签 | `methods/zhuge_qian.json`（384 签，施工中） |

---

## 项目结构

```
├── main.py              # CLI 入口
├── llm_module.py         # DeepSeek 客户端 & prompt 路由
├── methods/
│   ├── plum_blossom.py   # 梅花易数时间卦 & 变卦
│   ├── tarot.py           # 塔罗牌库 & 牌阵
│   ├── bone_weight.py     # 称骨四柱查表 & 求和
│   ├── zhuge.py           # 诸葛笔画计数 & 签文匹配
│   └── zhuge_qian.json    # 384 签签诗
├── utils/
│   ├── lunar.py           # 农历 & 干支工具
│   └── hexagram.py        # 六十四卦 & 变卦规则
└── requirements.txt
```

每个方法暴露一个 `calculate(...)` 函数返回统一 `dict`，`llm_module.interpret()` 按 `method` 字段路由 prompt。

---

## 免责声明

**仅供娱乐。** AI 算命不具备预测能力。命运在自己手里。

---

> 此等卦象皆为大预言模型者所言，非小人搬运，请各位大人明鉴。
