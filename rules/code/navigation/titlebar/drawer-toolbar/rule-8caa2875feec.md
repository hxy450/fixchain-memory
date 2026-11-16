# 源端导航图标是 DrawerArrowDrawable 时，目标按 position 插值画汉堡↔箭头，不切两张图透明度

审的是：代码
触发（任一种）：
- 读到：源端用 ActionBarDrawerToggle / DrawerArrowDrawable，onDrawerSlide 里写 position（汉堡到箭头的动画）；写错的样子：导航位用汉堡和返回箭头两张图按 .opacity(...) 交叉淡化，没有和抽屉开合共用的 position，也没有指示器启用态
适用范围：目标用自绘标题栏加 SideBarContainer 复刻源端抽屉指示器时
做法：
- 导航位写一个自绘的汉堡↔箭头组件，按 position（0 汉堡、1 箭头）插值同一套线条，不用两张图切透明度
- position 由抽屉开合驱动：开合变化时用 syncState(opened) 写入；写前核对源端是否经 onDrawerSlide 写 position
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onChange(callback: (value: boolean) => void): SideBarContainerAttribute：侧栏显示状态变化完成时回调，可用来调 syncState(opened)；SideBarContainer 没有滑动进度回调（出处：鸿蒙 SDK 的 ets/component/sidebar.d.ts，SideBarContainerAttribute.onChange）
- 返修加 DrawerArrowController / DrawerArrowToggle，按 controller.syncState(opened) 同步：汉堡↔箭头指示器的落法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端 position 是怎么写入的：源工程抽屉 Fragment 或 Activity 里 ActionBarDrawerToggle 的构造和 onDrawerSlide 覆写；看 onDrawerSlide 里是否按 slideOffset 写 position，以及 setDrawerIndicatorEnabled 在哪些路径被调；照此决定目标 position 的来源
未核实：SideBarContainer 只回调显示状态变化完成，拖动过程中 position 随滑动插值在目标上怎么取，卡里没写清；DrawerArrowDrawable 和 ActionBarDrawerToggle 是 appcompat 库代码，本机只有编译产物，position 的写法按卡
来源：1 张卡，1 个应用
- case-aa81c21ff3eaca257ba4（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 2 ← 诊断
