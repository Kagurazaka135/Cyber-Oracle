# -*- coding: utf-8 -*-
"""LLM 解读模块：API Key 管理与多方法解读路由"""

import os
from openai import OpenAI


def _get_api_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key

    candidate_dirs = []
    try:
        candidate_dirs.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    candidate_dirs.append(os.getcwd())

    seen = set()
    for d in candidate_dirs:
        d = os.path.abspath(d)
        if d in seen:
            continue
        seen.add(d)

        env_path = os.path.join(d, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() == "DEEPSEEK_API_KEY":
                        v = v.strip().strip('"').strip("'")
                        os.environ["DEEPSEEK_API_KEY"] = v
                        return v

        txt_path = os.path.join(d, "api_key.txt")
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                key = f.read().strip()
                if key:
                    os.environ["DEEPSEEK_API_KEY"] = key
                    return key

    return ""


def _get_client():
    api_key = _get_api_key()
    if not api_key:
        cwd = os.getcwd()
        raise RuntimeError(
            f"[X] 未找到 DEEPSEEK_API_KEY。请任选一种方式配置：\n"
            f"    1. 设置环境变量：set DEEPSEEK_API_KEY=your_key\n"
            f"    2. 在 {cwd} 下创建 .env 文件，内容：DEEPSEEK_API_KEY=your_key\n"
            f"    3. 在 {cwd} 下创建 api_key.txt，写入 key"
        )
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def _interpret_hexagram(result: dict, user_question: str) -> str:
    client = _get_client()
    lunar = result["lunar"]
    lunar_time = {
        "year": f"{lunar['year_ganzhi']}（{lunar['lunar_year']}）",
        "month": f"{lunar['lunar_month']}",
        "day": f"{lunar['lunar_day']}（{lunar['day_ganzhi']}）",
        "hour": lunar["shichen_name"],
    }
    og = result["original"]
    ch = result["changed"]
    dl = result["dynamic_line"]

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": (
                    "你是一位精通《周易》的命理大师。请按以下结构输出解读：\n"
                    "一、卦象详解：用传统周易术语，分析本卦、变卦、动爻的卦象含义。\n"
                    "二、白话解读：用现代口语、生活化的语言重新解释一遍，像朋友聊天一样，避免文言和术语，让人一看就懂。\n"
                    "三、切实建议：给出具体、可操作的行动建议。\n"
                    "最后赛博神棍的话，看看就行了。"
                )},
                {"role": "user", "content": (
                    f"起卦时间（农历）：{lunar_time['year']}年{lunar_time['month']}月"
                    f"{lunar_time['day']}日{lunar_time['hour']}时\n"
                    f"用户所问之事：{user_question}\n"
                    f"本卦：{og['name']}（{og['symbol']}）\n"
                    f"变卦：{ch['name']}（{ch['symbol']}）\n"
                    f"动爻：第{dl}爻"
                )},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[X] 调用 LLM 失败：{e}")


def _interpret_tarot(result: dict, user_question: str) -> str:
    client = _get_client()
    cards = result["cards"]
    spread = result["spread"]

    card_lines = []
    for c in cards:
        orientation = "正位" if c["upright"] else "逆位"
        meaning = c["meaning_upright"] if c["upright"] else c["meaning_reversed"]
        suit_info = ""
        if c["type"] == "minor":
            suit_info = f" ({c['suit_name']}·{c['element']}元素)"
        card_lines.append(
            f"  [{c['position']}位置] {c['name']} ({c['name_en']}) — {orientation}{suit_info}\n"
            f"    牌义：{meaning}"
        )

    cards_text = "\n".join(card_lines)

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": (
                    "你是一位精通塔罗牌的占卜大师。请按以下结构输出解读：\n\n"
                    "一、牌面详解：逐张解读每张牌在当前位置的含义（正位/逆位），"
                    "结合牌的元素属性和用户提问，给出个性化分析。\n\n"
                    "二、综合解读：将牌阵中所有牌联系起来，找出牌与牌之间的关联、"
                    "矛盾和呼应，分析整体的能量趋势和内在逻辑。\n\n"
                    "三、切实建议：给出具体、可操作的行动建议，帮助用户将牌阵的"
                    "信息转化为实际生活中的行动。\n\n"
                    "最后赛博神棍的话，看看就行了。"
                    "注意：第一部分的牌面详解可以用专业术语和传统表达风格，但在综合解读和切实建议部分，切换成朋友聊天的语气——用自然段落、不用编号列表、不用小标题、不用加粗。就像你一边看着牌一边跟朋友面对面说话那样。"
                )},
                {"role": "user", "content": (
                    f"牌阵：{result.get('spread_name', '塔罗牌阵')}\n"
                    f"抽牌数量：{spread['cards']} 张\n"
                    f"用户所问之事：{user_question}\n\n"
                    f"抽牌结果：\n{cards_text}"
                )},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[X] 调用 LLM 失败：{e}")


