# elevation 高程阴影

agent 会看到什么：源端的 elevation 阴影（Modifier.shadow(elevation = …)、Surface 的 elevation、android:elevation 配 outlineProvider），对应目标组件上的 .shadow(ShadowOptions | ShadowStyle) 和共享的高程映射

## 规矩

- rule-a22523139fe8｜elevation 配 outlineProvider=background 且无背景时，目标不加 .shadow｜读到：同一节点写了 android:elevation 和 android:outlineProvider="background"（或没写 outlineProvider），且没有 android:background；写错：目标组件按 elevation 直译加了 .shadow({ radius: …, offsetY: … })
- rule-0b4df8919907｜dp 高程落到 .shadow 时，radius 和 offset 先 vp2px 换算再填｜读到：Compose `Modifier.shadow(elevation = 3.dp, shape = …)`，或 Surface 类容器的 `elevation: Dp` 参数（内部 .shadow(elevation = elevation, …)）；写错：`.shadow({ radius: …, offsetY: … })` 里直接写源端 dp 数值、this.elevation / 2 或字面数字，没有经过 vp2px
- rule-88eb3b337398｜dp 高程阴影不用预置 ShadowStyle，经共享映射写 ShadowOptions，全工程只留一条通路｜读到：Modifier.shadow(elevation = 3.dp, shape = …)，或规格、派工里写「shadow 3dp」这类高程阴影；写错：.shadow(ShadowStyle.OUTER_DEFAULT_XS) 等预置样式替代高程阴影
- rule-03f1f66b7ddc｜各处 elevation 阴影集中到一个按 elevation 换算的共享函数，不在页面另写近似常量｜读到：源端几处元素各自带不同的 elevation（如 elevation = 1.dp、2.dp、3.dp）；写错：页面里另写与 elevation 无关的阴影常量，`.shadow({ radius: 常量, offsetY: 1 })`，注释写「视觉近似」，不同 elevation 的元素共用同一组数值
