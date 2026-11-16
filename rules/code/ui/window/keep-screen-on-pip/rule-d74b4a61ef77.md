# 源码在校验前置位 FLAG_KEEP_SCREEN_ON 时，目标按源码的置位和清除位置复刻

审的是：代码
触发（任一种）：
- 读到：源码在前置操作成功后、范围或参数校验之前 addFlags(FLAG_KEEP_SCREEN_ON)，收尾段第一步 clearFlags(FLAG_KEEP_SCREEN_ON)，校验失败提前返回的路径不清除；写错的样子：目标把常亮置位（setWindowKeepScreenOn(true) 或包它的方法）挪到成功路径才做，注释或源码笔记把源时序称为源缺陷、越界泄漏
适用范围：一比一复刻时，源码副作用的置位和清除时序看似有缺陷（以窗口常亮标志为例）
做法：
- 在源 addFlags(FLAG_KEEP_SCREEN_ON) 的同一位置调 windowClass.setWindowKeepScreenOn(true)，在源 clearFlags 的同一位置调 setWindowKeepScreenOn(false)；提前返回的路径照源不清除
- 认为源时序应修正时写进决策台账交裁决，代码里不自行收敛
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowKeepScreenOn(isKeepScreenOn: boolean): Promise<void>：window.Window 设置屏幕常亮，true 常亮、false 取消（@since 11）（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.Window.setWindowKeepScreenOn）
- setKeepScreenOn(isKeepScreenOn: boolean): Promise<void> 自 9 起废弃，改用 setWindowKeepScreenOn：旧接口，不要新写（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.Window.setKeepScreenOn）
- FLAG_KEEP_SCREEN_ON = 0x00000080：窗口对用户可见期间保持屏幕常亮：源端标志的含义（出处：android.view.WindowManager.LayoutParams#FLAG_KEEP_SCREEN_ON）
未核实：卡里修复用的方法写作 setKeepScreenOn(true)，看不出是窗口接口（自 9 起废弃）还是自己的包装
来源：1 张卡，1 个应用
- case-7d097177e497ea9e202c（MifareClassicTool）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
