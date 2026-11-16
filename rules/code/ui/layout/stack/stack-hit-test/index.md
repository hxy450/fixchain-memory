# Stack 上层的点击命中

agent 会看到什么：读到 FrameLayout 里较晚声明、本身不可点击的 match_parent 容器或进度环叠在按钮上；产物里 Stack 上层子节点没写 .hitTestBehavior(HitTestMode.Transparent)，onClick 只挂在底层

## 规矩

- rule-5d0daf9e603f｜Stack 里盖在可点击兄弟上方、自身不处理点击的层，显式写 hitTestBehavior(Transparent)｜读到：源 `FrameLayout` 里较晚声明（z 序更高）的 `match_parent` 容器本身不可点击（没有 `android:clickable`、没有点击监听），却覆盖较早声明的按钮组或底部控制行；写错：对应 `Stack` 的上层子容器是 `.width('100%').height('100%')`，没有 `.hitTestBehavior(HitTestMode.Transparent)`；或者为还原 z 序重排后，`Transparent` 还留在原来那几个「浮层」上、没跟到现在位于上方的层
- rule-f21c4cb10084｜按钮上叠了不可点的进度环时，上层设 Transparent 命中或把 onClick 挂到 Stack 上｜读到：源布局里可点的按钮之后声明了没有 id、没有 android:clickable 的自绘进度环或 ProgressBar，叠在按钮上；写错：目标 Stack 里 onClick 只挂在最底层 Image 上，同尺寸（width('100%').height('100%')）的进度环、LoadingProgress 没写 hitTestBehavior
- rule-33154f4fef0b｜叠在 Scroll/Swiper 上的全屏叠加容器，设 hitTestBehavior Transparent｜读到：Compose `Box(fillMaxSize)` 里，在可滚动内容（含轮播）之上叠放悬浮栏；写错：Stack 里叠在 Scroll / Swiper 之上、`.width('100%').height('100%')` 的容器（如 Column + `Blank().layoutWeight(1)`）没有 `.hitTestBehavior(HitTestMode.Transparent)`
- rule-35f53edaedc2｜Stack 里可点击控件之后有盖住它的全屏同级节点时，壳设 Transparent 或控件提高 zIndex｜读到：Compose Box 里返回按钮（IconButton 一类）和后面的子项叠放，后面的子项只占自己的区域、不和按钮重叠；写错：目标 Stack 里返回按钮之后声明了 width('100%').height('100%') 的同级容器，没有 hitTestBehavior(HitTestMode.Transparent)，按钮也没有更高的 zIndex
- rule-6f571b3aad93｜弹层根容器含可交互子节点时，不设 HitTestMode.Block，保持 Default｜读到：源端模态浮层由全屏 `Modifier.fillMaxSize()` 加空 `clickable {}` 的拦截层（防穿透）、半透明遮罩 `clickable` 关闭、居中卡片三层组成；写错：目标弹层根 `Stack` 上写了 .hitTestBehavior(HitTestMode.Block)，而它的子树里有 onClick、Scroll、Slider、Button 等交互控件
- rule-70f664819876｜安卓叠放层吞触摸时，目标逐节点写 hitTestBehavior，不靠空 onClick 和缺省值｜读到：叠在列表上的条体样式或布局写 android:clickable="true"，条体自己消费触摸、不下穿；写错：目标条体只写空 .onClick(() => {})（注释称吞掉触摸），没有 hitTestBehavior；承载它的叠放 Stack 是 HitTestMode.Transparent，点条体时下层列表的 onTouch 也触发
- rule-f6b22e977b75｜给自定义组件实例加 margin 等通用属性时，同时写 hitTestBehavior｜写错：自定义组件实例上直接写 .margin({ top: ... }) / .padding / .position，没有 .hitTestBehavior，提示条显示期间挡住其下工具栏
