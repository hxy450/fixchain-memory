# 界面

读到的源码或规格里有窗口与系统栏、弹窗、布局尺寸、列表、共享组件、页面路由、主题、吐司和通知这类界面写法，派工、登记、计划或报告要交代它们时

## 子主题

- [公共组件与页面结构](components/index.md)（12 条）：源端有多页共用的 @Composable、经 replace / add 放进 Activity 容器的 Fragment，或者派工里有公共组件表、共享原语清单、页内等价实现、几个并行任务都要写的共享组件时
- [弹窗与弹层](dialog/index.md)（11 条）：源端有 AlertDialog、DialogFragment、XPopup、BottomSheet、setView 自定义对话框，或者派工、核查清单、弹层矩阵里写到弹窗的承载形态、bindSheet、页面内弹层时
- [吐司与通知](feedback/index.md)（3 条）：审计或计划里有直接 Toast 统一成 ToastService、调用数归零的横切行，或者把 Notification 整体推迟时
- [布局与尺寸](layout/index.md)（10 条）：源布局里有 match_parent 加水平 margin、按计数或密度分支算出的尺寸，或者派工、尺寸工单、交付报告里写到 '100%'、N vp、dp 对照、尺寸契约时
- [列表](list/index.md)（6 条）：源端列表 Adapter 有多个 viewType、在 onBindViewHolder 里改写行视图，或者计划、派工里有 LazyForEach 换 Repeat、virtualScroll、列表键契约时
- [页面路由与入口](navigation/index.md)（10 条）：目标端用 Navigation + pageMap、NavDestination、NavPathStack 装配页面，或者台账写了深链，派工、自检、交接摘要里写到页面可达、路由守卫、深链入口时
- [主题与深浅色](theme/index.md)（7 条）：计划或决策写主题「深浅双主题跟随系统」、源端按 isSystemInDarkTheme() 选套，派工要拆主题令牌任务时
- [窗口与系统栏](window/index.md)（11 条）：源端有 FEATURE_NO_TITLE、FLAG_FULLSCREEN、ImmersionBar、Scaffold innerPadding、状态栏底色，或者派工、slot 契约、前向引用、交付说明里写到沉浸、安全区避让值（statusBarHeight）、系统栏颜色时
