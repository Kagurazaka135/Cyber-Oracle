# Cyber-Oracle (赛博神棍)

A CLI divination program that combines ancient fortune-telling traditions with modern AI interpretation powered by DeepSeek LLM.

---

## Features

- **Plum Blossom Yi Jing (梅花易数)** — Enter a Gregorian date/time, automatically convert to Chinese lunar calendar, compute hexagrams (original → changed → moving line), and get an AI interpretation.
- **Tarot Reading (塔罗牌)** — Full 78-card Tarot deck (22 Major Arcana + 56 Minor Arcana) with deterministic seeded shuffling. Supports the classic three-card spread (Past, Present, Future).
- **AI-Powered Interpretation** — Each divination result is sent to DeepSeek for a structured three-part reading: classical/esoteric explanation, plain-language rephrasing, and practical advice.
- **Deterministic Shuffle** — Tarot draws are reproducible based on the MD5 hash of your question and timestamp.
- **No Persistence, No Tracking** — Pure CLI, no data stored. Your questions go directly to the LLM API.

---

## Installation

### Prerequisites

- Python 3.10+
- A [DeepSeek](https://platform.deepseek.com/) API key

### Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd Cyber-Oracle

# 2. Install dependencies
pip install openai zhdate dateparser

# 3. Configure your API key (choose one)
export DEEPSEEK_API_KEY="sk-xxx"          # environment variable
echo "DEEPSEEK_API_KEY=sk-xxx" > .env      # .env file
echo "sk-xxx" > api_key.txt                # plain text file
```

### Usage

```bash
python main.py
```

Follow the interactive menu:

1. **Plum Blossom Yi Jing** — Enter a date/time, get hexagram readings, then optionally ask a question for AI interpretation.
2. **Tarot Reading** — Think of a question, draw cards, receive an AI-powered reading.

---

## Divination Methods

### Plum Blossom Yi Jing (梅花易数时间卦法)

Based on Shao Yong's Plum Blossom Yi Jing system. The algorithm:

| Component | Formula |
|-----------|---------|
| Upper trigram (上卦) | `(year_branch + month + day) % 8` (0 → 8) |
| Lower trigram (下卦) | `(year_branch + month + day + hour_branch) % 8` (0 → 8) |
| Moving line (动爻) | `(year_branch + month + day + hour_branch) % 6` (0 → 6) |

Bagua mapping: 1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

The pair of trigrams forms one of the 64 hexagrams of the I Ching. The moving line determines the changed hexagram.

### Tarot

A complete 78-card Tarot deck:
- **22 Major Arcana** — From The Fool (0) to The World (XXI)
- **56 Minor Arcana** — 4 suits (Wands, Cups, Swords, Pentacles) × 14 cards each (Ace through 10, Page, Knight, Queen, King)

Each card has predefined upright/reversed meanings with element and astrological associations. The shuffle is seeded deterministically so the same question + timestamp always produces the same draw.

### AI Reading Structure

Every AI interpretation follows a consistent three-section format:

1. **Classical interpretation** — Using traditional terminology and symbolism
2. **Plain-language version** — Colloquial, easy-to-understand rephrasing
3. **Practical advice** — Actionable guidance based on the reading

---

## Project Structure

```
Cyber-Oracle/
├── main.py                 # CLI entry point & orchestrator
├── llm_module.py           # DeepSeek API integration & key management
├── methods/
│   ├── __init__.py
│   ├── plum_blossom.py     # Plum Blossom hexagram calculation
│   └── tarot.py            # Tarot deck, shuffle & spread logic
├── utils/
│   ├── lunar.py            # Chinese lunar calendar utilities
│   └── hexagram.py         # 64-hexagram lookup & change rules
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| [openai](https://pypi.org/project/openai/) | OpenAI-compatible client for DeepSeek API |
| [zhdate](https://pypi.org/project/zhdate/) | Gregorian ↔ Chinese lunar calendar conversion |
| [dateparser](https://pypi.org/project/dateparser/) | Natural language date/time parsing |

---

## Notes

- API requests are sent to `https://api.deepseek.com` using the `deepseek-v4-flash` model by default.
- Three API key configuration methods are supported: environment variable, `.env` file, or `api_key.txt`.
- The Tarot module includes additional spread definitions (single-card "Today's Guidance" and Celtic Cross) in the code that are not currently exposed in the CLI menu.

---

## Disclaimer

**For entertainment purposes only.** AI-generated divination readings should not be used as a basis for real-world decisions. The future is in your own hands.

---

## Tech Stack

Python 3 + zhdate + openai + dateparser + DeepSeek API

---

---

# 赛博神棍 — Cyber-Oracle

> **《周易》的智慧 + 赛博的算力 + 塔罗的神秘，给你算一卦。**

一个命令行占卜程序，支持**梅花易数时间卦法**和**塔罗牌占卜**两种方式，调用 DeepSeek LLM 进行 AI 解读。

---

## 功能特点

- **梅花易数** — 输入公历时间，自动转农历计算时间卦（本卦→变卦→动爻）
- **塔罗牌** — 完整 78 张牌组（大阿卡纳 + 小阿卡纳），基于时间和问题生成稳定牌面
- **AI 解读** — DeepSeek 三段式解读：古典详解 / 大白话重述 / 实操建议
- **确定性洗牌** — 相同问题 + 时间戳始终得到相同抽牌结果
- **纯命令行，不留存** — 无数据库，无追踪

---

## 快速开始

### 前置条件

- Python 3.10+
- [DeepSeek](https://platform.deepseek.com/) API 密钥

### 安装

```bash
# 1. 克隆仓库
git clone <repo-url>
cd Cyber-Oracle

# 2. 安装依赖
pip install openai zhdate dateparser

# 3. 配置 API 密钥（三选一）
set DEEPSEEK_API_KEY=sk-your-key          # 环境变量
echo DEEPSEEK_API_KEY=sk-your-key > .env   # .env 文件
echo sk-your-key > api_key.txt             # 纯文本文件
```

### 运行

```bash
python main.py
```

根据菜单选择占卜方式：

1. **梅花易数** — 输入日期时间，获取卦象，可选择提问获取 AI 解读
2. **塔罗占卜** — 心中默念问题，抽牌，获取 AI 解读

---

## 占卜方式说明

### 梅花易数时间卦法

基于邵雍梅花易数体系：

| 项目 | 计算 |
|------|------|
| 上卦 | `(年地支序数 + 月数 + 日数) % 8`，余 0 取 8 |
| 下卦 | `(年地支序数 + 月数 + 日数 + 时地支序数) % 8`，余 0 取 8 |
| 动爻 | `(年地支序数 + 月数 + 日数 + 时地支序数) % 6`，余 0 取 6 |

八卦：1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

上下卦组成六十四卦之一，动爻决定变卦。

### 塔罗牌

完整 78 张塔罗牌库：
- **22 张大阿卡纳** — 从愚人（0）到世界（XXI）
- **56 张小阿卡纳** — 4 个牌组（权杖、圣杯、宝剑、星币）× 每牌组 14 张

每张牌预定义了正位/逆位含义以及元素和星座关联。洗牌基于确定性种子，相同输入始终产生相同抽牌。

### AI 解读结构

每次 AI 解读分为三段：

1. **古典解读** — 使用传统术语和象征体系
2. **大白话版本** — 通俗易懂的重述
3. **实操建议** — 基于卦象/牌面的 actionable 建议

---

## 项目结构

```
赛博神棍/
├── main.py                 # CLI 入口 & 流程编排
├── llm_module.py           # DeepSeek API 集成 & 密钥管理
├── methods/
│   ├── __init__.py
│   ├── plum_blossom.py     # 梅花易数卦象计算
│   └── tarot.py            # 塔罗牌库、洗牌 & 牌阵逻辑
├── utils/
│   ├── lunar.py            # 农历转换工具
│   └── hexagram.py         # 六十四卦查询 & 变卦规则
└── README.md
```

---

## 依赖

| 包 | 用途 |
|---------|-------|
| [openai](https://pypi.org/project/openai/) | OpenAI 兼容客户端，调用 DeepSeek API |
| [zhdate](https://pypi.org/project/zhdate/) | 公历 ↔ 农历日期转换 |
| [dateparser](https://pypi.org/project/dateparser/) | 自然语言日期/时间解析 |

---

## 注意事项

- API 请求默认发送至 `https://api.deepseek.com`，模型为 `deepseek-v4-flash`
- 支持三种 API Key 配置方式：环境变量、`.env` 文件、`api_key.txt`
- 塔罗模块代码中额外定义了单牌"今日指引"和凯尔特十字牌阵，目前未在 CLI 菜单中暴露

---

## 免责声明

**仅供娱乐参考。** AI 生成的占卜解读不可作为实际决策依据。命运在自己手中。

---

## 技术栈

Python 3 + zhdate + openai + dateparser + DeepSeek API
