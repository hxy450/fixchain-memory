# 行内子项随兄弟或最高子项等高（IntrinsicSize.Min、wrap_content 行里的 match_parent）时，首选 Stretch

ID：`lesson-cb1a12afca61db08ed9a` · 版本：4

[本主题](index.md)

## 何时使用

页面转换与验证期修复阶段，遇到 Row(height(IntrinsicSize.Min)) 且子项 fillMaxHeight（常带 padding(top) 等偏移），或水平 LinearLayout 里右列 height=match_parent 跟随左侧 wrap_content 卡片等高、整行位于 ScrollView/NestedScrollView 中时

## 适用情境

行高由最高子项决定，其余子项要撑满这一高度；目标若在 Scroll 等纵向无界容器内，纵向 layoutWeight 或 height('100%') 会被撑高失控，ArkUI 也没有 IntrinsicSize 固有测量；修复时容易改成按字号行高估算的固定高度。

## 例外与边界

- 最高子项的高度是确定常量（如最小触控尺寸的按钮）时，可直接给 Row 写该显式高度，再让子项 height('100%')
- Row 本身不定高、而上层有确定高度（弹窗卡片位于定高遮罩或窗口内）时，已观察到 Stretch 子项取到外层尺寸、把行与卡片撑到父容器全高：先给行定高再让子项撑满，见 lesson-2a07020daf9a7d8a60a3；本条首选做法用于 Scroll 等纵向无界容器内的行

## 原因

Compose 的 IntrinsicSize.Min 与 Android 的 match_parent 跟随都表达“随兄弟等高”；常量高度与字体度量、内容长度脱钩，两卡仍不等高。ItemAlign.Stretch 让 Flex 内未设尺寸的子项在交叉轴拉伸到容器尺寸（enums.d.ts）；Row 不设高时先按子项定高再拉伸，d.ts 未写，以设备实测为准。删掉源码的偏移或改成居中会改变布局。

## 做法

1. 首选：同一 Row/Flex 不设高度，需要跟随的子项不设高度并写 .alignSelf(ItemAlign.Stretch)，保留源码的对齐与偏移（如 padding(top)）；实测生效即用。
2. Stretch 不适用（等高对象不在同一 Row/Flex，或实测不生效）时，在被跟随的子项 onSizeChange((_old: SizeOptions, size: SizeOptions) => …) 中取实测高度写入状态，跟随项 height 绑定该状态（首帧先按估值显示一次）；子项含可折行文本或权重时，固有高度依赖分到的宽度，不按“最高子项尺寸”估常量。
3. 给父级定高后百分比子项可以正常使用，不以“不定高父级下百分比会撑满”为由删掉源码的偏移、改成垂直居中。
4. 派修或验收时把“两卡等高”写成验收条件，不只给出“改成固定高度”这类修法。

## 可选检查

- dumpLayout 比对等高子项的 bounds 高度一致。

来源支持：4 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-47b9e1107e4e4ecd40bd](../../../../store/cases/case-47b9e1107e4e4ecd40bd/87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98.json) · 结论：recommendation:1
  卡片版本：`87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98`
- [case-83dafcc0eaba740bd9c0](../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：recommendation:3
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
- [case-bf55dc1aedfb0f2a965e](../../../../store/cases/case-bf55dc1aedfb0f2a965e/bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d.json) · 结论：diagnosis
  卡片版本：`bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d`
- [case-eac486f2e51124dda2cb](../../../../store/cases/case-eac486f2e51124dda2cb/0a1a8283f781cffed930c039434e8c25cb0d57f2664856dcb44110812e1fb18c.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`0a1a8283f781cffed930c039434e8c25cb0d57f2664856dcb44110812e1fb18c`
