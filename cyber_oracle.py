# -*- coding: utf-8 -*-
"""
赛博神棍 (Cyber Oracle) —— 梅花易数时间卦法 + DeepSeek LLM 解读
命令行易经算命程序
用法：python cyber_oracle.py
依赖：pip install zhdate openai
"""

import os
import sys
from datetime import datetime

# ============================================================
# 修复 Windows 终端 GBK 编码无法输出 emoji 的问题
# ============================================================
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# ============================================================
# 0. 依赖检查
# ============================================================
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


# ============================================================
# 1. 干支与八卦常量
# ============================================================

# 天干
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 八卦数字对应：1乾 2兑 3离 4震 5巽 6坎 7艮 8坤
TRIGRAM_NAMES = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
TRIGRAM_SYMBOLS = {1: "☰", 2: "☱", 3: "☲", 4: "☳", 5: "☴", 6: "☵", 7: "☶", 8: "☷"}
TRIGRAM_ELEMENTS = {1: "天", 2: "泽", 3: "火", 4: "雷", 5: "风", 6: "水", 7: "山", 8: "地"}

# 八卦的爻线（自下而上，1=阳爻—, 0=阴爻- -）
TRIGRAM_LINES = {
    1: [1, 1, 1],   # 乾 ☰
    2: [1, 1, 0],   # 兑 ☱
    3: [1, 0, 1],   # 离 ☲
    4: [0, 0, 1],   # 震 ☳
    5: [0, 1, 1],   # 巽 ☴
    6: [0, 1, 0],   # 坎 ☵
    7: [1, 0, 0],   # 艮 ☶
    8: [0, 0, 0],   # 坤 ☷
}

# 根据爻线模式查找卦数（用于变卦计算）
LINES_TO_TRIGRAM = {tuple(v): k for k, v in TRIGRAM_LINES.items()}

# 六十四卦映射：key = (上卦数, 下卦数) -> (卦名, 全卦符号)
HEXAGRAMS = {
    # 1-10
    (1, 1): ("乾为天", "☰☰"),
    (8, 8): ("坤为地", "☷☷"),
    (6, 4): ("水雷屯", "☵☳"),
    (7, 6): ("山水蒙", "☶☵"),
    (6, 1): ("水天需", "☵☰"),
    (1, 6): ("天水讼", "☰☵"),
    (8, 6): ("地水师", "☷☵"),
    (6, 8): ("水地比", "☵☷"),
    (5, 1): ("风天小畜", "☴☰"),
    (1, 2): ("天泽履", "☰☱"),
    # 11-20
    (8, 1): ("地天泰", "☷☰"),
    (1, 8): ("天地否", "☰☷"),
    (1, 3): ("天火同人", "☰☲"),
    (3, 1): ("火天大有", "☲☰"),
    (8, 7): ("地山谦", "☷☶"),
    (4, 8): ("雷地豫", "☳☷"),
    (2, 4): ("泽雷随", "☱☳"),
    (7, 5): ("山风蛊", "☶☴"),
    (8, 2): ("地泽临", "☷☱"),
    (5, 8): ("风地观", "☴☷"),
    # 21-30
    (3, 4): ("火雷噬嗑", "☲☳"),
    (7, 3): ("山火贲", "☶☲"),
    (7, 8): ("山地剥", "☶☷"),
    (8, 4): ("地雷复", "☷☳"),
    (1, 4): ("天雷无妄", "☰☳"),
    (7, 1): ("山天大畜", "☶☰"),
    (7, 4): ("山雷颐", "☶☳"),
    (2, 5): ("泽风大过", "☱☴"),
    (6, 6): ("坎为水", "☵☵"),
    (3, 3): ("离为火", "☲☲"),
    # 31-40
    (2, 7): ("泽山咸", "☱☶"),
    (4, 5): ("雷风恒", "☳☴"),
    (1, 7): ("天山遁", "☰☶"),
    (4, 1): ("雷天大壮", "☳☰"),
    (3, 8): ("火地晋", "☲☷"),
    (8, 3): ("地火明夷", "☷☲"),
    (5, 3): ("风火家人", "☴☲"),
    (3, 2): ("火泽睽", "☲☱"),
    (6, 7): ("水山蹇", "☵☶"),
    (4, 6): ("雷水解", "☳☵"),
    # 41-50
    (7, 2): ("山泽损", "☶☱"),
    (5, 4): ("风雷益", "☴☳"),
    (2, 1): ("泽天夬", "☱☰"),
    (1, 5): ("天风姤", "☰☴"),
    (2, 8): ("泽地萃", "☱☷"),
    (8, 5): ("地风升", "☷☴"),
    (2, 6): ("泽水困", "☱☵"),
    (6, 5): ("水风井", "☵☴"),
    (2, 3): ("泽火革", "☱☲"),
    (3, 5): ("火风鼎", "☲☴"),
    # 51-64
    (4, 4): ("震为雷", "☳☳"),
    (7, 7): ("艮为山", "☶☶"),
    (5, 7): ("风山渐", "☴☶"),
    (4, 2): ("雷泽归妹", "☳☱"),
    (4, 3): ("雷火丰", "☳☲"),
    (3, 7): ("火山旅", "☲☶"),
    (5, 5): ("巽为风", "☴☴"),
    (2, 2): ("兑为泽", "☱☱"),
    (5, 6): ("风水涣", "☴☵"),
    (6, 2): ("水泽节", "☵☱"),
    (5, 2): ("风泽中孚", "☴☱"),
    (4, 7): ("雷山小过", "☳☶"),
    (6, 3): ("水火既济", "☵☲"),
    (3, 6): ("火水未济", "☲☵"),
}


