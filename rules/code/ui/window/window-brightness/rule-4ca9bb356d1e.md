# 亮度手势的首拖基线读当前窗口亮度，读不到回退系统设置，不写死 0.5

审的是：代码
触发（任一种）：
- 读到：源手势在 ACTION_DOWN 读 window.attributes.screenBrightness，等于 BRIGHTNESS_OVERRIDE_NONE 时回退 min(Settings.System.SCREEN_BRIGHTNESS, 255) / 255，ACTION_MOVE 再按位移增量写回窗口；写错的样子：目标手势首调把亮度基线写死为 0.5，字段注释或 TODO 写「window 无亮度读取 API」，只用了 setWindowBrightness 写入
适用范围：把源端「按下读当前亮度 → 按位移增量写回」的窗口亮度手势迁到鸿蒙窗口 API 时
做法：
- 页面就绪时预读基线（如 NavDestination 就绪回调里调一次预读方法）：先读主窗口 windowClass.getWindowProperties().brightness，取值在 (0, 1] 就用它
- 不在 (0, 1] 时（窗口没设过亮度会读到 -1.0）回退 settings.getValue(context, settings.display.SCREEN_BRIGHTNESS_STATUS)，把 0–255 的值除以 255；手势回调用预读好的基线同步算，再 setWindowBrightness(基线 + 增量)
- 常量 0.5 只在两路读取都失败时兜底，并在注释里写明是兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getWindowProperties(): WindowProperties；WindowProperties.brightness: number：同步读当前窗口属性里的亮度（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowProperties、WindowProperties.brightness）
- 窗口没有设置亮度值时 brightness 读到 -1.0（亮度跟随系统）：读到 -1.0 就要回退系统设置（出处：arkts-apis-window-i.md，WindowProperties）
- setWindowBrightness(brightness: number): Promise<void>，取值 [0.0, 1.0] 或 -1.0：写回窗口亮度，-1.0 恢复系统亮度（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowBrightness；arkts-apis-window-Window.md，setWindowBrightness）
- settings.display.SCREEN_BRIGHTNESS_STATUS，取值 0 到 255：系统设置里的屏幕亮度键（出处：鸿蒙 SDK 的 ets/api/@ohos.settings.d.ts，display.SCREEN_BRIGHTNESS_STATUS）
- getValue(context: Context, name: string): Promise<string>：异步读设置值，context 只支持 UIAbilityContext 和 ExtensionContext（出处：鸿蒙 SDK 的 ets/api/@ohos.settings.d.ts，settings.getValue）
- getValueSync(context: Context, name: string, defValue: string): string：同族接口：同步读设置值，带默认值（出处：鸿蒙 SDK 的 ets/api/@ohos.settings.d.ts，settings.getValueSync）
- BRIGHTNESS_OVERRIDE_NONE = -1.0f；screenBrightness 小于 0 表示用系统亮度，0 到 1 从暗到最亮：源端回退条件和取值范围，与鸿蒙的 -1.0 / [0, 1] 对应（出处：android.view.WindowManager.LayoutParams#screenBrightness）
- Settings.System.SCREEN_BRIGHTNESS 在 1（最小）到 255（最大）之间：源端系统亮度要除以 255 归一化（出处：android.provider.Settings.System#SCREEN_BRIGHTNESS）
未核实：卡里鸿蒙 SDK 是 6.1.1(24) / 6.0.1(21)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-ddbf301e2e83a466c644（DeepAI全能PPT）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断
