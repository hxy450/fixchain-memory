# 源端是 animated-vector 时，resource-mapping 记 unmappable，导出起始帧要注明

审的是：资源
触发（任一种）：
- 读到：源 res/drawable 下根元素是 <animated-vector>，<target> 的 objectAnimator 用 valueFrom / valueTo 改 pathData；写错的样子：resource-mapping 里没有这条的逐资源状态，或导出了同名静态 .svg 却没写 `unmappable`、没注明只含起始帧
适用范围：资源迁移阶段遇到 animated-vector（含 Compose AnimatedImageVector 用到的）时，资源映射表和导出的媒体
做法：
- resource-mapping 里每个 animated-vector 逐条记为 `unmappable`
- 为了引用可解析导出了起始帧静态 SVG 时，同一行写明「仅含起始帧，动画与终点帧已丢弃」，让下游在 mapping 里查得到
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- AnimatedVectorDrawable 的 android:drawable 是静态 vector：从内嵌 vector 导出的 SVG 只是起点帧（出处：Android SDK 平台资源 data/res/values/attrs.xml，AnimatedVectorDrawable 的 drawable（按应用的 compileSdk 取对应平台））
- valueTo 是动画终止值；valueType="pathType" 用于 AnimatedVectorDrawable 的 path morphing：终点帧在 objectAnimator 的 valueTo 里，静态导出时丢掉了（出处：Android SDK 平台资源 data/res/values/attrs.xml，Animator 的 valueTo、valueType（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-753b41488ff67ec1d068（Cofi）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
