# 源子项贴父容器某边时，Stack 子项不用 .align，改父 alignContent 或 .position

审的是：代码
触发（任一种）：
- 读到：FrameLayout / CoordinatorLayout 子项写 android:layout_gravity（bottom、bottom|end 等），或映射参考写 layout_gravity → .align(Alignment.X)；写错的样子：Stack 子项上写 .align(Alignment.Bottom / BottomEnd)，父 Stack 没写 alignContent
- 读到：RelativeLayout 子项写 layout_alignParentBottom / End / Top / Start，或 layout_alignBottom="@id/…"；写错的样子：Stack 子项上写 .align(Alignment.X)，想让它贴边贴角
适用范围：安卓父容器的子项定位规则迁成 ArkUI Stack 叠放子项时
做法：
- 子项都贴同一边：写 Stack({ alignContent: Alignment.Bottom })（按源 gravity 取值），删掉子项的 .align
- 对齐混合：贴边子项写 .position({ right: <源 marginEnd>, bottom: <源 marginBottom> })，满宽浮层写 .position({ left: 0, bottom: 0 })；或包进满幅透明 Column 配 .justifyContent(FlexAlign.End)
- 交付前搜 .align(Alignment.，逐个核对父容器类型和意图
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- align(value: Alignment): T，默认 Alignment.Center：对齐的是组件自己绘制区域里的内容；在 Stack 上等同 alignContent，写在子项上不移动子项本身（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.align；ts-universal-attributes-location.md，align）
- StackOptions.alignContent?: Alignment，@default Alignment.Center：Stack 子项默认居中摆放，不是左上（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- alignContent(value: Alignment): StackAttribute：属性写法的 Stack 子项对齐，与构造参数 alignContent 等效（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackAttribute.alignContent）
- position(value: Position | Edges | LocalizedEdges): T：相对父组件内容区的绝对定位；传 Edges 时按四边距离定位，适用于悬浮按钮、置顶显示（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position；ts-universal-attributes-location.md，position）
- Edges { top?: Dimension; left?: Dimension; bottom?: Dimension; right?: Dimension }（@since 12）：各项是组件该边到父组件内容区对应边的距离，源端 margin 填进对应的边（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Edges）
- DEFAULT_CHILD_GRAVITY = Gravity.TOP | Gravity.START：源端 FrameLayout 子项不写 layout_gravity 时贴左上；两端默认值不同，不能当成一样（出处：android.widget.FrameLayout#DEFAULT_CHILD_GRAVITY）
- 满宽浮层改 .position({ left: 0, bottom: 0 })，悬浮按钮改 .position({ right, bottom }) 填源 margin，同向叠层改父 Stack({ alignContent: Alignment.Bottom }) 后贴底：改完后各子项贴到源端的边和角（出处：卡里修好并验证过）
- alignContent(value: Alignment): FolderStackAttribute：同族接口：FolderStack 的子项对齐，同样定在容器上而不是子项上（出处：鸿蒙 SDK 的 ets/component/folder_stack.d.ts，FolderStackAttribute.alignContent）
来源：1 张卡，1 个应用
- case-d53f19cb359b879b340c（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2、诊断；做法第 3 步 ← 建议 3；取值 7 ← 诊断
