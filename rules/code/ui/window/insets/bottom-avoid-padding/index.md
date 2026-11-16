# 底部避让 padding 所在的容器层

agent 会看到什么：交回的根容器自带背景色、height('100%') 并写 .padding({ bottom: 底部避让 })，而延伸到屏幕底边的是里面背景色不同的 layoutWeight(1) 内容层

## 规矩

- rule-d3ed4dbf8f8a｜底部避让 padding 加在占据屏幕底边的那层容器上，不加在背景色不同的根容器上｜写错：根容器（自带背景色、height('100%')）上写 .padding({ top: 顶部避让, bottom: 底部避让 })，而延伸到底边的是它里面背景色不同的 layoutWeight(1) 内容层，底部避让区被根容器的背景色填充
- rule-d4f8360eaf6b｜全屏页的前景避让逐边落实：伸到窗口底边的内容层补 windowBottomPadding｜读到：页面规格标 needs_immersive_safearea=true、按 arkts-immersive-safearea 四层架构实施；Layer 3 写明标题栏补 windowTopPadding、贴底内容补 windowBottomPadding；写错：只给标题栏外层加了 .padding({ top: windowTopPadding })，伸到窗口底边的根 Column 只有 width/height 100%、没有底部 padding；报告 immersive_safearea_implemented 只列了顶部一处
- rule-b56ad4d2ee95｜开启 setWindowLayoutFullScreen 时逐页核对贴底那一层消费了底部避让｜写错：入口在 EntryAbility 里调了 setWindowLayoutFullScreen(true)，但有 NavDestination 页只消费了 windowTopPadding，贴底那一层没有 windowBottomPadding
