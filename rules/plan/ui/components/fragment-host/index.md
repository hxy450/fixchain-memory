# 拆成共享组件或子组件的 Fragment 的宿主

agent 会看到什么：源端 Fragment 经 replace / add 放进某个 Activity 的容器、根布局带 padding 或背景、宿主 Fragment 有 ImmersionBar，派工、接线归属表或移交项按目标页结构给别的页加槽位，没写宿主和根布局的 padding、背景、沉浸由谁实现

## 规矩

- rule-083468b5d0d3｜规划 Fragment 型共享组件的嵌入接线时，按源码宿主列目标页，不给别的页加槽位｜读到：安卓源码里 Fragment 型共享组件只在某个 Activity 里经 replace / add 放进它布局的容器 id；主 Activity 布局只有 ViewPager 与 Tab 栏；写错：派工或接线归属表要求在宿主以外的页面（多为主页）生成这个组件的空槽位并登记 FWD-REF 占位，或者要求同一个组件填充多个页面的槽位，而其中有的页写不出源端宿主
- rule-cacf268e31cf｜把 fragment 内容交给共享组件时，移交项写明 fragment 根的 padding 和背景由谁实现｜读到：fragment 布局的根 LinearLayout 写了 android:padding*（或背景），承载它的 ViewPager 没有 padding；页面转换把 fragment 内容交给共享组件承载；写错：移交项只写了共享组件名和槽位，没写 fragment 根布局的 padding、背景由宿主容器还是共享组件实现
- rule-65f3618c30c4｜子组件改不到宿主的沉浸时，移交项登记宿主 Tab 顶部 padding 和状态栏图标颜色｜读到：源码宿主 Fragment 有 `ImmersionBar.with(this).titleBarMarginTop(...)`，目标把该 Tab 拆成子组件、宿主页面另由别人写；写错：转换报告只写 `immersive_safearea_skipped`，移交项里没有「宿主对该 Tab 取消顶部 padding、切换状态栏图标颜色」的交接
