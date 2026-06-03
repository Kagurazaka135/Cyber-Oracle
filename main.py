# -*- coding: utf-8 -*-
"""
赛博神棍 (Cyber Oracle) —— 命令行入口
用法：python main.py
依赖：pip install zhdate openai dateparser
"""

import sys
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    from zhdate import ZhDate
except ImportError:
    print("[X] 缺少依赖库 zhdate，请执行：pip install zhdate")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("[X] 缺少依赖库 openai，请执行：pip install openai")
    sys.exit(1)

try:
    import dateparser
except ImportError:
    print("[X] 缺少依赖库 dateparser，请执行：pip install dateparser")
    sys.exit(1)

from methods.plum_blossom import calculate as plum_blossom_calculate
from methods.tarot import calculate as tarot_calculate
from llm_module import interpret


METHODS = {
    "1": ("梅花易数时间卦法", plum_blossom_calculate),
    "2": ("塔罗牌占卜", tarot_calculate),
}


def _parse_time() -> datetime:
    prompt = "\n请输入事件发生的公历时间（直接回车使用当前时间，支持多种格式）：\n> "
    time_input = input(prompt).strip()

    if time_input == "":
        now = datetime.now()
        print(f"[OK] 使用当前系统时间：{now.strftime('%Y-%m-%d %H:%M')}")
        return now

    dt = dateparser.parse(time_input, languages=["zh"])
    if dt is None:
        print("[X] 没看懂你输的时间，试试 2025-06-15 14:30 或 明天下午三点 这类格式。")
        sys.exit(1)
    return dt.replace(second=0, microsecond=0)


def _select_method() -> tuple:
    if len(METHODS) == 1:
        name, func = list(METHODS.items())[0]
        return func, name
    print("\n请选择算命方法：")
    for key, (name, _) in METHODS.items():
        print(f"  {key}. {name}")
    choice = input("> ").strip()
    if choice not in METHODS:
        print("[X] 无效选择")
        sys.exit(1)
    return METHODS[choice][1], METHODS[choice][0]


def _display_tarot(result: dict):
    print(f"\n{'=' * 50}")
    print(f"  牌阵：{result['spread_name']}")
    print(f"{'=' * 50}")
    for c in result["cards"]:
        orientation = "* 正位" if c["upright"] else "▼ 逆位"
        suit_tag = ""
        if c["type"] == "minor":
            suit_tag = f"  [{c['suit_name']}·{c['element']}]"
        card_name_display = f"{c['name']} ({c['name_en']})"
        meaning = c["meaning_upright"] if c["upright"] else c["meaning_reversed"]
        print(f"  [{c['position']}] {card_name_display}  {orientation}{suit_tag}")
        print(f"        {meaning}")
        print()


def _display_hexagram(result: dict):
    lunar = result["lunar"]
    print(f"\n起卦时间（公历）：{lunar['datetime'].strftime('%Y年%m月%d日 %H:%M')}")
    print(f"起卦时间（农历）：{lunar['year_ganzhi']}年{lunar['lunar_month']}月"
          f"{lunar['lunar_day']}日（{lunar['day_ganzhi']}日）{lunar['shichen_name']}时")

    og = result["original"]
    ch = result["changed"]
    dl = result["dynamic_line"]

    print(f"\n☯  本卦：{og['name']} {og['symbol']}")
    print(f"☯  变卦：{ch['name']} {ch['symbol']}")
    print(f"☯  动爻：第 {dl} 爻")


def main():
    print("=" * 50)
    print("   * 赛博神棍 ")
    print("=" * 50)

    method_func, method_name = _select_method()
    is_tarot = "塔罗" in method_name

    if is_tarot:
        user_question = input("\n请输入你想问的问题（在心里默念，回车确认）：\n> ").strip()
        if not user_question:
            user_question = "一般指引"
            print("[OK] 未输入问题，使用默认：「一般指引」")
        dt = datetime.now()
        #print(f"[OK] 使用当前时间：{dt.strftime('%Y-%m-%d %H:%M')}")
        result = method_func(dt, user_question)
    else:
        dt = _parse_time()
        result = method_func(dt, "")
        user_question = ""

    if is_tarot:
        _display_tarot(result)
    else:
        _display_hexagram(result)

    if not is_tarot:
        user_question = input("\n请输入您想问的问题（直接回车则跳过大师解读）：\n> ").strip()
        if not user_question:
            print("已跳过解读，再见！")
            return

    print("\n[*] 正在请求赛博大师解读，请稍候...\n")
    try:
        llm_result = interpret(result, user_question)
        print("=" * 50)
        print(llm_result or "(AI 返回了空内容)")
        print("=" * 50)
    except Exception as e:
        print(f"[X] 解读失败：{e}")


if __name__ == "__main__":
    main()
