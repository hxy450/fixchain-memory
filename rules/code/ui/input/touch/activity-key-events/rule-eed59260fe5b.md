# 源端 onKeyDown 迁成 onKeyEvent 时，回调里加 KeyType.Down 守卫

审的是：代码
触发（任一种）：
- 读到：源端 Activity 或 View 重写 onKeyDown(int keyCode, KeyEvent event) 处理按键（只在按下时进入）；写错的样子：.onKeyEvent((event: KeyEvent) => …) 回调里没有判断 event.type === KeyType.Down，按下和抬起各执行一次源端逻辑
适用范围：把安卓 onKeyDown 里的按键处理迁成 ArkUI 组件 .onKeyEvent 回调时
做法：
- 在 .onKeyEvent 回调开头写 if (event.type !== KeyType.Down) { return; }，只在 KeyType.Down 时执行源端 onKeyDown 的逻辑
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onKeyEvent(event: (event: KeyEvent) => void): T：组件获焦后的按键回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEvent）
- 每个按键都有 2 次回调，分别对应 KeyType.Down 和 KeyType.Up：onKeyEvent 对按下、抬起各派发一次（出处：arkts-interaction-development-guide-keyboard.md，onKeyEvent & onKeyPreIme）
- KeyEvent.type: KeyType；KeyType.Down（Press the key）、KeyType.Up（The key is released）：守卫判断用的字段和枚举值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，KeyEvent.type；ets/component/enums.d.ts，KeyType）
- onKeyDown：Called when a key down event has occurred：源端只在按下时进入（出处：android.view.KeyEvent.Callback#onKeyDown）
- onKeyEvent(event: Callback<KeyEvent, boolean>): T：同族接口：CommonMethod.onKeyEvent 的 API 15 重载，回调返回 boolean（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEvent）
- onKeyPreIme(event: Callback<KeyEvent, boolean>): T：同族接口：CommonMethod 上在输入法之前处理按键（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyPreIme）
来源：1 张卡，1 个应用
- case-e96028e4cc29cd5bd8eb（2048）：做法第 1 步 ← 诊断、建议 3
