# 数据来源与校验

所有文件由克劳德酱于 2026-10-19 抓取、转换并校验。

| 文件 | 内容 | 条数 | 来源 | 许可 |
|---|---|---|---|---|
| `zhuge_qian.json` | 诸葛神数 384 签（签诗/吉凶/断语/详解） | 384 | [GitHub Gist monsterxcn](https://gist.github.com/monsterxcn/47681a6db630887d69946cc7f0faa0e6)，原站 laohuangli.net | 无明确许可，仅个人使用 |
| `ling_qian_guan_di.json` | 关帝灵签 100 签（清刊本校勘版） | 100 | [lakeofsky347/dsh-wen_xiang](https://github.com/lakeofsky347/dsh-wen_xiang) `content/lot/guandi-100` | MIT（解读文本），签诗源自维基文库公有领域 |
| `iching_full.json` | 周易 64 卦 + 卦辞 + 爻辞 | 64 卦 / 386 条爻辞 | [john-walks-slow/open-iching](https://github.com/john-walks-slow/open-iching) | 见上游仓库 |
| `kangxi_strokes.json` | 康熙笔画字典（字 → 笔画数） | 20794 字 | [shunshi-kangxi-core](https://www.npmjs.com/package/shunshi-kangxi-core) 0.1.1，取 `chars.json` 的 `kx` 字段 | MIT |
| `xiaoliuren.json` | 小六壬六掌诀（口诀 + 六类事项断辞） | 6 | 项目 spec（`G:\code\唠嗑\赛博神棍\小六壬是怎么算的.txt`）整理 | 本项目自有 |

## 校验结果

- 诸葛神数：`number` 1–384 连续无重复，7 个字段全部非空。
- 关帝灵签：`number` 1–100 连续无重复，签诗与解读无缺失。
- 周易：64 卦 id 1–64 连续，每卦 6 条爻辞（乾坤另含用九/用六，合计 386 条），卦辞无缺失。
- 康熙笔画：20794 字，`kx` 全为整数；已验证「找=8、工=3、作=7」，与 spec 示例一致。

## 注意

- `zhuge_qian.json` 的来源站点无明确开源许可，**仅限个人/本地使用**；若要公开发布插件，需替换为可商用或自建数据。
- 关帝灵签签诗保留**繁体**（清刊本校勘版原样），不要自动转简体。
- 康熙笔画是**康熙字典标准**，不是简体笔画；同一字简繁可能不同（如「爱」10 画 / 康熙 13 画）。
