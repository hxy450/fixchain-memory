# linearGradient 的 angle 0 指向上方、90 左到右，轴向渐变优先用 direction

审的是：代码
触发（任一种）：
- 读到：源端 Compose 用 .fadingEdges(scrollState) 配 .horizontalScroll(...) 或 .verticalScroll(...) 做边缘渐隐；或规格写「横向滚动 + fadingEdges（linearGradient 遮罩）」；写错的样子：左右两端的遮罩条写成 .linearGradient({ angle: 0 / 180, ... })，上下两端的写成 angle 90 / 270，横纵整组互换
适用范围：用 ArkUI linearGradient 写渐变（尤其是滚动边缘的渐隐遮罩条）、确定方向时
做法：
- angle 按 CSS 语义：0 自下而上（colors[0] 在底边）、90 左→右、180 上→下（缺省）、270 右→左；左右、上下这类轴向渐变优先写 direction: GradientDirection.Right / Left / Bottom / Top，不按 Android GradientDrawable 或数学坐标（0 = 向右）换算
- 写完逐条列出每个渐变条在哪条边、angle 或 direction、colors[0] 落在哪条边；同一文件里横向和纵向遮罩分别核对，避免整组互换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- angle 为 0 度时渐变方向从下往上，顺时针为正，默认值 180：所以 90 是左→右、180 是上→下、270 是右→左（出处：ts-universal-attributes-gradient-color.md，LinearGradientOptions对象说明）
- direction 在 angle 不是 undefined 时不生效；direction 默认 GradientDirection.Bottom：两者都写时以 angle 为准（出处：ts-universal-attributes-gradient-color.md，LinearGradientOptions对象说明；鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions.direction）
- GradientDirection.Left：右→左；Right：左→右；Top：自下而上；Bottom：自上而下：轴向渐变用的枚举（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，GradientDirection）
- linearGradient(value: LinearGradientOptions): T：组件的线性渐变（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
- 横向遮罩改为左条 angle 90、右条 angle 270 后方向和源端一致：修好后的写法（出处：卡里修好并验证过）
- constructor(options: LinearGradientOptions)：同族接口：LinearGradientStyle（文字着色用的线性渐变，@since 20），角度同样按 LinearGradientOptions（出处：鸿蒙 SDK 的 ets/component/text_common.d.ts，LinearGradientStyle.constructor）
来源：1 张卡，1 个应用
- case-9190f97a15e03668b874（GameOfLife）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3；取值 5 ← 诊断
