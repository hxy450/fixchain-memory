# 源端“首批数据到达后默认选中首项并通知父级”迁成 @Param 子组件时只初始化一次：items 引用更新只同步高亮，不重置初始化标志、不回调第 0 项

ID：`lesson-b6abeeb9b9476b1f1f4d` · 版本：1

[本主题](index.md)

## 何时使用

页面或子组件转换阶段，把源端 Tab 列表的默认选中与父分页联动写成 ArkUI V2 的 @Param/@Monitor/@Event 逻辑时

## 适用情境

源端 Tab Fragment 只在一次性装载分类后选中首项并回调父 ViewPager，翻页时父级只调用 setSelect(position) 同步；目标子组件接收 @Param items/selectedIndex，并经 @Event 让父 Swiper 切页，父组件可能每次渲染都重新映射出 items 数组。

## 原因

把“items 变化”当作首次装载，会在父级每次重建数组时重置并回调 0，父 Swiper 随之被拉回首页，表现为翻页后数据不变、Tab 不选中；源端靠“同一项不重复回调”的防重避开了这种回环。

## 做法

1. 只在首个非空数据到达且尚无有效选中时执行默认选中与回调；之后 items 引用更新只按 selectedIndex 同步高亮，不清初始化标志，也不硬编码回调第 0 项。
2. 回调父级前比较目标索引与当前选中，相同就不回调，对齐源端的防重语义；同工程已有一次性初始化的同类 Tab 组件时按其写法对齐。

## 可选检查

- 设 selectedIndex=1 后替换 items 引用，确认不会触发回调 0。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4848068df360a077f4fa](../../../store/cases/case-4848068df360a077f4fa/098c9c703df7f4cfc8c040c472d72655404baa85ded7d417a5907e15cc84d0c0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`098c9c703df7f4cfc8c040c472d72655404baa85ded7d417a5907e15cc84d0c0`
