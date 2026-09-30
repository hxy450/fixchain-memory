# 恒空的广告或占位不在多列 Grid 里生成通栏项

ID：`lesson-2bd2620e5d1ef4bb17b4` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-1b0f5d29f08f055878f4](../../../store/cases/case-1b0f5d29f08f055878f4/0c4f086a537fd33ec32d7ba71d9e1cc939751b54e61f093dcdaa6695bc541b01.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`0c4f086a537fd33ec32d7ba71d9e1cc939751b54e61f093dcdaa6695bc541b01`
