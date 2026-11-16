# Stack 里盖在可点击兄弟上方、自身不处理点击的层，显式写 hitTestBehavior(Transparent)

审的是：代码
触发（任一种）：
- 读到：源 `FrameLayout` 里较晚声明（z 序更高）的 `match_parent` 容器本身不可点击（没有 `android:clickable`、没有点击监听），却覆盖较早声明的按钮组或底部控制行；写错的样子：对应 `Stack` 的上层子容器是 `.width('100%').height('100%')`，没有 `.hitTestBehavior(HitTestMode.Transparent)`；或者为还原 z 序重排后，`Transparent` 还留在原来那几个「浮层」上、没跟到现在位于上方的层
适用范围：把安卓 FrameLayout 叠放层翻译成 ArkUI Stack、确定各子层命中测试行为时
做法：
- 按 Stack 最终的子节点顺序逐层看：位于可点击兄弟之上、尺寸覆盖其区域、自身不处理点击的容器，写 .hitTestBehavior(HitTestMode.Transparent)；不要假设没有 onClick 的容器不参与命中
- 重排子节点顺序后重新核对 Transparent 落在哪些层：跟随「在上方且覆盖下层控件」的层，不沿用重排前的浮层身份
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 给顶层全尺寸主内容层补 hitTestBehavior(HitTestMode.Transparent) 后，被它覆盖的胶囊和底部控制行恢复可点：修好的写法（出处：卡里修好并验证过）
- hitTestBehavior(value: HitTestMode): T，默认 HitTestMode.Default：自身和子节点响应命中，兄弟节点被挡：不写时上层容器会挡住下层兄弟（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- HitTestMode.Transparent：自身和子节点响应命中，并允许被它遮住的其他节点参与命中：上层容器既保留自己子节点的点击，又让下层兄弟可点（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Transparent）
- FrameLayout 的子视图按栈绘制，最后加入的在最上面：源端声明越晚 z 序越高，Stack 里也在上方（出处：android.widget.FrameLayout）
未核实：卡里的观察出自 HarmonyOS 6.1.1(24)，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-57a208ad2e9541272704（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
