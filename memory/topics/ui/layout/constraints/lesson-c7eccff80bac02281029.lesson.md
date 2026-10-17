# RelativeLayout 设了 android:gravity 时，测量末尾把全部子项（ignoreGravity 除外）作为一组按 gravity 平移：alignParentTop 的子项同样随 center_vertical 居中，目标让整组居中并保留组内相对偏移

ID：`lesson-c7eccff80bac02281029` · 版本：2 · 阶段：execute · 主题：[ui/layout/constraints](index.md)

概要：RelativeLayout gravity 平移整组子项

信号：`RelativeLayout`, `android:gravity`, `center_vertical`, `alignParentTop`, `ignoreGravity`, `alignContent`, `FlexAlign.Center`

## 何时使用

界面实现阶段，把带 android:gravity 的 RelativeLayout 映射为 ArkUI 容器对齐时

## 适用情境

源 RelativeLayout 设 gravity=center_vertical 等，子项同时声明 alignParentTop/alignParentStart 等对齐规则；映射参考只写“容器级 gravity 无直接对应”。

## 原因

RelativeLayout.onMeasure 先按规则排好子项，再按 gravity 计算整组包围盒的偏移并平移所有可见子项；凭记忆认定“有 align 规则的子项不受 gravity 影响”而把容器写成 TopStart，源端居中的标题就贴顶了。

## 做法

1. 先按 alignParent*、margin 排出组内相对位置，再把整组按容器 gravity 定位：ArkUI 侧用容器内容对齐让整组居中（如 Stack.alignContent(Alignment.Start) 对应 center_vertical|start，或 Column.justifyContent(FlexAlign.Center)），不给单个子项各自对齐；拿不准时与源端截图对照。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [expandSafeArea 非避让，前景按避让区补内距](../immersion/lesson-a8452bfea5d42d3dcae3.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4e1ab457a4fa55aaeb29](../../../../../store/cases/case-4e1ab457a4fa55aaeb29/11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9.json) · 结论：diagnosis, rec-bfc215850c
  卡片版本：`11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9`
