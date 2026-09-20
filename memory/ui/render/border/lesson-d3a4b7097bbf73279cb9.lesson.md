# Compose 纯绘制描边落到 ArkUI 时，无显式宽高的容器不得直接 .border()：描边会计入测量

ID：`lesson-d3a4b7097bbf73279cb9` · 版本：1

[本主题](index.md)

## 何时使用

规格映射与界面实现阶段，把 Compose Modifier.border 等 draw-only 修饰符落到尺寸由内容决定的 ArkUI 容器（Stack/Column）上时

## 适用情境

源 border 由 Modifier.border(BorderStroke, shape) 在调用方已定尺寸的盒内侧绘制、不改测量尺寸；目标容器自身不设 width/height，尺寸由 @BuilderParam 内容决定。

## 例外与边界

- 目标容器自身已有显式 width/height（此时 .border 在盒内绘制不改尺寸）

## 原因

ArkUI .border 在无定尺容器上计入容器测量：高亮卡 Stack 172×250 内含 Column 170×249，Android 170×250，第 2 张卡左沿偏 2.3vp。映射作者知道 Compose border 是内侧描边（mapping :228）却把 §5 伪代码写成无宽高 `Stack(){content}.border(...)`；工程 pitfalls P-20 反而推荐「描边画在由内容定大小的容器上」。

## 做法

1. 映射/规格：先写明目标容器尺寸由谁决定；容器无显式宽高时改为 overlay 子层（onSizeChange 定尺 + position({x:0,y:0}) + hitTestBehavior None）或把尺寸提升到容器本身，并在 AC 里加可量测判据（描边不得改变盒尺寸）。
2. 实现：写 .border() 前检查该节点是否有显式 width/height；没有就把「内容盒 = 描边盒」的预期写进注释，自检对一次 dumpLayout bounds。
3. 维护材料：pitfalls P-20 应补注无定尺容器的 .border 计入测量，需 overlay 或显式尺寸。

## 检查

- dumpLayout：带描边容器的 bounds 与其内容子项 bounds 逐边相等；与 Android 同一卡片宽高逐边比较。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-77c4d0c99ad4a6486b79](../../../../store/cases/case-77c4d0c99ad4a6486b79/27e777a50597a4025558e4e2acc40fb81182444305b104b7c319f379abb5735f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`27e777a50597a4025558e4e2acc40fb81182444305b104b7c319f379abb5735f`
