# 横屏可触发的「另起 Activity」改成同窗口 push 时，跳转前切目标方向、返回后恢复

审的是：代码
触发（任一种）：
- 读到：页面运行时用 setRequestedOrientation 切横屏，横屏界面上的入口调 startActivity 或 login(activity) 这类另起 Activity 的拦截；写错的样子：拦截直接用 NavPathStack 的 push 把按竖屏设计的页面推进同一窗口，前后都没有 setPreferredOrientation，返回后也不恢复原方向
适用范围：把安卓独立 Activity 的跳转（如登录拦截）翻译成鸿蒙 Navigation 同窗口 push、入口可在运行时横屏界面触发、目标页按竖屏设计时
做法：
- 跳转前判断当前方向；横屏时先记下要恢复（标志位），再 await mainWindow.setPreferredOrientation(window.Orientation.PORTRAIT)，然后 push 目标页
- 在原页面 NavDestination 的 onShown 回调里按记录恢复 setPreferredOrientation(window.Orientation.LANDSCAPE)，成功和取消两条返回路径都要恢复
- 依赖横屏的后续动作（如应用暂存的选择）延后到 mainWindow.on('windowSizeChange') 确认回到横屏后再执行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setPreferredOrientation(orientation: Orientation): Promise<void>：设置主窗口方向；不支持传感器旋转的设备、2in1 设备和子窗口上不生效（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setPreferredOrientation）
- Orientation.PORTRAIT = 1、Orientation.LANDSCAPE = 2：竖屏、横屏两个取值（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.Orientation）
- on(type: 'windowSizeChange', callback: Callback<Size>): void：窗口尺寸变化回调，用来确认方向已切回（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('windowSizeChange')）
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute（API 21 起；之前是无参回调）：页面重新显示（从被 push 的页面返回）时回调（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown）
- setRequestedOrientation 改的是当前这个 Activity 想要的方向：源端方向按 Activity 隔离，另起的 Activity 不继承横屏请求（出处：android.app.Activity#setRequestedOrientation）
- 跳转前切竖屏并置恢复标志，onShown 里切回横屏，windowSizeChange 回到横屏后再应用暂存动作：修法（出处：卡里修好并验证过）
针对本应用要查的：
- 目标页按哪个方向设计：源工程 AndroidManifest.xml 里目标 Activity 的 android:screenOrientation，没写就看应用默认方向和目标端页面规格；竖屏设计的就在跳转前切 PORTRAIT；没有声明时按应用默认方向处理并在交回里注明是推断
未核实：「目标页应为竖屏」在卡里是推断的（没见目标 Activity 的 screenOrientation 声明）；卡里环境是 5.0.4(16)，本机声明是 API 23；onShown 带 VisibilityChangeReason 的签名是 API 21 起
来源：1 张卡，1 个应用
- case-9407362995183cba7e5b（五星智投）：做法第 1 步 ← 建议 1、建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断；取值 6 ← 诊断
