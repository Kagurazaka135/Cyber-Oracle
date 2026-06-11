# 🔮 赛博神棍 · Cyber-Oracle

> *I Ching wisdom + Tarot mystery + Bone‑Weight fate + Cyber computation.*
>
> *《周易》的智慧 + 塔罗的神秘 + 称骨的命理 + 赛博的算力，给你算一卦。*

A CLI divination tool powered by DeepSeek LLM. Three methods, one prompt.

---

## Divination Methods

| Method | Description |
|--------|-------------|
| **Plum Blossom Yi Jing** | Time-based hexagram calculation (original → changed → moving line) from the 64-hexagram I Ching system |
| **Tarot** | Full 78-card deck (22 Major + 56 Minor Arcana) with deterministic seeded shuffling |
| **Bone‑Weight Fortune** | Yuan Tiangang's traditional method — derive a "bone weight" from the four pillars of birth, mapped to classical poems |

All three methods feed into a structured **DeepSeek AI reading**: classical breakdown → plain-language explanation → actionable advice.

---

## Quick Start

```bash
# Install dependencies
pip install zhdate openai dateparser

# Configure API key (pick one)
export DEEPSEEK_API_KEY=sk-your-key          # env var
echo "DEEPSEEK_API_KEY=sk-your-key" > .env    # .env file
echo "sk-your-key" > api_key.txt              # plain text

# Run
python main.py
```

---

## Algorithms

### Plum Blossom

| Component | Formula |
|-----------|---------|
| Upper trigram | `(year_branch + month + day) % 8` (0 → 8) |
| Lower trigram | `(year_branch + month + day + hour_branch) % 8` (0 → 8) |
| Moving line | `(year_branch + month + day + hour_branch) % 6` (0 → 6) |

Bagua: 1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### Bone‑Weight

Each birth pillar carries a fixed weight in *qian* (1 liang = 10 qian). The sum yields a total bone weight (2.1–7.2 liang), matched against classical fortune poems.

| Pillar | Source |
|--------|--------|
| Year | 60 stem-branch pairs (5–19 qian) |
| Month | 12 lunar months (5–18 qian) |
| Day | 30 days (5–18 qian) |
| Hour | 12 shichen (6–16 qian) |

Most people naturally fall between 3–5 liang due to the central limit effect of summing four independent weights.

---

## Project Structure

```
├── main.py                  # CLI entry point
├── llm_module.py            # DeepSeek API integration & interpretation router
├── cyber_oracle.py          # Standalone single-file version (Plum Blossom only)
├── methods/
│   ├── plum_blossom.py      # Plum Blossom hexagram calculation
│   ├── tarot.py             # 78-card Tarot deck, shuffle & spread logic
│   └── bone_weight.py       # Yuan Tiangang bone-weight fortune
├── utils/
│   ├── lunar.py             # Chinese lunar calendar & stem-branch utilities
│   └── hexagram.py          # 64-hexagram lookup & change rules
└── 问卦/                    # Reading history
```

---

## Disclaimer

**For entertainment purposes only.** AI-generated divination readings should not be used as a basis for real-world decisions. The future is in your own hands.

---

## Tech Stack

Python 3 + zhdate + openai + dateparser + DeepSeek API

---

---

# 🔮 赛博神棍

> **《周易》的智慧 + 塔罗的神秘 + 称骨的命理 + 赛博的算力，给你算一卦。**

一个命令行占卜程序，支持**梅花易数时间卦法**、**塔罗牌占卜**、**称骨算命**三种方式，调用 DeepSeek LLM 进行 AI 解读。

---

## 占卜方法

| 方法 | 说明 |
|------|------|
| **梅花易数** | 输入公历时间，自动转农历计算时间卦（本卦→变卦→动爻），六十四卦体系 |
| **塔罗牌** | 完整 78 张牌组（22 张大阿卡纳 + 56 张小阿卡纳），基于问题 + 时间戳确定性洗牌 |
| **称骨算命** | 袁天罡称骨法，按生辰八字四柱重量推算总骨重，匹配称骨歌批语 |

三种方法均接入 **DeepSeek AI 三段式解读**：卦象/牌面/骨重详解 → 白话解读 → 切实建议。

---

## 快速开始

```bash
# 安装依赖
pip install zhdate openai dateparser

# 配置 API Key（三选一）
set DEEPSEEK_API_KEY=sk-your-key
echo DEEPSEEK_API_KEY=sk-your-key > .env
echo sk-your-key > api_key.txt

# 开算
python main.py
```

---

## 算法说明

### 梅花易数

| 项目 | 计算 |
|------|------|
| 上卦 | (年地支序数 + 月数 + 日数) % 8，余 0 取 8 |
| 下卦 | (年地支序数 + 月数 + 日数 + 时地支序数) % 8，余 0 取 8 |
| 动爻 | (年地支序数 + 月数 + 日数 + 时地支序数) % 6，余 0 取 6 |

八卦：1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

### 称骨算命

四柱各有固定重量（单位：钱，1两=10钱），求和得总骨重，对照《袁天罡称骨歌》取批语：

| 四柱 | 数据量 |
|------|--------|
| 年柱 | 60 甲子各不同（5~19钱） |
| 月柱 | 12 个月（5~18钱） |
| 日柱 | 30 天（5~18钱） |
| 时柱 | 12 时辰（6~16钱） |

总骨重范围 2两1钱 ~ 7两2钱。四个独立分量的加总使得大部分人的骨重自然落在 3两到 5两之间。

---

## 项目结构

```
├── main.py                  # CLI 入口
├── llm_module.py            # DeepSeek API 集成 & 解读路由
├── cyber_oracle.py          # 单文件独立版本（仅梅花易数）
├── methods/
│   ├── plum_blossom.py      # 梅花易数时间卦法
│   ├── tarot.py             # 塔罗牌库、洗牌 & 牌阵逻辑
│   └── bone_weight.py       # 称骨算命（袁天罡称骨法）
├── utils/
│   ├── lunar.py             # 农历转换 + 干支计算
│   └── hexagram.py          # 六十四卦查询 & 变卦规则
└── 问卦/                    # 历史占卜记录
```

---

## 免责声明

**仅供娱乐参考。** AI 生成的占卜解读不可作为实际决策依据。命运在自己手中。

---

## 技术栈

Python 3 + zhdate + openai + dateparser + DeepSeek API