def _interpret_bone_weight(result: dict, user_question: str) -> str:
    client = _get_client()
    lunar = result["lunar"]
    weights = result["weights"]
    bone_weight = result["bone_weight"]

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": (
                    "你是一位精通袁天罡称骨法的命理大师。请按以下结构输出解读：\n\n"
                    "一、骨重解析：解释这个骨重在称骨法中的地位——是轻是重？落在什么段位？"
                    "从2两到7两的分布中它处于什么位置？记住：称骨法有一个有趣的统计现象——"
                    "四个独立分量的加总会让大部分人的骨重自然落在3两到5两之间，"
                    "落在两端的（极轻/极重）在概率上本来就极少。\n\n"
                    "二、批语白话：将称骨歌原文用现代口语重新表达，让用户一看就懂，"
                    "像朋友聊天一样，避免文言术语。\n\n"
                    "三、切实建议：根据骨重格局，给出具体的生活建议。"
                    "但务必强调：命格只是底色，后天努力才是真正的画笔。"
                    "骨重轻的人靠勤奋弥补，骨重重的人靠谦虚守住。"
                    "称骨看个乐子，日子靠自己过。\n\n"
                    "注意：用朋友聊天的语气，不要教条，可以适当幽默。"
                )},
                {"role": "user", "content": (
                    f"用户出生时间（公历）：{result['birth_dt']}\n"
                    f"农历：{lunar['year_ganzhi']}年{lunar['lunar_month']}月"
                    f"{lunar['lunar_day']}日 {lunar['shichen_name']}时\n"
                    f"性别：{result['gender']}\n"
                    f"四柱重量：年柱{weights['year']}钱 + 月柱{weights['month']}钱"
                    f" + 日柱{weights['day']}钱 + 时柱{weights['hour']}钱"
                    f" = 总骨重{result['bone_weight']}（{weights['total']}钱）\n"
                    f"称骨歌批语原文：{result['poem']}\n"
                    + (f"用户所问之事：{user_question}" if user_question else "")
                )},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[X] 调用 LLM 失败：{e}")


def _interpret_zhuge(result: dict, user_question: str) -> str:
    client = _get_client()
    qd = result["qian_data"]
    inp = result["input"]
    chars_text = "".join(inp["chars"])

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": (
                    "你是一位精通诸葛神数的解签大师。请按以下结构输出解读：\n\n"
                    "一、签文详解：解读签诗的含义，分析签名的意象。"
                    "诸葛神数共384签，每签的签诗都是一首七言绝句，"
                    "蕴含传统命理智慧。请结合签诗本身进行分析。\n\n"
                    "二、与字关联：用户所报的三个字带有自身意念，"
                    "请将三个字的意象与签诗内容相互印证，"
                    "找出字与签之间的呼应关系。\n\n"
                    "三、白话解读：用现代口语、生活化的语言重新解释一遍，"
                    "像朋友聊天一样，避免文言和术语，让人一看就懂。\n\n"
                    "四、切实建议：给出具体、可操作的行动建议。\n\n"
                    "最后提醒：赛博神棍的话，看看就行了，别太当真。"
                )},
                {"role": "user", "content": (
                    f"用户所报三个字：{chars_text}\n"
                    f"康熙笔画数：{inp['strokes']}\n"
                    f"求得 —— 第 {result['qian_number']} 签：{qd['title']}\n"
                    f"签诗：\n{qd['poem']}\n"
                    f"签文断语：{qd['interpretation']}\n"
                    + (f"\n用户所问之事：{user_question}" if user_question else "")
                )},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[X] 调用 LLM 失败：{e}")


def interpret(result: dict, user_question: str) -> str:
    """统一入口：根据 result 中的 method 自动路由到对应解读"""
    method = result.get("method", "")
    if "塔罗" in method:
        return _interpret_tarot(result, user_question)
    if "称骨" in method:
        return _interpret_bone_weight(result, user_question)
    if "诸葛" in method:
        return _interpret_zhuge(result, user_question)
    return _interpret_hexagram(result, user_question)
