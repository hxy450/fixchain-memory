# 给按值渲染的 @Builder 行写异步数据时，原位更新 @Trace 字段，不整体替换也不自赋值

审的是：代码
触发（任一种）：
- 读到：已有 @Builder 行按值取一个 @ObservedV2 实例渲染，数据在定位、加载等异步回调里才到；写错的样子：回调里 this.item = new …(…) 整体替换实例，或写 this.item = this.item 自赋值想触发刷新
适用范围：接线或修复时给已有 @Builder 行写入异步数据
做法：
- 先确认该行按值还是按引用取数；按值渲染的 @ObservedV2 实例在同一实例上逐个给 @Trace 字段赋值（this.item.name = …），不 new 新实例替换，也不写 this.item = this.item
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @ObservedV2 类中 @Trace 属性变化时，会触发该属性绑定的 UI 组件刷新：原位改 @Trace 字段才会通知到已按值传进 @Builder 的那个实例（出处：arkts-new-observedV2-and-trace.md，观察变化）
- 改成 @ObservedV2 + @Trace 但仍整体替换时依旧不显示；改为同一实例逐字段更新后显示：整体替换的新实例没有传进已渲染的 builder（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8a889aba046e2d2f1f3e（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 5、诊断；取值 2 ← 诊断