# ============================================================
# 2. 工具函数
# ============================================================

def get_shichen_order(hour: int) -> int:
    """根据24小时制的整点数，计算时辰地支序数（子=1, 丑=2, ..., 亥=12）"""
    shifted = (hour + 1) % 24
    return (shifted // 2) % 12 + 1


def get_year_branch_order(lunar_year: int) -> int:
    """根据农历年份计算年地支序数（子=1, 丑=2, ..., 亥=12）"""
    return ((lunar_year - 4) % 12) + 1


def get_day_ganzhi(gregorian_date: datetime) -> str:
    """根据公历日期计算日干支（用于展示）"""
    # 以已知的日干支为基准：1900-01-01 是 甲戌日
    base_date = datetime(1900, 1, 1)
    diff = (gregorian_date - base_date).days
    stem_index = diff % 10
    branch_index = diff % 12
    return HEAVENLY_STEMS[stem_index] + EARTHLY_BRANCHES[branch_index]


def get_hexagram_info(upper: int, lower: int) -> dict:
    """根据上卦数、下卦数返回卦名与符号"""
    key = (upper, lower)
    if key in HEXAGRAMS:
        name, symbol = HEXAGRAMS[key]
    else:
        # fallback：用卦象元素拼接
        name = TRIGRAM_ELEMENTS[upper] + TRIGRAM_ELEMENTS[lower]
        symbol = TRIGRAM_SYMBOLS[upper] + TRIGRAM_SYMBOLS[lower]
    return {"name": name, "symbol": symbol, "upper": upper, "lower": lower}


def compute_changed_hexagram(upper: int, lower: int, moving_line: int) -> dict:
    """根据本卦的上下卦数和动爻位置，计算变卦"""
    upper_lines = TRIGRAM_LINES[upper].copy()
    lower_lines = TRIGRAM_LINES[lower].copy()

    if moving_line <= 3:
        # 动爻在下卦
        idx = moving_line - 1  # 0-based
        lower_lines[idx] = 1 - lower_lines[idx]  # 阳变阴、阴变阳
    else:
        # 动爻在上卦
        idx = moving_line - 4  # 0-based 定位到上卦内
        upper_lines[idx] = 1 - upper_lines[idx]

    new_upper = LINES_TO_TRIGRAM.get(tuple(upper_lines), upper)
    new_lower = LINES_TO_TRIGRAM.get(tuple(lower_lines), lower)

    return get_hexagram_info(new_upper, new_lower)


def calculate_gua(year_branch: int, lunar_month: int, lunar_day: int, hour_branch: int):
    """梅花易数时间卦计算：返回 (上卦数, 下卦数, 动爻)"""
    base_sum = year_branch + lunar_month + lunar_day
    upper_num = base_sum % 8
    if upper_num == 0:
        upper_num = 8
    lower_num = (base_sum + hour_branch) % 8
    if lower_num == 0:
        lower_num = 8
    dynamic = (base_sum + hour_branch) % 6
    if dynamic == 0:
        dynamic = 6
    return upper_num, lower_num, dynamic


# ============================================================
# 3. LLM 解读
# ============================================================

def _get_api_key() -> str:
    """从环境变量或本地文件获取 DeepSeek API Key"""
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


def interpret(original_hexagram: dict, changed_hexagram: dict,
              dynamic_line: int, lunar_time: dict, user_question: str) -> str:
    """赛博仙人正在进行卦象解读"""
    api_key = _get_api_key()
    if not api_key:
        cwd = os.getcwd()
        raise RuntimeError(
            f"[X] 未找到 DEEPSEEK_API_KEY。请任选一种方式配置：\n"
            f"    1. 设置环境变量：set DEEPSEEK_API_KEY=your_key\n"
            f"    2. 在 {cwd} 下创建 .env 文件，内容：DEEPSEEK_API_KEY=your_key\n"
            f"    3. 在 {cwd} 下创建 api_key.txt，写入 key"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

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
                    f"起卦时间（农历）：{lunar_time['year']}年{lunar_time['month']}月{lunar_time['day']}日{lunar_time['hour']}时\n"
                    f"用户所问之事：{user_question}\n"
                    f"本卦：{original_hexagram['name']}（{original_hexagram['symbol']}）\n"
                    f"变卦：{changed_hexagram['name']}（{changed_hexagram['symbol']}）\n"
                    f"动爻：第{dynamic_line}爻"
                )},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[X] 调用 LLM 失败：{e}")


