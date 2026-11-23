# 恒空的广告或占位不在多列 Grid 里生成通栏项

## 何时使用

界面实现阶段，把含广告跨列的 RecyclerView 多类型网格转成 ArkUI Grid，决定 no-op 占位是否生成 GridItem 与跨列配置时；规格把广告定为 no-op 时

## 适用情境

源端 GridLayoutManager 多列，spanSizeLookup 让广告项跨满一行，广告按固定间隔插入（可能紧跟奇数个内容项）；目标端广告是恒空的桩（零高容器）。

## 原因

通栏项即使高度为 0 也独占一行，插在奇数个内容项之后会让前一项独占一行、留下空格；纵向列表“空容器零高塌陷”的先例不适用于多列宫格。

## 做法

1. 目标端占位恒为空时，ForEach 只渲染内容项，不为占位生成 GridItem；数据层的占位可以保留，供点击时过滤后重算下标。
2. 必须保留跨列项时，按插入规则推一遍它落在哪一列，确认不会让前一行缺格。
3. 规格或全局决策把广告定为 no-op 时，对 Grid、WaterFlow 等多列容器单独写明占位是否参与排布。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕2 列 Grid 里占满一整行的 GridItem 即使高度为 0 也独占一行、强制换行：它前面是奇数个内容项时，最后一个内容项独占一行，旁边留出半行空格
- 〔做法第 2 步〕GridLayoutOptions 的 irregularIndexes 只对只设了 rowsTemplate 或 columnsTemplate 之一的 Grid 起作用；没设 onGetIrregularSizeByIndex 时，列在 irregularIndexes 里的 GridItem 默认占垂直滚动 Grid 的一整行（水平滚动时一整列）
