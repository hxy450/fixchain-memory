# Stack 中覆盖在可点击兄弟之上、自身不处理点击的层显式设 HitTestMode.Transparent，不假设它不参与命中

ID：`lesson-4a4f8d845a204ffa244b` · 版本：7

[本主题](index.md)

## 何时使用

界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 时；为还原 z 序重排子节点，或调整 Stack 对齐与上层几何后

## 适用情境

源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器。也包括按钮之上叠有同尺寸、不可点击的自绘进度环或加载圈（源端触摸落到下层按钮），目标 Stack 保留 z 序而点击只挂在最底层图片上。

## 例外与边界

- 上层本身绑定了点击或滑动手势（如侧滑行的内容层）：不改整层命中模式，把调整限定在按钮热区
- 源 Box 中按内容定高、贴底或贴顶的栏：保持自身尺寸直接锚定，不套全屏定位壳
- 页面级全屏遮罩与一次性全屏动效层：只在需要时作为根 Stack 条件子节点挂载

## 原因

ArkUI 中没有 onClick 的容器同样参与命中测试，各值以 enums.d.ts 的 HitTestMode 注释为准：Default 自身与子节点响应、挡住被它遮住的节点；Block 只自身响应、挡住子节点与被遮节点；Transparent 自身与子节点响应、放行被遮节点；None 自身不响应、子节点照常响应。全尺寸上层沿用 Default 会吞掉下层点击，hilog 表现为 Touch test result is empty。为还原源端 z 序重排子节点后，原先“浮层设 Transparent”的标注会落在错误的层上；调整对齐或几何会放大覆盖区。

## 做法

1. 按最终声明顺序逐层检查：位于可点击兄弟之上、覆盖其区域且自身不处理点击的容器，显式写 hitTestBehavior(HitTestMode.Transparent)；重排子节点或修改对齐与几何后重新核对。
2. 按钮上叠的进度环、加载层同样逐个决定命中：纯展示节点设 Transparent，或把 onClick 挂在整个 Stack 容器上，不只挂在最底层图片。
3. 叠层确需全屏布局容器时给它设 Transparent，再实测下层滚动与横滑仍能响应；可检索同一 Stack 内 width('100%').height('100%') 的兄弟节点逐一确认 hitTestBehavior 或 onClick 落位。

## 可选检查

- 调整 Stack 对齐、上层几何或新增层后，对被覆盖区域的按钮逐个实际点击（不只看节点 clickable 与 bounds），检查 hilog 有无 Touch test result is empty。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-57a208ad2e9541272704](../../../store/cases/case-57a208ad2e9541272704/8d2a2903f578b837bbe4fbae23c3df7cbdd8897003895ed0d906609949fd4c6d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`8d2a2903f578b837bbe4fbae23c3df7cbdd8897003895ed0d906609949fd4c6d`
- [case-8809177953953374a01e](../../../store/cases/case-8809177953953374a01e/0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f.json) · 结论：recommendation:1, recommendation:2
  卡片版本：`0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f`
- [case-9b8bac5680e58daada3a](../../../store/cases/case-9b8bac5680e58daada3a/07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591.json) · 结论：recommendation:2
  卡片版本：`07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591`
