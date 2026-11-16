# 锚在兄弟行上方的控件转 Stack 时，底距写兄弟行高加 padding 加自身 margin

审的是：代码
触发（任一种）：
- 读到：TextView 带 app:layout_constraintBottom_toTopOf="@+id/…"（指向按钮行等兄弟控件）和 android:layout_marginBottom、android:layout_marginStart；写错的样子：转成全高 Stack({ alignContent: Alignment.BottomStart }) 贴父容器底部，没有兄弟行的高度偏移，也没应用 marginStart / marginBottom；文字压在按钮上
适用范围：把 ConstraintLayout 里锚在兄弟控件上方或下方的控件转成 Stack 浮层时
做法：
- 逐个核对 layout_constraintX_toYOf 的兄弟锚点；锚在兄弟行上方的，底距 = 兄弟行高度 + 兄弟行上下 padding + 自身 marginBottom，左距 = marginStart，写成 .padding({ left: <marginStart>, bottom: <底距> })，不简化成父容器 BottomStart
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- alignContent(value: Alignment): StackAttribute：只按父 Stack 对齐，不知道兄弟控件的位置（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackAttribute.alignContent）
- padding(value: Padding | Length | LocalizedPadding): T：修复里用 Padding 对象写左距和底距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- padding({ left: 16, bottom: 85 })，85 = 按钮行高 45 + 上下 padding 2×10 + marginBottom 20：修复后的写法（例：源值是 marginStart 16dp、marginBottom 20dp）（出处：卡里修好并验证过）
针对本应用要查的：
- 兄弟行的实际高度和 padding：源布局 XML 里被锚的那个控件：android:layout_height、android:padding*；wrap_content 时看它的子控件；高度 + 上下 padding 加上自身 marginBottom 得到底距；wrap_content 且高度取决于内容时记进 unverified，不自己补定值
来源：1 张卡，1 个应用
- case-c85d8667f78c2cc8f53a（免费来电多多）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断、建议 2
