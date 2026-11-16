# Activity 的按键回调（onKeyDown、onKeyUp）

agent 会看到什么：读到 Activity 或 View 覆写 onKeyDown / onKeyUp / dispatchKeyEvent 处理 KEYCODE_*；交回的 .onKeyEvent 没判 KeyType、挂在要先获焦的子组件上、页内没有可获焦组件，或不放行输入框

## 规矩

- rule-eed59260fe5b｜源端 onKeyDown 迁成 onKeyEvent 时，回调里加 KeyType.Down 守卫｜读到：源端 Activity 或 View 重写 onKeyDown(int keyCode, KeyEvent event) 处理按键（只在按下时进入）；写错：.onKeyEvent((event: KeyEvent) => …) 回调里没有判断 event.type === KeyType.Down，按下和抬起各执行一次源端逻辑
- rule-0216b4ca6b2e｜源端是 Activity 级 onKeyDown 时，.onKeyEvent 挂在页面根节点，不挂在要先获焦的子组件上｜读到：Activity 覆写 onKeyDown 或 dispatchKeyEvent 处理 KEYCODE_DPAD_*、KEYCODE_MENU 等按键，不依赖哪个 View 持有焦点；写错：.onKeyEvent 挂在 Canvas 或自绘子组件上，只加了 .focusable(true)，页面根（NavDestination 或 @Entry 根组件）上没有 .onKeyEvent
- rule-e02947f9f99e｜Activity 级 onKeyDown 迁成 onKeyEvent 时，页内要有可获焦组件让焦点链经过本页｜读到：Activity 上覆写 onKeyDown(int keyCode, KeyEvent event)，处理 KEYCODE_DPAD_* 方向键或 Ctrl 组合键（如 KEYCODE_Z 加 isCtrlPressed()）；写错：目标页把 onKeyEvent 挂在 NavDestination 或 @Entry 根节点，但 build 里没有 Button、TextInput 或显式 .focusable(true) 的组件；按键到达窗口后 DispatchKeyEventCallback consumed: 0，页面回调不触发
- rule-638d9bebc5ab｜根级键盘快捷键要放行输入框时，写显式判据，不假定 TextInput 会吞掉抬起事件｜读到：源端 Activity.onKeyUp 先判 getCurrentFocus() instanceof EditText，是就 return super.onKeyUp 放行，之后才映射 KEYCODE_* 快捷键；写错：根组件 .onKeyEvent 里只判 event.type === KeyType.Up 就触发快捷键，注释假定 TextInput 聚焦时按键被输入框先消费、不冒泡到根
- rule-95110fef255a｜页面有按键分发时，根容器设 focusable、defaultFocus 并接 onKeyPreIme｜读到：源端 Activity 覆写 onKeyDown 分发硬件键；写错：目标有按键分发方法，但页面根容器没有 `.focusable(true)`、`.defaultFocus(true)`，也没有 .onKeyPreIme(...) / .onKeyEvent(...)，分发方法在页面上没有入口
- rule-0fa194cfca18｜按规格键位表逐键核对 KeyCode 到动作的映射，源端按模式分支的键保留模式判断｜读到：源端 onKeyDown 里同一键按模式分支：遥控模式下 KEYCODE_DPAD_UP / DOWN 走行导航、KEYCODE_SPACE 先走菜单命令，否则另作他用；写错：目标把 KEYCODE_DPAD_UP / DOWN 并进另一个键（如 KEYCODE_NUMPAD_MULTIPLY）的分支直接切换弹层，KEYCODE_SPACE 直接拍照，没有遥控模式状态和分支
- rule-073f3fe2d20d｜桥接源端同名方法而目标缺失时，读源方法正文实现，不用 toggle 或恒 false 近似｜读到：目标端 `interface` 的注释写明其中方法对应源端同名方法（如菜单命令、上下键处理，返回 true 表示已消费），而目标控制器里没有这些方法；写错：接线时把这类方法接到现成的 toggle 方法上，或让返回「是否已消费」的方法恒 `return false`，注释还自述会改变行为
- rule-4fefa762bd9d｜要由按键驱动的选择和展开态放进 @ObservedV2/@Trace 模型，不放组件 @Local｜读到：源端 onKeyDown 的遥控导航在模型侧逐行逐项改弹层或面板的选择、展开和高亮（行/项下标字段）；写错：面板组件用 `@Local` 保存选中下标和展开态，弹层分组的模型是普通类（没有 @ObservedV2 / @Trace），控件没有高亮入参
