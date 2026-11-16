# 映射 Compose 的 Modifier.border 时，规格写明容器尺寸由谁定，并加盒尺寸判据

审的是：规格
触发（任一种）：
- 读到：Compose 修饰符链里有 Modifier.border(BorderStroke, shape)（或 shadow、drawBehind 这类只绘制的修饰符），盒子尺寸由调用方的 Modifier.size 决定；写错的样子：映射伪代码把描边落成没有 width / height 的 Stack(){ 内容 }.border(...)，验收条目判据只写「描边 1vp、圆角 N」，没有盒尺寸判据
适用范围：规格提取与映射阶段，为源端只绘制的修饰符确定 ArkUI 落点时
做法：
- 映射里先写明目标容器尺寸由谁决定；容器没有显式宽高时，不写成直接 .border()，写成覆盖子层画描边，或把尺寸提升到容器本身
- 验收条目加可量测的判据：描边不得改变盒尺寸，和 Android 逐边比较 bounds
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 没有定尺的容器上写 .border() 时，描边宽度计入容器测量尺寸（实测每边描边 1vp 时盒子比内容宽 2vp）：和 Compose 描边画在已定尺盒内侧、不改尺寸不同（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-77c4d0c99ad4a6486b79（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
