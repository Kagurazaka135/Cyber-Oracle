# Cyber-Oracle
**I Ching divination powered by Plum Blossom Numerology + DeepSeek LLM**  A CLI fortune-telling program that computes the I Ching hexagram based on the time-event method of Plum Blossom Yi Numerology (梅花易数), and calls DeepSeek LLM for interpretation.
# 🔮 Cyber Oracle (赛博神棍)

## Features

- Converts Gregorian date to Chinese lunar calendar and calculates the time hexagram
- Authentic Plum Blossom algorithm
- Full 64-hexagram mapping with changed-hexagram computation
- Three-part LLM interpretation (Classical / Plain Language / Advice)
- API Key configurable via env var, `.env` file, or `api_key.txt`

## Requirements

- Python 3.10+
- pip

## Install

```bash
git clone https://github.com/your-username/cyber-oracle.git
cd cyber-oracle
pip install zhdate openai
```

## API Key Setup

Choose **one** of the following:

```bash
# Option 1: Environment variable
set DEEPSEEK_API_KEY=sk-your-key-here

# Option 2: .env file in project root
echo DEEPSEEK_API_KEY=sk-your-key-here > .env

# Option 3: api_key.txt (just paste the key)
echo sk-your-key-here > api_key.txt
```

## Usage

```bash
python cyber_oracle.py
```

Enter the event time in `YYYY-MM-DD HH:MM` format, or press Enter for the current time. Then type your question.

```
==================================================
   * 赛博神棍
==================================================

Please enter the event time (YYYY-MM-DD HH:MM), or press Enter to use current time:
>

Present hexagram: 天雷无妄 ☰☳
Changed hexagram: 天风姤 ☰☴
Moving line: 2

Your question: How will my career go?
```

## Algorithm

The time-based hexagram formula:

| Component | Formula |
|-----------|---------|
| Upper trigram | (Year branch + Month + Day) % 8 (0→8) |
| Lower trigram | (Year branch + Month + Day + Hour branch) % 8 (0→8) |
| Moving line | (Year branch + Month + Day + Hour branch) % 6 (0→6) |

Trigram mapping: 1=Qian☰ 2=Dui☱ 3=Li☲ 4=Zhen☳ 5=Xun☴ 6=Kan☵ 7=Gen☶ 8=Kun☷

## Disclaimer

For entertainment purposes only. AI-generated interpretation should not be used as decision-making basis.

---

# 🔮 赛博神棍 

> **用《周易》的智慧 + 赛博的算力，给你算一卦。**

一个命令行易经算命程序，基于梅花易数时间卦法起卦，调用 DeepSeek LLM 进行卦象解读。

## 功能

- 输入公历时间，自动转换为农历，计算时间卦
- 梅花易数正统算法：年支 + 月 + 日 → 上卦 / 年支 + 月 + 日 + 时 → 下卦 + 动爻
- 六十四卦完整映射，支持本卦 → 变卦推算
- 调用 DeepSeek API 输出三段式解读（卦象详解 / 白话解读 / 切实建议）
- 支持环境变量、`.env` 文件、`api_key.txt` 三种方式配置 API Key

## 环境要求

- Python 3.10+
- pip

## 安装

```bash
git clone https://github.com/你的用户名/赛博神棍.git
cd 赛博神棍
pip install zhdate openai
```

## 配置 API Key

任选一种：

```bash
# 方式一：环境变量
set DEEPSEEK_API_KEY=sk-your-key-here

# 方式二：在项目目录下创建 .env 文件
echo DEEPSEEK_API_KEY=sk-your-key-here > .env

# 方式三：在项目目录下创建 api_key.txt，写入 key
echo sk-your-key-here > api_key.txt
```

## 使用

```bash
python cyber_oracle.py
```

按提示输入事件发生的公历时间（格式 `YYYY-MM-DD HH:MM`），直接回车使用当前时间。然后输入你想问的问题。

示例输出：

```
==================================================
   * 赛博神棍
==================================================

请输入事件发生的公历时间（格式：YYYY-MM-DD HH:MM），直接回车使用当前时间：
>

起卦时间（农历）：丙午年3月23日（癸酉日）戌时

☯  本卦：天雷无妄 ☰☳
☯  变卦：天风姤 ☰☴
☯  动爻：第 2 爻

请输入您想问的问题（直接回车则跳过大师解读）：
> 最近工作怎么样

[*] 正在请求赛博大师解读，请稍候...
```

## 算法说明

梅花易数时间卦法：

| 项目 | 计算 |
|------|------|
| 上卦 | (年地支序数 + 月数 + 日数) % 8，余 0 取 8 |
| 下卦 | (年地支序数 + 月数 + 日数 + 时地支序数) % 8，余 0 取 8 |
| 动爻 | (年地支序数 + 月数 + 日数 + 时地支序数) % 6，余 0 取 6 |

八卦对应：1乾☰ 2兑☱ 3离☲ 4震☳ 5巽☴ 6坎☵ 7艮☶ 8坤☷

## 免责声明

本程序仅供娱乐参考。卦象解读由 AI 生成，不可作为决策依据。命运在自己手中。

## 技术栈

- Python 3
- [zhdate](https://pypi.org/project/zhdate/) — 公历农历转换
- [OpenAI Python SDK](https://pypi.org/project/openai/) — DeepSeek API 调用
- DeepSeek Chat API — 卦象解读
