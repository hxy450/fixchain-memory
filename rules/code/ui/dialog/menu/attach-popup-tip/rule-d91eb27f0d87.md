# 源端 AttachPopupView 锚定父页控件时，目标提示挂在锚点所在页并按锚点实测位置定箭头

审的是：代码
触发（任一种）：
- 读到：弹窗类继承 `AttachPopupView`，调用方用 atView(...) 传入的锚点视图取自 parentFragment，箭头边距按锚点宽度计算；写错的样子：目标的提示浮层写在子页组件的 build() 里，用写死的 right/top 数值（.position / .margin）定位，和锚点组件的位置无关
适用范围：安卓依附式弹窗（锚定在另一个页面的视图上弹出）迁成 ArkUI 时
做法：
- 提示组件声明在锚点组件所在的页面（父页）里，与锚点同处一个布局，由父页控制显隐，不写在触发它的子页里
- 在锚点组件上挂 .onAreaChange((oldValue: Area, newValue: Area) => {…})，用 newValue.globalPosition 和 newValue.width 算气泡和箭头的位置（单位 vp），不写固定边距
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：所有组件都有的区域变化回调，组件尺寸或位置变化完成后触发（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- Area.width、Area.height 单位 vp；Area.globalPosition 是组件左上角在当前窗口坐标系中的位置，Position.x / y 单位 vp：算箭头位置用的锚点实测值（出处：ts-types.md，Area、Position；鸿蒙 SDK 的 ets/component/units.d.ts，Area.globalPosition）
- onAreaChange 只响应布局变化导致的大小、位置变化，不响应 translate、offset、markAnchor、scale、transform：锚点靠这些属性移动时回调不触发，位置要另取（出处：ts-universal-component-area-change-event.md，onAreaChange）
- 提示组件改挂到锚点所在页、锚定锚点组件后，箭头对齐锚点：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端箭头边距怎么由锚点算出：源工程里调用 atView(...) 并设置箭头边距的那段代码（按锚点宽度计算的那一处）；读出公式（如锚点宽度的一半加某个 dp 常量），在目标端用 newValue.width 和同样的常量按 vp 重算
来源：1 张卡，1 个应用
- case-c777abf40cffa3ab181d（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 4 ← 诊断
