# 源项 match_parent 加 layout_margin 时，边距交给父容器 padding，不叠 margin

审的是：代码
触发（任一种）：
- 读到：列表项或网格项布局的根 android:layout_width="match_parent"，同时带 android:layout_margin；写错的样子：卡片写成 .width('100%') 再叠 .margin(…)，宽变成格宽 + 2×margin 而右溢
- 读到：FrameLayout 等叠放容器的子视图某一轴 match_parent，又带同轴的 android:layout_marginTop / layout_marginBottom 或左右 margin；写错的样子：Stack 里同一修饰链写成 .height('100%') 加 .margin({ top, bottom })，或 .width('100%') 加左右 margin
适用范围：源端 match_parent 加同轴外边距的子项，迁成网格项、列表项或 Row、Column、Stack 子组件时
做法：
- 同轴的 layout_margin 改写到包住它的容器的 padding，子组件保留 '100%'、不写 margin：GridItem() { 卡片.width('100%') }.padding(margin)；Stack 里套外包 Column().padding({ top: <marginTop>, bottom: <marginBottom> }) 包住内层 .height('100%')；或直接给有界的显式尺寸
- 交回前查同一修饰链里 '100%' 与同轴 .margin 的组合并按「父尺寸 − margin」核对；Stack 默认 Alignment.Center、不裁剪，对照源布局核对第一个子组件的起点
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- match_parent 加 margin 的子项尺寸 = 父尺寸 − 父 padding − 同轴 margin：measureChildWithMargins 用 mPaddingLeft + mPaddingRight + lp.leftMargin + lp.rightMargin 扣出可用宽；FrameLayout 量 match_parent 子视图时扣 lp.topMargin、lp.bottomMargin（宽同理）：源端 match_parent 加同轴 margin 的几何是父尺寸减去 margin（出处：android.view.ViewGroup#measureChildWithMargins；android.widget.FrameLayout#onMeasure）
- 百分比尺寸参考最近设置了固定大小的祖先节点的尺寸，不扣自身 margin；在 Row、Column、Flex 交叉轴上，子组件交叉轴的大小与 margin 的和为整体：目标端 '100%' 再加同轴 margin 会超出父容器（出处：ts-universal-attributes-size.md，尺寸设置（开头的说明）、margin）
- padding(value: Padding | Length | LocalizedPadding): T：父容器、GridItem 或外包容器上承接内缩用的内边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- 卡片 margin 移到 GridItem.padding 后宽度不再右溢：网格项修好的写法（出处：卡里修好并验证过）
- 百分比高按父高计算、不扣除 margin，'100%' 加同轴 margin 的子组件总占位超出父 Stack；改成外包 Column 的 padding 加内层 '100%' 后位置恢复：叠层里直译的后果和修好的写法（出处：卡里修好并验证过）
- alignContent(value: Alignment): StackAttribute，默认 Alignment.Center：Stack 不设 alignContent 时子组件居中，超高的子组件上下两头都会溢出（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackAttribute.alignContent、StackOptions.alignContent）
- FrameLayout 子视图默认 gravity 是 Gravity.TOP | Gravity.START：源端叠层从左上角起排，与 Stack 默认居中不同（出处：android.widget.FrameLayout#DEFAULT_CHILD_GRAVITY）
- clip(value: boolean): T，默认 false：容器默认不裁剪超出自身范围的子组件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.clip）
未核实：width('100%') 加 margin 造成右溢，case-e7f02c687378e98dc213 里是按几何推演判断，没有单独截图确认；case-66989090d28a600f93bf 里观察到的行为出自鸿蒙 SDK 6.1.1(24)，本机声明按 API 23 核实
来源：2 张卡，1 个应用
- case-66989090d28a600f93bf（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断
- case-e7f02c687378e98dc213（免费来电多多）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
