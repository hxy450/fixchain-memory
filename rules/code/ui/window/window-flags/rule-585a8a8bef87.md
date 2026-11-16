# 源只有 FLAG_FULLSCREEN 时只隐藏状态栏，不用 setWindowSystemBarEnable([])

审的是：代码
触发（任一种）：
- 读到：源 Activity 只有 setFlags(FLAG_FULLSCREEN) / android:windowFullscreen，没有隐藏导航栏的标志；写错的样子：入口 Ability 里写 setWindowSystemBarEnable([])，状态栏、导航栏和导航条一起隐藏
适用范围：源 Activity 全屏旗标迁成目标主窗口的系统栏显隐时
做法：
- 写成 windowClass.setSpecificSystemBarEnabled('status', false)；'navigation' 与 'navigationIndicator' 保持显示，不调 setWindowSystemBarEnable([])
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setSpecificSystemBarEnabled(name: SpecificSystemBar, enable: boolean, enableAnimation?: boolean): Promise<void>：单独显示或隐藏某一种系统栏，enable 为 false 时隐藏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setSpecificSystemBarEnabled）
- type SpecificSystemBar = 'status' | 'navigation' | 'navigationIndicator'：可单独控制的三种系统栏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SpecificSystemBar）
- setWindowSystemBarEnable(names: Array<'status' | 'navigation'>): Promise<void>；names 设为 [] 则都不显示：传空数组会连导航栏一起隐藏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarEnable；arkts-apis-window-Window.md，setWindowSystemBarEnable）
- 改为只隐藏状态栏、保留导航条与手势条后与源端一致：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bbb49cc9ec510f04eb33（Bubble Shooter）：做法第 1 步 ← 建议 1、建议 4；取值 4 ← 诊断
