# 页内浮层承载源端非托管对话框、源 Activity 会重建时，补横竖翻转的关闭路径

审的是：代码
触发（任一种）：
- 读到：源 Activity 没有 android:configChanges 也没有 screenOrientation 锁定，对话框用 AlertDialog.Builder(...).show() 直接弹出；写错的样子：目标端用 @Local / @State 布尔量驱动的页内浮层，只在 Back、遮罩、返回键和 aboutToDisappear 时关闭，没有方向或配置变化的关闭路径
适用范围：实现阶段用页内状态驱动浮层承载源端非托管对话框时
做法：
- 在页面根容器挂 .onAreaChange((oldValue: Area, newValue: Area) => { … })，记住上次的横竖（宽 > 高）；横竖翻转时把浮层状态置 false
- Back、遮罩、返回键这些关闭路径照留，方向变化的关闭路径是另加的一条；在两端旋转对照
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件尺寸或位置变化完成后回调，可用新旧宽高判断横竖翻转（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 根 Stack 挂 onAreaChange，页面区域横竖翻转时关闭帮助类浮层；旋转对照后对话框不再残留：修好并验证过的写法（出处：卡里修好并验证过）
- onConfigurationUpdate(newConfig: Configuration): void：Ability 收到配置变化的回调，卡里建议的另一个关闭时机（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
- onSizeChange(event: SizeChangeCallback): T：同族接口：组件尺寸变化回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onSizeChange）
未核实：onConfigurationUpdate 这条关闭时机卡里没有上机验证，验证过的是 onAreaChange
来源：1 张卡，1 个应用
- case-b99e7061a74e82b731f3（Blockinger）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 建议 3；取值 2 ← 诊断
