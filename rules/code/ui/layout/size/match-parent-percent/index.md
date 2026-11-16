# match_parent 子项转成 '100%' 的写法

agent 会看到什么：读到列表项、网格项或 FrameLayout 叠层里 layout_width / layout_height="match_parent" 的子项，常带同轴的 android:layout_margin；产物里 .width('100%') / .height('100%') 漏写，或和同轴的 .margin 叠写

## 规矩

- rule-caedc2793174｜源项 match_parent 加 layout_margin 时，边距交给父容器 padding，不叠 margin｜读到：列表项或网格项布局的根 android:layout_width="match_parent"，同时带 android:layout_margin；写错：卡片写成 .width('100%') 再叠 .margin(…)，宽变成格宽 + 2×margin 而右溢
- rule-b94a5d7465c3｜叠层子层 layout_width=match_parent 时，Stack 子节点写 .width('100%')｜读到：条目布局用 FrameLayout 叠放封面和底部信息条，信息条 android:layout_width="match_parent"、android:layout_gravity="bottom"；写错：Stack 里对应的 Row 只写了 .height / .padding / .justifyContent(FlexAlign.Center)，没有 .width('100%')，条带按内容宽度收窄
- rule-dae0e1f7834f｜match_parent 加水平 margin 时用 calc 宽度或父级 padding，不写 100% 宽｜读到：android:layout_width="match_parent"（或 0dp 两端约束到 parent）加 layout_marginHorizontal / marginStart/End / marginLeft/Right / layout_margin；写错：同一链里 .width('100%') 又有水平 .margin({ left/right/start/end … }) 或 .margin(N) 简写
- rule-e319d3601218｜layout_width=match_parent 转宽度：有左右 margin 用 calc 扣除，文本条写满宽｜读到：layout_width="match_parent" 同时有 layout_marginHorizontal（或 marginStart、marginEnd）；写错：目标写 .width('100%') 再加左右 .margin(...)，组件超出父容器
