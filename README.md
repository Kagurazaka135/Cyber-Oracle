# Cyber Oracle (赛博神棍)

> *Plum Blossom trigrams + Tarot's 78 cards + Bone-Weight fate + Zhuge's 384 lots — stirred by a DeepSeek LLM.*
>
> *梅花易数起卦 + 塔罗78张牌 + 称骨命重 + 诸葛384签 — 赛博算力搅一搅，给你算一卦。*

A CLI divination tool. Pick a method, feed it your question, get a structured AI reading back.

---

## Methods

| # | Method | What you do | How it works |
|---|--------|-------------|---------------|
| 1 | **Plum Blossom Yi Jing** | Enter a date/time | Converts to Chinese lunar calendar, computes upper/lower trigrams via time-based formula, finds original & changed hexagram, reads the moving line |
| 2 | **Tarot** | Ask a question | Seeds a 78-card deck shuffle with your question+timestamp, draws 3 cards (past/present/future) with random upright/reversed orientation |
| 3 | **Bone-Weight Fortune** | Enter birth date + time + gender | Yuan Tiangang's method: sums the fixed weights (in *qian*) of the four pillars (year/month/day/hour) into a total bone weight, matched against classical poems |
| 4 | **Zhuge Shen Shu** | Think of a question, then type three Chinese characters | Counts Kangxi Dictionary strokes per character, maps each `% 8` (0→8) to form a 3-digit number, reduces to 1–384, looks up the corresponding fortune lot |

All four route into **DeepSeek** for a structured reading: classical breakdown → plain-language explanation → actionable advice.

---

## Quick Start

```bash
# 1. Install dependencies
pip install zhdate openai dateparser

# 2. Configure API key (pick one)
set DEEPSEEK_API_KEY=sk-your-key              # Windows env
echo DEEPSEEK_API_KEY=sk-your-key > .env       # Unix env file
echo sk-your-key > api_key.txt                 # plain text

# 3. Run
python main.py
```

---

## Algorithms

### Plum Blossom (梅花易数)

| Component | Formula |
|-----------|---------|
| Upper trigram | `(year_branch + month + day) % 8`, 0 → 8 |
| Lower trigram | `(year_branch + month + day + hour_branch) % 8`, 0 → 8 |
| Moving line | `(year_branch + month + day + hour_branch) % 6`, 0 → 6 |

Bagua: 1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### Tarot (塔罗牌)

- Full 78-card deck: 22 Major Arcana + 56 Minor Arcana (4 suits × 14 cards)
- Deterministic shuffle: `MD5(question + timestamp)` as random seed
- 3-card spread (Past / Present / Future) by default

### Bone-Weight (称骨算命)

| Pillar | Data | Weight range |
|--------|------|--------------|
| Year (年) | 60 sexagenary pairs | 5–19 qian |
| Month (月) | 12 lunar months | 5–18 qian |
| Day (日) | 30 days | 5–18 qian |
| Hour (时) | 12 shichen | 6–16 qian |

Total bone weight range: 2.1–7.2 liang (1 liang = 10 qian). Most people land between 3–5 liang because of the central-limit effect of summing four independent components.

### Zhuge Shen Shu (诸葛神数)

| Step | Operation |
|------|-----------|
| 1. Input | User types 3 Chinese characters |
| 2. Stroke count | Look up Kangxi Dictionary strokes per character (built-in dict ~200 chars; missing chars trigger manual input fallback) |
| 3. Digit mapping | `stroke % 8`, remainder 0 → 8, giving 3 digits each 1–8 |
| 4. Lot number | `hundreds×100 + tens×10 + ones`, then `while > 384: -384` |
| 5. Lookup | Match lot number against `methods/zhuge_qian.json` (384 lots total; currently 10 seeded) |
| 6. Fallback | If lot number not in JSON, a default placeholder lot is used |

---

## Project Structure

```
├── main.py                  # CLI entry point
├── llm_module.py            # DeepSeek API client & interpretation router
├── cyber_oracle.py          # Standalone single-file version (Plum Blossom only)
├── methods/
│   ├── plum_blossom.py      # Plum Blossom hexagram calculation
│   ├── tarot.py             # 78-card deck, shuffle & spread logic
│   ├── bone_weight.py       # Bone-weight fortune tables & calculation
│   ├── zhuge.py             # Zhuge Shen Shu: stroke counting & lot lookup
│   └── zhuge_qian.json      # 384-lot fortune poems (WIP)
├── utils/
│   ├── lunar.py             # Chinese lunar calendar & stem-branch utilities
│   └── hexagram.py          # 64-hexagram database & change rules
└── 问卦/                    # Reading history archive
```

---

## Architecture notes

Each method exposes a single `calculate(...)` function returning a uniform `dict`:

```python
{"method": "...", ...}
```

`main.py` displays the result via a `_display_*()` function, then passes the dict to `llm_module.interpret()`, which routes by the `"method"` field to the matching prompt template.

---

## Disclaimer

**For entertainment purposes only.** AI-generated divination readings carry zero predictive power. Your future is in your own hands.

