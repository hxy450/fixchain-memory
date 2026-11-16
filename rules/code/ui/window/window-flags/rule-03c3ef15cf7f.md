# 源端只有 FLAG_FULLSCREEN 时，页面根容器不四向 expandSafeArea 铺进挖孔和导航区

审的是：代码
触发（任一种）：
- 读到：源 Activity 只有 setFlags(FLAG_FULLSCREEN) / android:windowFullscreen，没有延伸到导航栏下的标志；写错的样子：页面根 Stack 或背景 Image 上写 .expandSafeArea([SafeAreaType.SYSTEM, SafeAreaType.CUTOUT]) 不限边，背景和内容铺进挖孔边和导航区
适用范围：源端全屏旗标只隐藏状态栏的页面，迁成 ArkUI 页面根容器时
做法：
- 去掉根容器和背景上的四向 expandSafeArea，页面背景和内容都不向导航区、挖孔边延伸；内容放进按应用内容区定宽高与偏移的容器
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T；默认 types [SYSTEM, CUTOUT, KEYBOARD]，edges [TOP, BOTTOM, START, END]：不传 edges 时四个方向都延伸（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- 三页改为内容放进按内容区定宽高与偏移的 Stack 后与源端一致：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bbb49cc9ec510f04eb33（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；取值 2 ← 诊断
