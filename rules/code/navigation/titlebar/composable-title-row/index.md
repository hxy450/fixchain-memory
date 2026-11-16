# 照源端 @Composable 复刻的标题行组件

agent 会看到什么：产物里的标题行组件（换上的共享 @Component，或凭截断的读源码回执重写的组件）丢了源端的标题色、maxLines、weight 和尾部 IconButton，或 padding 对不上

## 规矩

- rule-9863e82cb60f｜读源码的回执被截断时，按函数名或行窗口重读被截部分再写组件，不用默认文本样式补空｜读到：批量读多个 Kotlin 源文件的回执带 `Warning: truncated output`，要复刻的 @Composable 函数体落在被截掉的部分；写错：目标组件的标题写成单个 Text 加默认的次要文字色、width('100%')，源端标题 Row 里的品牌色、maxLines、weight(1f) 和尾部 IconButton 都没有
- rule-64f36c912710｜用共享组件替换页面里已实现的片段前，逐项对比标题色、尾部图标和内边距，不一致先修组件｜写错：页面里原本自写的 @Builder 片段（带标题色、尾部图标）被换成共享 @Component 的调用，组件的标题颜色、尾部图标或 padding 和原片段不一致
