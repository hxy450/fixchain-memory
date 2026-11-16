# 要求一比一而源端是 Holo 下拉面板时，规格把溢出菜单定为页内浮层，不只写通用 Menu 映射

审的是：规格
触发（任一种）：
- 读到：showAsAction="never" 的项由平台主题绘制的下拉面板（ListPopupWindow）承载；任务要求与源端逐屏一致；写错的样子：转换决策沿用通用映射「PopupMenu → Menu + MenuItem」，没写系统 Menu 与 Holo 面板在形状、分隔线、定位上的差异，也没定替代承载方式
适用范围：规格提取阶段，为平台主题绘制的溢出面板写转换决策、且要求一比一时
做法：
- 转换决策直接定为页内浮层：全屏遮罩只负责关闭并吞掉事件（不触发下层），面板按可见契约自绘并贴 ActionBar 下沿定位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hitTestBehavior(value: HitTestMode): T；HitTestMode.Block：自身响应触摸，并阻断被它盖住的节点的命中测试：全屏遮罩用 Block，点外部只关闭、不传到下层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior；ets/component/enums.d.ts，HitTestMode.Block）
- 页内浮层：全屏遮罩 HitTestMode.Block 且点击只关闭，面板宽、行高、分隔线、上沿亮边按契约自绘：卡里返修对照截图后的承载方式（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c6728cbe6feb50c4f9ea（Blockinger）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
