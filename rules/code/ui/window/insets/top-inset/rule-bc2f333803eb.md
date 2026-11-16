# 工具栏由子组件或内嵌子页自绘时，宿主页包住它的外层容器补 windowTopPadding

审的是：代码
触发（任一种）：
- 读到：源端顶部 inset 由根布局或子 Fragment `AppBarLayout` 的 `android:fitsSystemWindows="true"` 隐式消费，Activity 只显式处理 systemBars 的底部和左右；目标工具栏改由共享基座或内嵌子页绘制；写错的样子：宿主 NavDestination 包住它的外层容器只有 `windowBottomPadding`，没有 `.padding({ top: windowTopPadding })`
- 读到：内嵌子页头注释声明 needs_immersive_safearea=false（sub_component），工具栏自绘，避让交给宿主壳页；写错的样子：壳 NavDestination 根容器只有 windowBottomPadding 垫片，没有顶部 padding，头注释却自称做了 Layer 3
适用范围：沉浸式四层架构下，宿主 NavDestination 把工具栏基座或内嵌子页当子组件用时的顶部和底部避让
做法：
- 逐边列出四边 inset 由谁负责：经 fitsSystemWindows 隐式消费的顶部也算；基座和声明豁免的子页不自补，由宿主页负责
- 宿主页在包住子组件的外层容器写 .padding({ top: windowModel.windowTopPadding })；windowBottomPadding 加在占屏底的内容层或壳根容器（两种说法见未核实）；systemBars() 映射为这两者
- 写完 grep 本页是否同时有 windowTopPadding 和 windowBottomPadding，并对照兄弟页已登记的避让项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fitsSystemWindows：format="boolean"，为 true 时调整该 View 的 padding 给系统窗口（如状态栏）留出空间：源端顶部 inset 由带这个属性的布局隐式消费，Activity 代码里看不到，目标要有对应的顶部避让（出处：Android SDK 平台资源 data/res/values/attrs.xml，fitsSystemWindows（按应用的 compileSdk 取对应平台））
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T，默认四边都扩展：根 Navigation 四向扩展后，前景也会延伸到系统栏下，需要页面自己避让（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- 外层容器加 padding top windowTopPadding 和工具栏底色：包基座的宿主页修复后的顶部避让落点（出处：卡里修好并验证过）
- 壳根 Column 加 .padding({ top: windowModel.windowTopPadding }) 后工具栏不再叠进状态栏：承载内嵌子页的壳页修复后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端顶部 inset 由谁消费：源工程被嵌 Fragment 的布局 XML 里的 AppBarLayout、根布局的 android:fitsSystemWindows，以及 Activity 里的 setOnApplyWindowInsetsListener；逐边记下哪一处消费了哪一边；Activity 代码没处理而布局带 fitsSystemWindows="true" 的那一边，目标也要补
未核实：底部 inset 的落点两张卡说法不同：case-fe1caa813d814978decf 写加在占屏底的内容层（宿主外层容器只补顶部），case-b4a2f2d65e01a68393e3 写壳根容器同时 padding windowTopPadding 和 windowBottomPadding；顶部避让两张卡一致
来源：2 张卡，2 个应用
- case-b4a2f2d65e01a68393e3（AntennaPod）：做法第 1 步 ← 建议 2、建议 1；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
- case-fe1caa813d814978decf（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、建议 5、诊断；做法第 3 步 ← 建议 3；取值 3 ← 诊断
