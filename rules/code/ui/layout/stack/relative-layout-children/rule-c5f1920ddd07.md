# RelativeLayout 子项各锚两端时用 Stack+position，不写 Row+Blank

审的是：代码
触发（任一种）：
- 读到：RelativeLayout 里一个子项 android:layout_alignParentStart 加 marginStart，另一个 android:layout_alignParentEnd 加 marginEnd，容器定宽；写错的样子：目标写成 Row { Text().margin({ left }), Blank(), Text().margin({ right }) }，两段文字被并排挤开，不像源端那样各自贴边、可能重叠
适用范围：安卓 RelativeLayout 的子项各自锚定父容器两端、迁到 ArkUI 时
做法：
- 外层用 Stack，宽度同源容器；两个子项分别写 .position({ left: <marginStart 的值> }) 和 .position({ right: <marginEnd 的值> })，各自相对父容器两边定位
- 先算容器宽减两侧边距，小于两段文字宽度之和时源端就是重叠显示，目标保留重叠，不为避免重叠改成并排
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- position(value: Position | Edges | LocalizedEdges): T：相对父组件的绝对定位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- Edges：top/left/right/bottom 分别为组件各边距离父组件内容区相应边的边距（@since 12）：position({ right: x }) 就是右边贴父容器右内边 x（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Edges；ts-universal-attributes-location.md，position）
- offset(value: Position | Edges | LocalizedEdges): T：同族接口：相对原布局位置偏移，不影响父布局，不能代替锚定两端（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.offset）
- Stack + position({ left }) / position({ right }) 重叠定位后与源端一致：卡里最终保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-f103fbdcad4e6eeb7569（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断
