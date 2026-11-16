# LinearLayout 带权 wrap_content 子项按 share 公式显式算尺寸，不用 flexGrow

审的是：代码
触发（任一种）：
- 读到：LinearLayout 下多个子项为 wrap_content 且带 android:layout_weight（可能还有 android:weightSum）；写错的样子：目标里这些子项写成 Flex / Column 里的 .flexGrow(1) 或 .layoutWeight(1) 交给框架分余量，没有显式算出各框的尺寸；自然尺寸之和超过可用尺寸时框高不对
- 读到：带权 wrap_content 子项里的 ImageView，图片固有尺寸大于权重行能给的空间；写错的样子：图片写成 24×24 这类经验值加 ImageFit.Contain
适用范围：安卓 LinearLayout 里带权子项的尺寸是 wrap_content（自然尺寸非 0），迁成 ArkUI 容器时，含自然尺寸之和超过可用尺寸的情形
做法：
- 先求各子项沿主轴的自然尺寸（图片按分轴测量取密度缩放后的固有尺寸），余量 = 父容器主轴可用尺寸 − 各子项自然尺寸之和
- 按子项顺序逐个算 share = Math.trunc(weight × 余量 / 剩余权重和)，余量 -= share，剩余权重和 -= weight，子项尺寸 = Math.max(0, 自然尺寸 + share)；剩余权重和起始取 weightSum（大于 0 时），否则取各权重之和；余量为负时照同一公式扣减
- 把算出的尺寸写成各子项显式的 .height(...)（纵向）或 .width(...)（横向），去掉 flexGrow / layoutWeight；图片超出时按父级给的上限夹紧图片盒子宽高再 .objectFit(ImageFit.Contain)，不填经验值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- final int share = (int) (childWeight * remainingExcess / remainingWeightSum); remainingExcess -= share; remainingWeightSum -= childWeight;：安卓逐个带权子项分余量的公式，余量可为负（出处：android.widget.LinearLayout#measureVertical（横向同在 measureHorizontal））
- float remainingWeightSum = mWeightSum > 0.0f ? mWeightSum : totalWeight;：剩余权重和的起始值（出处：android.widget.LinearLayout#measureVertical）
- childHeight = child.getMeasuredHeight() + share; MeasureSpec.makeMeasureSpec(Math.max(0, childHeight), MeasureSpec.EXACTLY)：wrap_content 带权子项的最终尺寸 = 自然尺寸 + share，下限 0；layout_height 为 0 时才只取 share（出处：android.widget.LinearLayout#measureVertical）
- flexGrow(value: number): T：只分配父容器的剩余空间，不对应 LinearLayout 余量为负时的等量扣减（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.flexGrow）
- flexShrink(value: number): T，Column / Row 下默认 0，Flex 下默认 1：压缩比例和 LinearLayout 的按权等量扣减不是同一算法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.flexShrink）
- layoutWeight 分配时会忽略元素本身的尺寸设置：所以 wrap_content 加权重的子项不能直接写成 layoutWeight（出处：ts-universal-attributes-size.md，layoutWeight）
- ImageView 默认 mScaleType = ScaleType.FIT_CENTER：源端没写 scaleType 时按 FIT_CENTER 等比缩放居中（出处：android.widget.ImageView#initImageView）
- objectFit(value: ImageFit): ImageAttribute，默认 ImageFit.Cover；ImageFit.Contain 保持宽高比缩放，使图片完整显示在显示边界内：目标端不写 objectFit 时是 Cover（裁切填满），和安卓默认不同，要显式写 Contain 对应 FIT_CENTER（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit；ets/component/enums.d.ts，ImageFit.Contain）
针对本应用要查的：
- 各带权子项的权重、容器的 weightSum 和方向：源工程布局 XML 里这个 LinearLayout 的 android:orientation、android:weightSum，和各子项的 android:layout_weight、layout_width / layout_height；orientation 定主轴；weightSum 没写时用各权重之和；子项顺序按 XML 里的先后
- 图片的固有尺寸（dp）：源工程 res 下引用该图片的 drawable-*dpi 目录里的图片文件；读出像素宽高，除以所在密度目录的系数（mdpi 为 1、hdpi 1.5、xhdpi 2、xxhdpi 3）得到 dp；例：mdpi 目录下的 272×455px 就是 272×455dp
来源：2 张卡，2 个应用
- case-4e7e0e12d7b6b08c08b0（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2、诊断
- case-85db2e28957bc67387d9（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 诊断