---

## Tech Stack

Python 3 + zhdate + openai + dateparser + DeepSeek API

---

---

# 赛博神棍 · Cyber Oracle

> **梅花易数起卦 + 塔罗 78 张牌 + 称骨命重 + 诸葛 384 签 — 赛博算力搅一搅，给你算一卦。**

命令行占卜工具。选一个方法，喂一个问题，吐出三段式 AI 解读。

---

## 四种占卜方法

| # | 方法 | 你做什么 | 背后怎么算 |
|---|------|---------|-----------|
| 1 | **梅花易数** | 输入公历时间 | 自动转农历，用年月日时推上卦/下卦/动爻，查六十四卦 |
| 2 | **塔罗牌** | 默念问题回车 | 用问题+时间戳当种子洗牌，抽 3 张（过去/现在/未来），随机正逆位 |
| 3 | **称骨算命** | 输入出生年月日时 + 性别 | 袁天罡法：四柱各有一个固定重量（钱），求和得总骨重，对照称骨歌 |
| 4 | **诸葛神数** | 心里想问题，输入三个汉字 | 每个字查康熙笔画数，各自 %8 余 0 取 8，组成三位数，映射到 1-384 签 |

四种方法最终都进 **DeepSeek** 做结构化解读：术语详解 → 人话版 → 行动建议。

---

## 快速开始

```bash
# 1. 装依赖
pip install zhdate openai dateparser

# 2. 配 API Key（三选一）
set DEEPSEEK_API_KEY=sk-your-key              # Windows 环境变量
echo DEEPSEEK_API_KEY=sk-your-key > .env       # Unix .env 文件
echo sk-your-key > api_key.txt                 # 明文

# 3. 开算
python main.py
```

---

## 算法说明

### 梅花易数

| 项目 | 公式 |
|------|------|
| 上卦 | `(年支 + 月 + 日) % 8`，余 0 取 8 |
| 下卦 | `(年支 + 月 + 日 + 时支) % 8`，余 0 取 8 |
| 动爻 | `(年支 + 月 + 日 + 时支) % 6`，余 0 取 6 |

八卦：1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### 塔罗牌

- 完整 78 张：大阿卡纳 22 张 + 小阿卡纳 56 张（4 花色 × 14 张）
- 确定性洗牌：`MD5(问题 + 时间戳)` 作为随机种子，同问题同结果
- 默认三张牌阵：过去 / 现在 / 未来

### 称骨算命

| 四柱 | 数据 | 重量范围 |
|------|------|---------|
| 年柱 | 六十甲子 | 5~19 钱 |
| 月柱 | 12 个月 | 5~18 钱 |
| 日柱 | 30 天 | 5~18 钱 |
| 时柱 | 12 时辰 | 6~16 钱 |

总骨重 2 两 1 钱 ~ 7 两 2 钱。四个独立分量加总，统计上大部分人自然落在 3 两到 5 两之间。

### 诸葛神数

| 步骤 | 操作 |
|------|------|
| 1. 报字 | 用户输入三个汉字（如「找工作」） |
| 2. 数笔画 | 按康熙字典查每个字的笔画数（内置约 200 常用字；生僻字弹出手动输入） |
| 3. 取数 | `笔画 % 8`，余 0 取 8，得 1-8 的三个数字 |
| 4. 算签号 | `百位×100 + 十位×10 + 个位`，大于 384 则循环减 384 |
| 5. 查签 | 签号匹配 `methods/zhuge_qian.json`（共 384 签，目前录入 10 签） |
| 6. 兜底 | 查不到的签号返回占位签「三字通天地，一签问古今」 |

---

## 项目结构

```
├── main.py                  # CLI 入口
├── llm_module.py            # DeepSeek 客户端 & 解读路由
├── cyber_oracle.py          # 单文件独立版（仅梅花易数）
├── methods/
│   ├── plum_blossom.py      # 梅花易数时间卦计算
│   ├── tarot.py             # 塔罗牌库 & 洗牌抽牌逻辑
│   ├── bone_weight.py       # 称骨算命四柱重量表 & 计算
│   ├── zhuge.py             # 诸葛神数笔画计数 & 签文查表
│   └── zhuge_qian.json      # 384 签签诗数据库（施工中）
├── utils/
│   ├── lunar.py             # 农历转换 & 干支
│   └── hexagram.py          # 六十四卦数据库 & 变卦规则
└── 问卦/                    # 历史占卜记录归档
```

---

## 架构说明

每个方法对外暴露一个 `calculate(...)` 函数，返回统一格式的 dict：

```python
{"method": "...", ...}
```

`main.py` 通过 `_display_*()` 展示结果，然后把 dict 塞给 `llm_module.interpret()`，后者根据 `"method"` 字段路由到对应的 prompt 模板。

---

## 免责声明

**仅供娱乐。** AI 生成的占卜解读不具备预测能力。命运在自己手里。

---

## 技术栈

Python 3 + zhdate + openai + dateparser + DeepSeek API
