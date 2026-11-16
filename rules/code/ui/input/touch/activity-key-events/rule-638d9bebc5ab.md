# 根级键盘快捷键要放行输入框时，写显式判据，不假定 TextInput 会吞掉抬起事件

审的是：代码
触发（任一种）：
- 读到：源端 Activity.onKeyUp 先判 getCurrentFocus() instanceof EditText，是就 return super.onKeyUp 放行，之后才映射 KEYCODE_* 快捷键；写错的样子：根组件 .onKeyEvent 里只判 event.type === KeyType.Up 就触发快捷键，注释假定 TextInput 聚焦时按键被输入框先消费、不冒泡到根
适用范围：在入口页根组件统一处理硬件键盘快捷键、源端要求输入框聚焦时不拦截时
做法：
- 根组件 onKeyEvent 在 KeyType.Down 时记下 event.keyCode；KeyType.Up 时只处理记过按下的键并把它移除，没见过按下的抬起一律放过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onKeyEvent(event: Callback<KeyEvent, boolean>): T：组件获焦后的按键回调，返回 true 视为已处理（@since 15；旧签名 onKeyEvent(event: (event: KeyEvent) => void): T）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEvent）
- onKeyEvent 事件默认冒泡：子组件处理完的按键事件会再交给父组件，根组件能收到输入框里的按键（出处：ts-universal-events-key.md，示例4（使用stopPropagation阻止冒泡））
- KeyType.Down（按下）、KeyType.Up（抬起）：按键事件的两种类型（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，KeyType）
- 聚焦的 TextInput 只消费字符键的按下，抬起仍冒泡到根；改成只处理根上见过按下的抬起后，输入框内键入快捷键字母不再触发，框外快捷键仍生效：卡里上机看到的行为和修好后的结果（出处：卡里修好并验证过）
- onKeyPreIme(event: Callback<KeyEvent, boolean>): T：同族接口：CommonMethod 上在输入法之前处理按键，返回 true 时后续回调被拦截（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyPreIme）
- onKeyEventDispatch(event: Callback<KeyEvent, boolean>): T：同族接口：CommonMethod 上自定义按键分发，按键不再分发给子组件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onKeyEventDispatch）
未核实：卡里上机看到的行为出自 HarmonyOS API 21–23，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-f32c19bb6ab1caffe063（AntennaPod）：做法第 1 步 ← 建议 4、诊断；取值 4 ← 诊断
