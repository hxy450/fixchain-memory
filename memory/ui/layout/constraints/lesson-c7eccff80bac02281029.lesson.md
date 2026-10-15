# RelativeLayout 设了 android:gravity 时整组非 GONE 子项按 gravity 平移，alignParentTop 子项也会居中

ID：`lesson-c7eccff80bac02281029` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把带 android:gravity 的 RelativeLayout 映射为 ArkUI 容器对齐时

## 适用情境

源 RelativeLayout 设 gravity=center_vertical 等非 start|top 值，容器尺寸大于子项包围盒（match_parent 或固定尺寸），子项同时声明 alignParentTop/alignParentStart 等对齐规则，可能用 android:ignoreGravity 排除某个子项；映射参考只写“容器级 gravity 无直接对应”。

## 例外与边界

- 容器在该轴上为 wrap_content 时，子项包围盒与容器一样大，gravity 不产生偏移，按子项规则排布即可

## 原因

RelativeLayout.onMeasure 先按规则排好子项，再按 gravity 计算整组包围盒的偏移，并平移所有非 GONE（含 INVISIBLE）且不是 ignoreGravity 指定者的子项（RelativeLayout.java）；凭记忆认定“有 align 规则的子项不受 gravity 影响”而把容器写成 TopStart，源端居中的标题就贴顶了。

## 做法

1. 先按 alignParent*、margin 排出组内相对位置，再把整组按容器 gravity 定位：ArkUI 侧用容器内容对齐让整组居中（如 Stack.alignContent(Alignment.Start) 对应 center_vertical|start，或 Column.justifyContent(FlexAlign.Center)），不给单个子项各自对齐。
2. 包围盒与平移都只看非 GONE 子项：INVISIBLE 子项同样参与并随组平移（目标写 Visibility.Hidden 保留占位），GONE 子项不参与。
3. 解析 android:ignoreGravity 指向的 id：该子项不随组平移，按自身 alignParent*/margin 单独定位（如外层 Stack 中 position）；它对包围盒的贡献按 RelativeLayout.onMeasure 的条件计算（有竖向 gravity 时计入左上边界，有横向 gravity 时计入右下边界）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4e1ab457a4fa55aaeb29](../../../../store/cases/case-4e1ab457a4fa55aaeb29/11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9.json) · 结论：diagnosis, recommendation:2
  卡片版本：`11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9`
