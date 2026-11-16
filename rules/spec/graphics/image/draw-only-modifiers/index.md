# Compose 只绘制的修饰符（Modifier.shadow、Modifier.border）的映射

agent 会看到什么：读到 Compose 修饰符链里的 Modifier.shadow(elevation: Dp)、Surface 的 elevation、Modifier.border(BorderStroke, shape) 这类只绘制的修饰符；规格的阴影配方把 dp 数直接填进 ShadowOptions，或描边落在没有宽高的 Stack 上、验收没有盒尺寸判据

## 规矩

- rule-92b6b2a24310｜规格给 ShadowOptions 写阴影配方时，写明字段单位 px 并在公式里写 vp2px 换算｜读到：源端阴影是 dp 量纲：Compose Modifier.shadow(elevation: Dp)、Surface 的 elevation: Dp，或 android:elevation；写错：规格里阴影配方写成 { radius: 2e, offsetY: e } 这类把 dp 数直接填进 ShadowOptions 字段的式子，没写单位和 vp2px 换算
- rule-a2606d2df66f｜映射 Compose 的 Modifier.border 时，规格写明容器尺寸由谁定，并加盒尺寸判据｜读到：Compose 修饰符链里有 Modifier.border(BorderStroke, shape)（或 shadow、drawBehind 这类只绘制的修饰符），盒子尺寸由调用方的 Modifier.size 决定；写错：映射伪代码把描边落成没有 width / height 的 Stack(){ 内容 }.border(...)，验收条目判据只写「描边 1vp、圆角 N」，没有盒尺寸判据
