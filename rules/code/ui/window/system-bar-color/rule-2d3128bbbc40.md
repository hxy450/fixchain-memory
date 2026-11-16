# 源端非手势导航时给导航栏着色的，入口按 TYPE_SYSTEM 底部高度判断后着色

审的是：代码
触发（任一种）：
- 读到：源 Activity 里 if (!isUsingGestures) setNavigationBarColor(…) 给三键导航栏着色；写错的样子：EntryAbility 的 setWindowSystemBarProperties 里 navigationBarColor 恒为 '#00000000'，没有导航方式判断
适用范围：迁移入口窗口的系统栏着色、源端按导航方式区分时
做法：
- 取 win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM)，usingGestures = bottomRect.height === 0；非手势时 setWindowSystemBarProperties({ navigationBarColor: <源端颜色含透明度> })
- 在 win.on('avoidAreaChange', …) 里重新判断并着色，响应导航方式切换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- navigationBarColor?: string：SystemBarProperties 的导航栏底色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.navigationBarColor）
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设置系统栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- AvoidArea.bottomRect: Rect：避让区的底部矩形，height 为 0 表示底部没有系统栏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，AvoidArea.bottomRect）
- on(type: 'avoidAreaChange', callback: Callback<AvoidAreaOptions>): void：避让区变化回调（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('avoidAreaChange')）
针对本应用要查的：
- 源端三键导航时的导航栏颜色：源工程 Activity 代码里 setNavigationBarColor 的参数（主题色、copy(alpha = …)）；算出 ARGB 写成 '#AARRGGBB' 填进 navigationBarColor
来源：1 张卡，1 个应用
- case-01833db0536ba02ed2ce（Cofi）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 诊断、建议 2
