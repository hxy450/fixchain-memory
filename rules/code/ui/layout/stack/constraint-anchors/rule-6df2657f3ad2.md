# 多个子项都锚 parent 底的 ConstraintLayout 改 Column 流式时，重算底边距或改贴底定位

审的是：代码
触发（任一种）：
- 读到：ConstraintLayout 里两个及以上子项都写 app:layout_constraintBottom_toBottomOf="parent"，各带 android:layout_marginBottom，其中有 android:visibility="invisible" 仍占位的行；写错的样子：目标写成 Column 顺序流，每个子项照抄源端 .margin({ bottom: <源值> })，排在后面的兄弟写 .visibility(Visibility.Hidden) 仍占位，于是前一个子项的底边距从这个兄弟之上算起
适用范围：把 ConstraintLayout 内容层改写成 ArkUI Column / Row 顺序流时，多个子项各自锚父容器底边的情形
做法：
- 改写前先列出每个子项的锚点；多个子项都锚 parent 底时，不照抄原 margin 按顺序堆叠
- 二选一：用 Stack 或 RelativeContainer 按源 margin 贴底（RelativeContainer 里写 .alignRules({ bottom: { anchor: '__container__', align: VerticalAlign.Bottom } }).margin({ bottom: <源 marginBottom> })）；或保留流式，把前一个子项的底边距改成 源 marginBottom − Σ(其后流式兄弟的高度 + 其 marginBottom)，Hidden 的兄弟也要算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Visibility.Hidden：隐藏但参与布局占位；Visibility.None：隐藏且不占位：源端 invisible 对应 Hidden，它在 Column 流里仍占高度（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
- View.INVISIBLE：不可见，但仍为布局占位：源端 invisible 的行在 ConstraintLayout 里也占位，只是各自锚底、不互相推（出处：android.view.View#INVISIBLE）
- alignRules(value: AlignRuleOption): T，只在 RelativeContainer 里生效：贴底定位的写法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.alignRules）
- '__container__' 代表 RelativeContainer 父容器的 id；RelativeContainer 子组件的 margin 是到该方向锚点的距离：锚父底时 margin bottom 就是源端 marginBottom（出处：arkts-layout-development-relative-layout.md，锚点设置；ts-container-relativecontainer.md，开头的说明）
- 保留流式、把前一个子项的底边距改成 源 marginBottom − (后面 Hidden 行的高度 + 其 marginBottom) 后，位置与源端对齐：扣减重算的做法（出处：卡里修好并验证过）
未核实：卡里的观察出自 HarmonyOS 6.1.1(24)，本机核对声明用的是 API 23
来源：1 张卡，1 个应用
- case-50467dd451cd7c5be566（免费来电多多）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
