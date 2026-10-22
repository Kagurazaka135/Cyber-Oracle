# -*- coding: utf-8 -*-
"""诸葛神数占卜模块

对外唯一接口：calculate(chars) -> dict
"""

import os
import json

KANGXI_STROKES = {
    "一": 1, "二": 2, "三": 3, "四": 5, "五": 4,
    "六": 4, "七": 2, "八": 2, "九": 9, "十": 2,
    "我": 7, "你": 7, "他": 5, "她": 6, "它": 5,
    "是": 9, "的": 8, "不": 4, "了": 2, "在": 6,
    "有": 6, "人": 2, "个": 10, "们": 10, "大": 3,
    "来": 8, "上": 3, "中": 4, "下": 3, "为": 12,
    "和": 8, "与": 13, "这": 10, "那": 7, "要": 9,
    "心": 4, "想": 13, "问": 11, "题": 15, "找": 8,
    "工": 3, "作": 7, "好": 6, "坏": 17, "对": 13,
    "错": 14, "能": 10, "可": 5, "会": 13, "去": 5,
    "说": 14, "看": 9, "听": 22, "走": 7, "跑": 12,
    "吃": 9, "喝": 15, "睡": 13, "买": 12, "卖": 14,
    "钱": 16, "财": 10, "运": 12, "爱": 13, "情": 11,
    "婚": 14, "家": 10, "父": 4, "母": 5, "子": 3,
    "女": 3, "夫": 4, "妻": 8, "朋": 8, "友": 4,
    "学": 16, "老": 6, "师": 10, "生": 5, "病": 10,
    "死": 6, "年": 6, "月": 4, "日": 4, "时": 10,
    "今": 4, "明": 8, "昨": 9, "天": 4, "地": 6,
    "水": 4, "火": 4, "風": 9, "风": 9, "雨": 8,
    "雷": 13, "电": 13, "山": 3, "海": 10, "夢": 12,
    "梦": 11, "金": 8, "木": 4, "土": 3, "石": 5,
    "花": 7, "草": 9, "树": 16, "叶": 12, "果": 8,
    "春": 9, "夏": 10, "秋": 9, "冬": 5, "紅": 9,
    "红": 9, "白": 5, "黑": 12, "黄": 12, "蓝": 17,
    "开": 12, "关": 19, "进": 12, "退": 9, "出": 5,
    "成": 7, "败": 11, "得": 11, "失": 5, "真": 10,
    "假": 13, "善": 12, "恶": 12, "美": 9, "丑": 4,
    "高": 10, "低": 7, "长": 8, "短": 12, "多": 6,
    "少": 4, "快": 7, "慢": 15, "早": 6, "晚": 10,
    "东": 8, "西": 6, "南": 9, "北": 5, "前": 9,
    "后": 8, "左": 5, "右": 5, "内": 4, "外": 5,
    "身": 7, "体": 23, "手": 4, "脚": 15, "头": 16,
    "眼": 11, "口": 3, "耳": 6, "鼻": 14, "舌": 6,
    "行": 6, "飞": 9, "跑": 12, "跳": 13, "坐": 7,
    "站": 10, "等": 12, "回": 6, "過": 12, "过": 7,
    "安": 6, "全": 6, "忙": 9, "闲": 13, "空": 8,
    "魚": 11, "鱼": 11, "虎": 8, "龙": 16, "鹤": 21,
    "馬": 10, "马": 10, "鸟": 11, "蛇": 11, "鼠": 13,
    "福": 13, "禄": 12, "寿": 14, "喜": 12, "吉": 6,
    "凶": 5, "贵": 12, "富": 12, "穷": 15, "苦": 8,
    "乐": 15, "怒": 9, "悲": 12, "恐": 13, "惊": 22,
    "忘": 7, "记": 16, "认": 14, "识": 19, "让": 5,
    "行": 6, "等": 12, "把": 7, "给": 9, "被": 10,
    "用": 5, "道": 12, "理": 11, "事": 8, "物": 8,
    "新": 13, "旧": 17, "易": 8, "难": 19, "行": 6,
}


def _load_qian_data():
    """加载签文 JSON，返回字典"""
    this_dir = os.path.dirname(__file__)
    json_path = os.path.join(this_dir, "..", "data", "zhuge_qian.json")
    if not os.path.exists(json_path):
        print(f"[警告] 神楽坂じゃん找不到签文了：{json_path}")
        return {}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


DEFAULT_QIAN = {
    "title": "签文暂缺",
    "poem": "三字通天地\n一签问古今\n吉凶皆自取\n何必问神明",
    "interpretation": "此签暂无记载，请以平常心看待。",
}

QIAN_DATA = _load_qian_data()


def _stroke_to_digit(stroke_count):
    """笔画数 % 8，余 0 取 8，返回 1-8"""
    r = stroke_count % 8
    return 8 if r == 0 else r


def calculate(chars):
    """
    诸葛神数计算入口。
    参数：
        chars: 用户输入的字符串，比如 "找工作"
    返回：
        dict: method, input, qian_number, qian_data
    """
    # 清洗输入，去掉空白
    cleaned = "".join(chars.split())
    if len(cleaned) == 0:
        raise ValueError("至少需要输入一个汉字哦，比如'找工作'这样三个字。")

    # 拆成单个字符，只取前三个
    char_list = list(cleaned)[:3]

    # 检查是否全是汉字
    for c in char_list:
        if not ("一" <= c <= "鿿"):
            raise ValueError(
                f"'{c}' 看起来不是中文汉字哦。请输入三个汉字，比如'找工作'。"
            )

    # 查康熙笔画
    strokes = []
    for c in char_list:
        if c in KANGXI_STROKES:
            s = KANGXI_STROKES[c]
            strokes.append(s)
            print(f"  '{c}' -> {s}画（康熙字典）")
        else:
            print(f"\n  [注意] '{c}' 在康熙笔画字典里没找到。")
            user_input = input(
                f"  请手动输入 '{c}' 的康熙笔画数（1-30）：> "
            ).strip()
            try:
                s = int(user_input)
                if s < 1 or s > 30:
                    raise ValueError(
                        f"笔画数不太对劲（你输入了 {s}），应该在 1-30 之间。"
                    )
                strokes.append(s)
            except ValueError:
                raise ValueError(
                    f"请输入数字呀，'{user_input}' 不是有效的数字。"
                )

    # 不足三个字补 0
    while len(strokes) < 3:
        strokes.append(0)

    # 诸葛神数公式：三字笔画各 %8 余0取8，组成三位数
    hundreds = _stroke_to_digit(strokes[0])
    tens = _stroke_to_digit(strokes[1])
    ones = _stroke_to_digit(strokes[2])
    qian = hundreds * 100 + tens * 10 + ones

    # 大于 384 则循环减 384
    while qian > 384:
        qian -= 384
    if qian <= 0:
        qian = 1

    # 查签文，取不到用兜底签
    qian_key = str(qian)
    qian_data = QIAN_DATA.get(qian_key, DEFAULT_QIAN)

    return {
        "method": "诸葛神数",
        "input": {
            "chars": char_list,
            "strokes": strokes,
        },
        "qian_number": qian,
        "qian_data": qian_data,
    }