# ============================================================
# 4. 主程序
# ============================================================

def main():
    print("=" * 50)
    print("   * 赛博神棍 ")
    print("=" * 50)

    # ---- 4.1 获取公历时间 ----
    time_input = input("\n请输入事件发生的公历时间（格式：YYYY-MM-DD HH:MM），直接回车使用当前时间：\n> ").strip()

    if time_input == "":
        now = datetime.now()
        print(f"[OK] 使用当前系统时间：{now.strftime('%Y-%m-%d %H:%M')}")
    else:
        try:
            now = datetime.strptime(time_input, "%Y-%m-%d %H:%M")
        except ValueError:
            print("[X] 时间格式错误，请输入如 2025-06-15 14:30 的格式。")
            sys.exit(1)

    # ---- 4.2 公历 → 农历转换 ----
    try:
        lunar = ZhDate.from_datetime(now)
    except Exception as e:
        print(f"[X] 农历转换失败：{e}")
        sys.exit(1)

    lunar_year = lunar.lunar_year       # 农历年份数字
    lunar_month = lunar.lunar_month     # 农历月份数字（正月=1）
    lunar_day = lunar.lunar_day         # 农历日数（初一=1）
    lunar_hour = now.hour               # 公历小时，用于计算时辰

    # 年份干支
    year_stem_index = (lunar_year - 4) % 10
    year_branch_index = (lunar_year - 4) % 12
    year_ganzhi = HEAVENLY_STEMS[year_stem_index] + EARTHLY_BRANCHES[year_branch_index]

    # 时辰
    shichen_order = get_shichen_order(lunar_hour)
    shichen_name = EARTHLY_BRANCHES[shichen_order - 1]

    # 日干支
    day_ganzhi = get_day_ganzhi(now)

    print(f"\n起卦时间（公历）：{now.strftime('%Y年%m月%d日 %H:%M')}")
    print(f"起卦时间（农历）：{year_ganzhi}年{lunar_month}月{lunar_day}日（{day_ganzhi}日）{shichen_name}时")

    # ---- 4.3 梅花易数计算 ----
    year_branch_order = get_year_branch_order(lunar_year)
    upper_num, lower_num, dynamic_line = calculate_gua(
        year_branch_order, lunar_month, lunar_day, shichen_order
    )

    original = get_hexagram_info(upper_num, lower_num)
    changed = compute_changed_hexagram(upper_num, lower_num, dynamic_line)

    print(f"\n☯  本卦：{original['name']} {original['symbol']}")
    print(f"☯  变卦：{changed['name']} {changed['symbol']}")
    print(f"☯  动爻：第 {dynamic_line} 爻")

    # ---- 4.4 用户提问 ----
    user_question = input("\n请输入您想问的问题（直接回车则跳过大师解读）：\n> ").strip()
    if not user_question:
        print("已跳过解读，再见！")
        return

    # ---- 4.5 调用 LLM ----
    print("\n[*] 正在请求赛博大师解读，请稍候...\n")
    try:
        lunar_time_info = {
            "year": f"{year_ganzhi}（{lunar_year}）",
            "month": f"{lunar_month}",
            "day": f"{lunar_day}（{day_ganzhi}）",
            "hour": shichen_name,
        }
        result = interpret(original, changed, dynamic_line, lunar_time_info, user_question)
        print("=" * 50)
        print(result or "(AI 返回了空内容)")
        print("=" * 50)
    except Exception as e:
        print(f"[X] 解读失败：{e}")


if __name__ == "__main__":
    main()
