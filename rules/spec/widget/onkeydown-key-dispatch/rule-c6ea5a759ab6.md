# 源端 onKeyDown 分发多类按键时，规格按键类分别写接收通道，只对核实不可达的键收缩

审的是：规格
触发（任一种）：
- 读到：源端 Activity 或 View 的 onKeyDown 同时分发音量、相机、媒体键和键盘 SPACE、DPAD、NUMPAD、FUNCTION 等键；写错的样子：规格映射行以「不投递音量键」为由把决策扩成「按键交互仅保留屏上控件路径」，没有引用读到的参考或 d.ts；同一文件的验收条目仍要求按键分发全部键位
适用范围：规格提取阶段判定源端各类按键在目标端的接收通道时
做法：
- 按键类分别写通道：键盘、DPAD、NUMPAD 等键经获焦组件的 onKeyEvent / onKeyPreIme 接收；音量、媒体等系统键可能被拦截，标为待核实
- 写平台限制时引用实际读到的参考或 d.ts 原文；只对已核实不可达的键写行为收缩，其余键位保留接收入口和验收条目，待验证项交给 Gate 裁决
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按键事件来自物理键盘、遥控器等设备，适用于所有可获焦组件；默认不可获焦的组件设 focusable(true) 后可用：键盘、遥控键在 ArkUI 的接收通道（出处：ts-universal-events-key.md，按键事件）
- 一些系统按键（如电源键）产生的事件不会传递给 UI 组件：系统键可能被拦截（出处：arkts-interaction-development-guide-keyboard.md，按键事件）
- onKeyEvent(event: Callback<KeyEvent, boolean>): T（@since 15）；onKeyPreIme(event: Callback<KeyEvent, boolean>): T（@since 12）：获焦组件接收按键的回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEvent、CommonMethod.onKeyPreIme）
未核实：物理音量、相机、媒体键在真机上是否投递到应用窗口没有核实
来源：1 张卡，1 个应用
- case-cbf23fa7a4ed42d37671（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
