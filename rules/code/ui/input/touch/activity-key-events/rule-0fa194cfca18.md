# 按规格键位表逐键核对 KeyCode 到动作的映射，源端按模式分支的键保留模式判断

审的是：代码
触发（任一种）：
- 读到：源端 onKeyDown 里同一键按模式分支：遥控模式下 KEYCODE_DPAD_UP / DOWN 走行导航、KEYCODE_SPACE 先走菜单命令，否则另作他用；写错的样子：目标把 KEYCODE_DPAD_UP / DOWN 并进另一个键（如 KEYCODE_NUMPAD_MULTIPLY）的分支直接切换弹层，KEYCODE_SPACE 直接拍照，没有遥控模式状态和分支
适用范围：把源端按键分发矩阵迁成 ArkTS 的 KeyCode → 动作映射时
做法：
- 按规格键位表逐条写 KeyCode → 动作映射，每个键对照源端 onKeyDown 的分支；源端按模式分支的键在目标端保留同样的模式判断，模式标志放进状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- KEYCODE_DPAD_UP = 2012、KEYCODE_DPAD_DOWN = 2013、KEYCODE_SPACE = 2050、KEYCODE_NUMPAD_MULTIPLY = 2114：目标端的键码值，和 Android KeyEvent 的数值不同（出处：鸿蒙 SDK 的 ets/api/@ohos.multimodalInput.keyCode.d.ts，KeyCode；android.view.KeyEvent#KEYCODE_DPAD_UP）
- KeyEvent.type: KeyType；KeyEvent.keyCode: number：回调里取按下或抬起和键码（出处：鸿蒙 SDK 的 ets/component/common.d.ts，KeyEvent）
- 修复新增按键路由，把 KeyCode 映射成动作，按源端的键位让 DPAD 等键进入遥控导航：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-cbf23fa7a4ed42d37671（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
