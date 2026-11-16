# LinearLayout 的权重子项（layout_weight、weightSum）

agent 会看到什么：读到 LinearLayout 子项带 android:layout_weight（XML 里或代码的 LayoutParams 里），可能还有 android:weightSum；产物里这些子项的 .layoutWeight、.flexGrow、.width('100%') 或算出来的显式尺寸

## 通用查法

### LinearLayout 子项带 layout_weight 时先读主轴尺寸和 weightSum 再定写法

审的是：代码
触发（任一种）：
- 读到：LinearLayout 子项带 android:layout_weight 或代码里 LayoutParams 的 weight，可能有 android:weightSum；写错的样子：子项一律写 .layoutWeight(w)、.flexGrow(1)，或留着 .width('100%')
适用范围：LinearLayout 的权重分配迁成 Row / Column 时
做法：
- 从源布局 XML 或代码的 LayoutParams 读 orientation、weightSum、各子项的 layout_weight 和主轴尺寸
- 主轴尺寸为 0、没写 weightSum 的写 .layoutWeight(w)，去掉主轴的 .width('100%')
- wrap_content 带权或 weightSum 与权重和不等的，按 LinearLayout 算：余量 = 可用尺寸 − 自然尺寸之和，逐项 share = Math.trunc(w × 余量 / 剩余权重和)，尺寸 = 自然尺寸 + share，写成显式宽高
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- final int share = (int) (childWeight * remainingExcess / remainingWeightSum); remainingExcess -= share; remainingWeightSum -= childWeight;：安卓逐个带权子项分余量的公式，余量可为负（出处：android.widget.LinearLayout#measureVertical（横向同在 measureHorizontal））
- float remainingWeightSum = mWeightSum > 0.0f ? mWeightSum : totalWeight;：剩余权重和的起始值：写了 weightSum 用它，否则用各权重之和（出处：android.widget.LinearLayout#measureVertical）
- childHeight = child.getMeasuredHeight() + share：有自然尺寸的权重子项，最终尺寸是自然尺寸加分到的余量；主轴尺寸为 0 时才只取 share（出处：android.widget.LinearLayout#measureVertical）
- layoutWeight 分配时会忽略元素本身的尺寸设置：wrap_content 加权重的子项不能直接写成 layoutWeight；layoutWeight 也没有 weightSum 这一参数（出处：ts-universal-attributes-size.md，layoutWeight）
针对本应用要查的：
- 各带权子项的权重、主轴尺寸，容器的 weightSum 和方向：源工程布局 XML 里这个 LinearLayout 的 android:orientation、android:weightSum 和各子项的 android:layout_weight、layout_width / layout_height；子项由代码添加的，按 LayoutParams( 找添加子项的那段；orientation 定主轴；weightSum 没写时用各权重之和；子项顺序按 XML 或添加的先后。例：代码以 LayoutParams(0, MATCH_PARENT) 加 weight = 1f 添加的等分子项，写 .layoutWeight(1)
来源：3 张卡，3 个应用
- case-4e7e0e12d7b6b08c08b0（Privacy Friendly 2048）：做法第 3 步 ← 建议 1
- case-85db2e28957bc67387d9（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-ce3a01377b3cd72f23e3（实时公交）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 1

## 规矩

- rule-342c1fca2d17｜等分子项搬进自绘 Row/Column 时写 .layoutWeight(1)，不留 .width('100%')｜读到：安卓水平 LinearLayout 没有静态子项，子项由代码以 LinearLayout.LayoutParams(0, MATCH_PARENT) 加 weight = 1f 等分；写错：目标 Row + ForEach 里每个子项写 .width('100%')，没有 .layoutWeight(...)
- rule-bf6ea1fc9746｜LinearLayout 带权 wrap_content 子项按 share 公式显式算尺寸，不用 flexGrow｜读到：LinearLayout 下多个子项为 wrap_content 且带 android:layout_weight（可能还有 android:weightSum）；写错：目标里这些子项写成 Flex / Column 里的 .flexGrow(1) 或 .layoutWeight(1) 交给框架分余量，没有显式算出各框的尺寸；自然尺寸之和超过可用尺寸时框高不对
- rule-f9c3410a112c｜weightSum 与子权重和不等时按 LinearLayout 算法算尺寸，不用 layoutWeight｜读到：LinearLayout 写了 android:weightSum，且和子项 android:layout_weight 之和不等（子权重和大于或小于 weightSum）；写错：子项照各自权重写成 .layoutWeight(w)，等于按权重和归一化、丢掉 weightSum；或注释写着「按相对比例复现」
