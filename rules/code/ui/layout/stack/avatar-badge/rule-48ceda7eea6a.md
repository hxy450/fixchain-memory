# FrameLayout 里贴右下的角标，目标用 position 按父容器坐标定位，不靠子项 .align()

审的是：代码
触发（任一种）：
- 读到：固定尺寸 `<FrameLayout>` 里头像铺满，小角标 `android:layout_gravity="end|bottom"` 贴右下；写错的样子：`Stack({ alignContent: Alignment.TopStart })` 里只给角标写 `.align(Alignment.BottomEnd)`，角标仍在左上
适用范围：把 FrameLayout 中按 layout_gravity 叠放的子项迁成 ArkUI Stack 叠放时
做法：
- 在 W×H 的头像容器里给角标写 .position({ x: W - 角标宽, y: H - 角标高 })，W、H 和角标宽高取源 XML 的 layout_width / layout_height
- 或者给这个子项单独套一层 Stack({ alignContent: Alignment.BottomEnd })；不要指望子组件的 .align() 移动它自身
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- align(value: Alignment): T 设置的是当前组件绘制区域内子组件的对齐方式；在 Stack 中与 alignContent 效果一致：写在角标上的 .align 只影响角标自己的内容，不移动角标在父 Stack 里的位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.align；ts-universal-attributes-location.md，align）
- position(value: Position | Edges | LocalizedEdges): T：相对父组件的绝对位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- alignContent(value: Alignment): StackAttribute；StackOptions.alignContent?: Alignment：Stack 子组件的位置由父 Stack 的 alignContent 决定（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackAttribute.alignContent、StackOptions）
- FrameLayout 通过给每个子项设 android:layout_gravity 控制它在 FrameLayout 内的位置：源端的位置属性在子项上，目标端要换成父容器坐标（出处：android.widget.FrameLayout（类注释））
- 角标改成 .position({ x: 容器宽 - 角标宽, y: 容器高 - 角标高 }) 后，真机控件树显示角标与头像右边、下边对齐：修法已上机验证（出处：卡里修好并验证过）
针对本应用要查的：
- 容器和角标的尺寸：源工程布局 XML 里这个 FrameLayout 及角标子项的 layout_width / layout_height；dp 值按 vp 写，x = 容器宽 - 角标宽，y = 容器高 - 角标高
来源：1 张卡，1 个应用
- case-c9cc6663456a2ef02f89（记得日历）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
