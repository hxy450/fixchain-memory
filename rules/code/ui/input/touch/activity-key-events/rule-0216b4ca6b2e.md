# 源端是 Activity 级 onKeyDown 时，.onKeyEvent 挂在页面根节点，不挂在要先获焦的子组件上

审的是：代码
触发（任一种）：
- 读到：Activity 覆写 onKeyDown 或 dispatchKeyEvent 处理 KEYCODE_DPAD_*、KEYCODE_MENU 等按键，不依赖哪个 View 持有焦点；写错的样子：.onKeyEvent 挂在 Canvas 或自绘子组件上，只加了 .focusable(true)，页面根（NavDestination 或 @Entry 根组件）上没有 .onKeyEvent
适用范围：源端 Activity 级硬件按键回调，迁到 Navigation 下的 NavDestination 或 @Entry 页面时
做法：
- 把 .onKeyEvent((event: KeyEvent) => { … return true/false }) 挂在 NavDestination（或 @Entry 根组件）上，回调里按 event.type === KeyType.Down 和 event.keyCode 分派到原来的处理函数
- 子组件上的 .onKeyEvent 去掉或不再承担页面级按键；子组件即使获焦，事件也会沿焦点链冒泡到页面根
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onKeyEvent(event: Callback<KeyEvent, boolean>): T（@since 15，另有返回 void 的旧签名）：CommonMethod 上的按键回调，返回 true 表示已消费（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEvent）
- declare class NavDestinationAttribute extends CommonMethod<NavDestinationAttribute>：NavDestination 继承 CommonMethod，有 onKeyEvent（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute）
- 按键事件沿获焦链从叶子到根逐一发送，子组件不处理就冒泡给父组件；onKeyEvent 只在绑定组件处于获焦状态时触发：挂在页面根上，焦点在页面内任何节点都能收到（出处：arkts-interaction-development-guide-keyboard.md，按键事件数据流；onKeyEvent & onKeyPreIme）
- 焦点停在 NavDestination、Canvas 上的 onKeyEvent 收不到；Canvas.defaultFocus(true) 无效，onReady 里 requestFocus 报 150003；改挂 NavDestination 后四向键和 MENU 都生效：返修时真机上的结果（出处：卡里修好并验证过）
- onKeyPreIme(event: Callback<KeyEvent, boolean>): T；onKeyEventDispatch(event: Callback<KeyEvent, boolean>): T：同族接口：输入法前拦截按键、按键分发给子组件前的回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyPreIme / CommonMethod.onKeyEventDispatch）
来源：1 张卡，1 个应用
- case-93d8a31d2b589234ebf2（2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断
