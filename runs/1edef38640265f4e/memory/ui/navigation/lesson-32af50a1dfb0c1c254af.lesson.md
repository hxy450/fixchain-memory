# 源页面由点击回调经 ViewModel 副作用导航时，逐个导航出口在目标 onClick 落实际跳转与参数，不留只含注释的回调

ID：`lesson-32af50a1dfb0c1c254af` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与返修阶段，为页面中的卡片、列表项、空状态按钮编写点击处理与跨页跳转时

## 适用情境

源 Fragment 的点击回调触发 ViewModel 副作用（如 OpenTripDetail(id)、OpenCreateTrip），再由副作用处理函数调 findNavController().navigate 并带 bundleOf 参数；目标页面自行用 router 或 NavPathStack 跳转。

## 原因

导航写在副作用处理函数里，只对齐可见 UI 元素时容易漏掉“点击→跳转”；回调体只有 // Navigate… 注释时，页面看似接了事件，按 TODO: 检索也发现不了，对齐报告却记成完成。来源中生成期首页卡片与待办都没有 onClick；返修轮读到了源码的两条副作用，仍只写注释占位并报告已对齐。

## 做法

1. 从源端副作用处理函数反查每个 effect 的触发者，列出“可交互元素 → 目标页 + 参数”清单（例如卡片、整项待办 → 详情页(id)，空状态创建按钮 → 编辑页），逐项写成实际跳转调用，并确认目标页已登记或已在导航映射中。
2. 回调体不写只有注释的占位；当前确实无法实现时按工程的移交约定登记，并如实报告未完成。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-be539ffd7751410d8ad6 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`9bce8a8274927a0c7402f403e85eb53e967d4fc71e3bb835471c52a05b07eed7`
