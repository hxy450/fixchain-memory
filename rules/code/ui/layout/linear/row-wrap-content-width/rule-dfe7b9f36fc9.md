# 横向 LinearLayout 里定宽兄弟后的自适应宽文字，Row 里加 flexShrink(1)

审的是：代码
触发（任一种）：
- 读到：横向 `<LinearLayout android:orientation="horizontal">`（常见于 layout-land 变体）里固定 dp 的 ImageView 之后，跟一个 android:layout_width="wrap_content" 的多行 TextView；写错的样子：Row 里对应的 Text 只有 fontSize、padding、margin、height，没有 .flexShrink(1)、.layoutWeight(1) 或宽度约束；Row 本身已 .width('100%') 也照样溢出
适用范围：横向 LinearLayout 迁成 ArkUI Row、文字排在固定尺寸兄弟之后且可能长于剩余宽度时，含 layout-land 等配置变体
做法：
- 给该 Text 加 .flexShrink(1)（或 .layoutWeight(1)、显式剩余宽度）；Row 已 .width('100%') 也不能省，Row 子项默认不收缩
- 页面有 layout-land 等变体时逐个变体核对文字的主轴宽度约束，竖屏 Column 的折行结论不代替横屏 Row
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- flexShrink(value: number): T；父容器是 Row、Column 时默认 0，且父容器要设主轴尺寸才生效：Row 子项默认不收缩，按自然宽度排布（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.flexShrink；ts-universal-attributes-flex-layout.md，flexShrink）
- layoutWeight(value: number | string): T，默认 0；大于 0 的子项从主轴剩余空间按权重分配，忽略自身尺寸：另一种让文字只占剩余宽度的写法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight；ts-universal-attributes-size.md，layoutWeight）
- 子项 WRAP_CONTENT 时测量模式是 AT_MOST，上限是父容器给的剩余尺寸：源端文字在剩余宽度内折行的来源（出处：android.view.ViewGroup#getChildMeasureSpec）
- 横屏各页说明文字加 .flexShrink(1) 后在图片右侧剩余宽度内折行：修好后的写法（出处：卡里修好并验证过）
- flexGrow(value: number): T：同族接口：父容器有剩余空间时的拉伸比例（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.flexGrow）
来源：1 张卡，1 个应用
- case-e4abf8f80dac25135b2e（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
