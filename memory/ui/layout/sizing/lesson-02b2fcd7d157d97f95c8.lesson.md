# LinearLayout 以 gravity=center 摆放的 wrap_content 子项组转成 Row 时保留居中与按内容定宽，不给中间输入框 layoutWeight(1) 拉满

ID：`lesson-02b2fcd7d157d97f95c8` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把数量步进器（减号、数量框、加号）一类居中的 wrap_content 子项组翻译成 ArkUI Row 时

## 适用情境

源端 LinearLayout 设 gravity=center 与固定外边距，子项是 wrap_content 的按钮与 EditText；控件可能叠在带装饰的背景图（票券存根、竖虚线）上。

## 原因

给中间输入框 layoutWeight(1) 会把它拉满剩余宽度，两侧按钮被推到容器边缘，可能压住背景装饰；源端的居中与按内容定宽是需要同时保留的两条约束。来源中步进器把居中组改成拉伸，减号正好落在票券竖虚线上。

## 做法

1. Row 用 justifyContent(FlexAlign.Center)，子项按内容定宽（数量框按位数定宽），不给中间项 layoutWeight(1)。
2. 控件叠在装饰背景图上时，先确定装饰在图中的相对位置，再按比例留出安全区。

## 可选检查

- 在选中、未选中与最长数值状态下对照源端截图，确认没有压住装饰。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6ba16d2344b52f8fca51](../../../../store/cases/case-6ba16d2344b52f8fca51/3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`3b128ce1f45adbd905d0ce25b9396eeee973d527b0b9ccad5c9a72d571e4534f`
