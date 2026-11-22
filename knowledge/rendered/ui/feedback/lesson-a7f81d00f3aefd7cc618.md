# Compose M3 不传 progress 的进度指示器与 PullToRefreshBox 指示器，不用 ArkUI 默认组件代替

## 何时使用

界面实现阶段（共享组件与页面），以及规格提取写转换决策时，把 Compose Material3 带默认动态视觉的进度与下拉刷新组件映射到 ArkUI 时

## 适用情境

源端 Compose 用不传 progress 的 LinearProgressIndicator/CircularProgressIndicator（加载条可能以 zIndex 叠放在内容上）或 PullToRefreshBox 默认指示器；目标 ArkUI Progress 只显示定值，LoadingProgress 是环绕点动画，Refresh 默认用系统指示器并把内容往下推。

## 原因

不传 progress 是持续动画，Progress 写成 value 0、30、50 就是一根静止条，换成 LoadingProgress 形状也不同；Refresh 默认指示器与 M3 指示器外观不同，下拉时内容随之下移。共享组件写成近似后，页面又各自内联近似版本，或把“无等价”注释当作既有决策沿用。

## 做法

1. 转换前确认是定值还是不定进度；不定进度在共享组件里用 Canvas 加逐帧回调（如 displaySync）复刻源端动画，保留叠放层级（zIndex），不推挤内容。
2. PullToRefreshBox 的映射写明指示器外观与“内容不随下拉移动”：Refresh 隐藏系统指示器、自绘指示器并抵消内容位移，保留源端的包裹范围。
3. 页面源码出现共享组件名时，先读该组件在源端的定义，再复用目标共享件，不在页面里内联近似版本；先例是静止条或写着“无等价”的，按源端定义纠正。

## 可选检查

- 生成后检索 Progress({ value: 常量、LoadingProgress 与无自定义 builder 的 Refresh(，逐处对照源端组件

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 androidx.compose.material3:material3-android 1.4.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Progress 按 ProgressOptions.value 显示当前进度：value 不写时为 0，取值范围 [0, total]，小于 0 按 0、大于 total 按 total、非法值按默认值处理；total 不写时为 100；value 写成常量时进度条是静止的
- 〔适用情境 / 原因〕LoadingProgress 是系统自带外观的加载动效组件，enableLoading 不写时为 true（显示动画）；动画不显示时组件仍然占位
- 〔做法第 1 步〕DisplaySync 用 on('frame') 注册的回调在 start() 之后才随帧触发，stop() 之后停止触发
- 〔适用情境 / 做法第 2 步〕从 API 11 开始，Refresh 的子组件默认跟随手势下拉而下移
- 〔做法第 2 步〕Refresh 没设 builder 或 refreshingContent 时，下拉位移靠更新子组件的 translate 实现，子组件自己设的 translate 不生效；设了 builder 或 refreshingContent 时，改为更新子组件相对 Refresh 的位置实现位移
- 〔做法第 2 步〕Refresh.pullDownRatio 取 [0, 1]：0 不跟随手势下拉，1 等比例跟随，小于 0 按 0、大于 1 按 1；不设或设为 undefined 时用动态跟手系数，下拉距离越大系数越小
- 〔做法第 2 步〕Refresh.onOffsetChange 回调给出的下拉偏移单位是 vp
- 〔做法第 2 步〕material3 1.4.0 的 PullToRefreshDefaults：触发刷新的位置阈值 PositionalThreshold 为 80dp，指示器最大下拉距离同为 80dp，指示器容器色取 colorScheme.surfaceContainerHigh；应用没有另传 threshold、颜色时按这些值
