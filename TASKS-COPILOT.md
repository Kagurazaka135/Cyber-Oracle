# 任务书：补完诸葛神数 + 新增小六壬 / 灵签 / 金钱卦

> 施工目录：**本仓库根目录**（本地对应 `G:\code\赛博神棍\`）
> 只改这四个位置：`main.py`、`methods/`、`utils/`、`data/`
> 数据已准备好，放在 `data/`，**只读，不要重新抓取、不要改内容、不要删**。

> ⚠️ **只做本任务。** 不要读仓库以外的任何文件（包括 `~/.claude`、memory、mailbox），不要提交 `api_key.txt`、`.env`。

---

## 〇、目标形态（验收时的最终状态）

运行 `python main.py`，菜单里有 **7 种方法**：

```
  1. 梅花易数时间卦法
  2. 塔罗牌占卜
  3. 称骨算命
  4. 诸葛神数
  5. 小六壬
  6. 灵签（关帝）
  7. 金钱卦
```

四种方法都能从头走到尾：输入 → 计算 → 打印结果 → 可选 LLM 解读。
**诸葛神数从"半成品"变为完整 384 签**，且计算函数不再依赖终端输入。
新增三种方法的计算函数都是**纯函数**，可在测试里直接调用、不弹 `input()`。

---

## 一、特性清单（必须全部满足）

1. **诸葛神数**
   - 签库 384 条全量可用，任意签号 1–384 都能查到。
   - 康熙笔画查不到时**抛 `ValueError`**并指明是哪个字，不再交互式询问用户。
   - `calculate(chars)` 的返回结构保持兼容：`method` / `input` / `qian_number` / `qian_data`，其中 `qian_data` 至少含 `title`、`poem`、`interpretation` 三个键（`llm_module.py` 依赖）。
   - 公式不变：三个字笔画各 `%8` 余 0 取 8，组成三位数，>384 反复减 384，≤0 取 1。

2. **小六壬**
   - 公式：`month_digit = ((lunar_month-1)%6)+1`；`day_digit = ((month_digit+lunar_day-2)%6)+1`；`final_digit = ((day_digit+shichen_order-2)%6)+1`。
   - 输出包含推算三步的中间位置（供 CLI 打印过程）和最终掌诀的完整断辞。
   - 农历数据来自现有 `utils/lunar.py`，不得另起一套。

3. **灵签（关帝）**
   - 默认随机抽 1–100；也支持指定签号（便于测试）。
   - 输出含签号、吉凶等级、四句签诗、断语；签诗**保留繁体**原样。

4. **金钱卦**
   - 默认随机掷六次；也支持传入六次结果（每次为 6/7/8/9，或 `"121"` 这种三枚硬币字符串）。
   - 正确区分本卦 / 变卦 / 动爻；无 6、9 时为静卦（`changed` 为 `None`）。
   - 卦名、卦辞、爻辞来自 `data\iching_full.json`；六个爻的上下卦拆分可复用 `utils/hexagram.py` 的思路，但**不要改动该文件的既有接口**。

5. **四种新老方法的 CLI 输出**
   - 都要有独立的 `_display_xxx()`，打印关键信息（不打印原始 JSON）。
   - 诸葛神数显示：三个字 → 康熙笔画 → 签号 → 签题/吉凶 → 签诗 → 短断语。

6. **LLM 解读**
   - `llm_module.py` 的 `interpret()` 能路由到新增三种方法，各写一个 `_interpret_xxx()`。
   - prompt 要求：结合用户问题与所得卦象/签文，语气自然，不复述原文。

7. **无新增第三方依赖**
   - 只允许 Python 标准库 + 现有 `zhdate` / `openai` / `dateparser`。不要引入 `opencc`、`pypinyin`、`requests` 等。

8. **测试**
   - 新增 `tests\selftest.py`，**不依赖 pytest**，直接 `python tests\selftest.py` 运行，全部通过时退出码 0。

---

## 二、施工步骤

### 步骤 1：接通数据目录

**改掉：**
- `methods\zhuge.py` 里 `_load_qian_data()` 读取 `methods/zhuge_qian.json` 的路径 → 改为读取 `data\zhuge_qian.json`。

**保留：**
- `DEFAULT_QIAN` 兜底签逻辑（数据缺失时仍能返回）。
- `_stroke_to_digit()` 的现有行为。
- `calculate()` 的返回字段名（见特性清单第 1 条）。

**验收：** `python -c "from methods.zhuge import QIAN_DATA; print(len(QIAN_DATA))"` 输出 `384`。

---

### 步骤 2：补完诸葛神数

**改掉：**
- `calculate()` 内部所有 `input()` 与 `print()` 交互（第 100 行前后那段逐字询问笔画的代码）→ 改为查 `data\kangxi_strokes.json`；查不到直接 `raise ValueError(f"'{c}' 不在康熙笔画字典里")`。
- 康熙笔画字典来源从 `methods\zhuge.py` 内嵌的 225 字 `KANGXI_STROKES` → 改为加载 `data\kangxi_strokes.json`（20794 字）。内嵌字典可以删除。

**保留：**
- 输入清洗、只取前三个字、非汉字校验、不足三字补 0 的行为。
- 公式与返回结构。

**验收：**
- `calculate("找工作")` 返回 `qian_number == 69`（找=8、工=3、作=7 → 837 → 453 → 69）。
- `calculate("找工作")["qian_data"]["title"]` 非空。
- `calculate("zzz")` 抛 `ValueError`。

---

### 步骤 3：新增 `methods\xiao_liu_ren.py`

接口：`calculate(dt: datetime, question: str = "") -> dict`

**返回结构：**
```python
{
  "method": "小六壬",
  "dt": dt,
  "lunar": {...},                  # 直接复用 utils.lunar.get_lunar_info(dt)
  "steps": {"month": 4, "day": 2, "hour": 1},   # 三步落位 1-6
  "final": {
      "position": 1, "name": "大安", "luck": "吉",
      "verse": "大安事事昌……", "fortune": "……",
      "career": "……", "love": "……", "health": "……",
      "lost": "……", "travel": "……"
  },
  "question": question
}
```
掌诀数据从 `data\xiaoliuren.json` 读取，键为 `"1"`–`"6"`。

**验收：** 构造农历十月初五巳时的公历时间，三步应为 `4 → 2 → 1`，最终「大安」。
（若构造农历不便，可在测试里直接对公式函数做单元断言，再用真实时间跑通一次。）

---

### 步骤 4：新增 `methods\ling_qian.py`

接口：`calculate(qian_number: int | None = None, question: str = "") -> dict`

**返回结构：**
```python
{
  "method": "灵签（关帝）",
  "qian_number": 17,
  "qian_data": {
      "number": 17, "title": "第17签", "grade": "上吉",
      "poem": "……", "keywords": [...], "interpretation": "……"
  },
  "question": question
}
```
`qian_number` 为 `None` 时用 `random.randint(1, 100)`。数据来自 `data\ling_qian_guan_di.json`。

**验收：** `calculate(1)["qian_data"]["poem"]` 第一行为 `巍巍獨步向雲間`；随机调用 200 次，签号全部落在 1–100。

---

### 步骤 5：新增 `methods\coin_hexagram.py`

接口：`calculate(throws: list | None = None, question: str = "") -> dict`

参数说明：
- `throws` 为 `None` → 随机生成 6 个值，每个从 `[6, 7, 8, 9]` 按真实概率取（6/9 各约 1/8，7/8 各约 3/8）。
- `throws` 元素可以是整数 `6/7/8/9`，也可以是 `"121"` 这类三位字符串（`1`=正面/字=2，`2`=背面/花=3，求和得爻值）。字符串与整数混用也要支持。

**返回结构：**
```python
{
  "method": "金钱卦",
  "throws": [9, 7, 7, 7, 7, 7],        # 自下而上，第 1 项为初爻
  "lines": [{"position": 1, "value": 9, "yin_yang": "阳", "moving": True}, ...],
  "original": {"id": 1, "name": "乾", "symbol": "䷀", "scripture": "元亨利贞。",
               "moving_text": "初九：潜龙，勿用。"},   # moving_text 仅当恰好一个动爻时给出
  "changed": {"id": ..., "name": ..., "symbol": ..., "scripture": ...},  # 静卦为 None
  "moving_lines": [1],
  "question": question
}
```
卦数据来自 `data\iching_full.json`（列表，按 `id` 1–64）。该数据每卦 `lines` 有 7 项（第 7 项为用九/用六），**只用前 6 项**对应初爻到上爻。

**验收：**
- `calculate([7,7,7,7,7,7])` → 本卦「乾」，`changed is None`，`moving_lines == []`。
- `calculate([8,8,8,8,8,8])` → 本卦「坤」。
- `calculate([9,9,9,9,9,9])` → 本卦「乾」，变卦「坤」，`moving_lines == [1,2,3,4,5,6]`。
- 随机跑 100 次，`original["name"]` 全部能在 64 卦里找到，无异常。

---

### 步骤 6：接入 `main.py`

**改掉：**
- `METHODS` 字典 → 增加三项 `"5"` 小六壬 / `"6"` 灵签 / `"7"` 金钱卦。
- 主流程 → 为三种新方法各加一个输入分支（时间 / 是否指定签号 / 是否手动掷币，均可直接回车走默认）。
- 增加 `_display_xiao_liu_ren()` / `_display_ling_qian()` / `_display_coin_hexagram()`。

**保留：**
- 现有 1–4 号的输入流程、打印格式、`_parse_time()`、`_display_*` 函数行为**一律不动**。
- 结尾"请输入您想问的问题"那段逻辑继续复用。

**验收：** 依次手动跑 7 个方法，每个都能走到"请输入您想问的问题"这一步不报错。

---

### 步骤 7：接入 `llm_module.py`

**改掉：**
- `interpret()` 的分派 → 增加「小六壬」「灵签」「金钱卦」三个分支。
- 新增 `_interpret_xiao_liu_ren()` / `_interpret_ling_qian()` / `_interpret_coin_hexagram()`。

**保留：**
- 现有四个 `_interpret_*()` 与 `_get_client()` / `_get_api_key()` 不动。
- 未配置 API key 时的降级行为（跳过解读）不动。

**验收：** 未设置 API key 时跑四种新方法，程序提示跳过解读而不是崩溃。

---

### 步骤 8：写 `tests\selftest.py`

覆盖：
1. 诸葛：384 条、`"找工作"` → 69、非汉字抛错。
2. 小六壬：公式三个中间值、最终落位、六掌诀字段齐全。
3. 灵签：指定 1 号的内容、随机 200 次范围。
4. 金钱卦：上述四组固定掷币的断言。
5. 回归：梅花易数 / 塔罗 / 称骨各跑一次，确认返回 `method` 字段没变。

**验收：** `python tests\selftest.py` 退出码 0，输出 `ALL PASS`。

---

## 三、边界与反例（必须按此处理）

| 情况 | 期望行为 |
|---|---|
| 诸葛输入不足三字（如"找工作"只有两字） | 不足补 0，按现有逻辑继续 |
| 诸葛输入含英文/数字 | `ValueError`，提示不是汉字 |
| 康熙字典查不到某生僻字 | `ValueError`，指明该字，**不得猜笔画** |
| 灵签签号传 0 / 101 | `ValueError` |
| 金钱卦 `throws` 长度不是 6 | `ValueError` |
| 金钱卦传入非法值（如 5、10） | `ValueError` |
| 静卦 | `changed is None`，CLI 不打印"变卦" |
| 多个动爻 | 不给 `moving_text`，`moving_lines` 完整列出 |
| 数据文件缺失 | 明确报错并指出缺哪个文件，不要静默用空数据跑 |

---

## 四、不要做的事

- ❌ 不要改动 `methods\plum_blossom.py` / `tarot.py` / `bone_weight.py`。
- ❌ 不要改动 `utils\lunar.py` / `utils\hexagram.py` 的既有函数签名与返回字段。
- ❌ 不要联网抓数据、不要重新生成 `data\` 下的任何文件。
- ❌ 不要新增第三方依赖。
- ❌ 不要把签诗自动转简体。
- ❌ 不要为了"看起来整齐"改写现有 1–4 号的输出格式。
- ❌ 不要删除 `methods/zhuge_qian.json` 之外的旧文件（该文件在步骤 1 完成后可以删，但需在提交说明里写明）。

---

## 五、交付物

1. 修改后的 `methods\zhuge.py`、`main.py`、`llm_module.py`。
2. 新增 `methods\xiao_liu_ren.py`、`methods\ling_qian.py`、`methods\coin_hexagram.py`。
3. 新增 `tests\selftest.py`。
4. 一份简短的 `CHANGES.md`，列出：改了什么、保留了什么、`python tests\selftest.py` 的实际输出。

## 六、自检清单（提交前逐项打勾）

- [ ] `python tests\selftest.py` 输出 `ALL PASS`
- [ ] `python main.py` 七个方法都能跑到解读提示
- [ ] 诸葛神数任意抽 10 个签号，签文都不为空
- [ ] 康熙笔画抽查：「找=8、爱=13、龙=16」
- [ ] 金钱卦静卦与多动爻两种边界都手动跑过一次
- [ ] 未配置 API key 时四种新方法都不崩溃
- [ ] 1–4 号方法的输出与改动前一致（逐字对比）
