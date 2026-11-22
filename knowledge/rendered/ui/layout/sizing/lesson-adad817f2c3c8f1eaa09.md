# LinearLayout 的 weightSum 与子权重之和不等，或 wrap_content 子项带权重时，不用 layoutWeight 归一化：余量（可用尺寸减各子项自然尺寸）按 w/剩余 weightSum 依次分配，份额耗尽的子项只留自然尺寸，超出 weightSum 的末块被裁

## 何时使用

界面实现阶段，把 Android LinearLayout 的 layout_weight/weightSum 分配翻译成 ArkUI 尺寸时；规格提取阶段写权重布局时

## 适用情境

源布局声明 weightSum 且与子权重之和不等（如根 weightSum=10 而子权重 4/1/9，列 weightSum=6 而 8 个 wrap_content 子项各权重 1），或 wrap_content 子项带权重、自然尺寸各不相同。 也包括带权重的 wrap_content ImageView 未设 adjustViewBounds、位图按密度放大后宽于父级，各子项自然尺寸之和可能超过可用尺寸（横屏、小屏）。

## 例外与边界

- LinearLayout 主轴尺寸确定（match_parent 或固定值）、带权子项主轴都写 0dp、没写 weightSum 或它等于权重之和时，各子项就是按权重比例分可用尺寸，与 ArkUI layoutWeight 一致：已有的 layoutWeight 写法保留，不按这条改写。带权子项主轴是 match_parent 时不在此列（自然尺寸取父尺寸、余量为负），按做法第 1 步的公式算。

## 原因

ArkUI layoutWeight 按权重和的比例分配全部空间，等于忽略 weightSum 与子项自然尺寸：源端被裁的末块、份额耗尽的子项与留白都会变形。 flexGrow 只在余量为正时按比例增长：自然尺寸之和超过可用尺寸时，LinearLayout 用同一公式给每个带权子项分负份额、逐项扣减，flexGrow/flexShrink 复现不了；自然尺寸取错（如把未设 adjustViewBounds 的图片高按父宽等比缩小），分出的各框尺寸也跟着错。

## 做法

1. 按 LinearLayout 算法计算：先测各子项自然尺寸，余量按权重依次分配（每次除以剩余 weightSum），weightSum 用尽后的子项只保留自然尺寸，总和超出可用尺寸的末块按剩余空间裁切；可按容器实测尺寸算出位置后绝对定位，或用占位补足 weightSum 余下的份额。 份额逐项计算为 share = (int)(w × 剩余余量 / 剩余 weightSum)（android.widget.LinearLayout 的 measureVertical / measureHorizontal，android-36.1 源码），余量为负时同一公式给出负份额、逐项扣减；不交给 flexGrow/flexShrink，显式算出各子项尺寸。
2. 带权重的 wrap_content 图片固有尺寸超过行能给的空间时，只把超限的那一轴夹紧到父级上限；ImageView 未设 adjustViewBounds 时另一轴保持密度缩放后的固有尺寸（位图在盒内 centerInside/FIT_CENTER 缩小绘制，盒子不等比缩小），以此作为自然尺寸代入余量分配，不填经验值；写完抽 2–3 个位置（行中心、分隔线）与源端截图的 dp 对比。
3. 规格写权重布局时同时写 weightSum 与子权重之和，以及溢出、份额为 0 的子项，不只列各子项权重。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕LinearLayout 的 weightSum 是权重总和的上限，不写时等于各子项 layout_weight 之和
- 〔做法第 1 步〕LinearLayout 先测各子项自然尺寸，余量 remainingExcess = 可用尺寸 − 已测总长（可为负）；剩余权重和起始值为 weightSum（写了且大于 0 时）否则为各权重之和；按子项顺序对每个带权子项取 share = (int)(权重 × remainingExcess / 剩余权重和)，再从余量和剩余权重和里各减去这次的 share 和权重；GONE 的子项跳过
- 〔做法第 1、2 步〕带权子项主轴尺寸写 0 时最终尺寸只取 share；有自然尺寸（如 wrap_content）时最终尺寸 = 自然尺寸 + share，按 EXACTLY 下限 0 再测量
- 〔原因〕ArkUI layoutWeight 只在 Row、Column、Flex 中生效，不写时为 0：不设或为 0 的子组件先占位，设了大于 0 的子组件按权重占比分主轴剩余空间，分配时忽略自身 width/height 但保留 minWidth/minHeight；没有 weightSum 这一参数
- 〔原因〕容器里有子组件设了大于 0 的 layoutWeight 时，所有子组件不再按 flexShrink、flexGrow 布局；flexGrow 只分配父容器的剩余空间
- 〔原因〕flexShrink 不写时：父容器是 Column 或 Row 为 0，父容器是 Flex 为 1
- 〔做法第 2 步〕安卓 ImageView 不写 scaleType 时为 FIT_CENTER；adjustViewBounds 默认 false
- 〔做法第 2 步〕安卓 ImageView 没设 adjustViewBounds 时，onMeasure 以 drawable 固有宽高为期望尺寸，宽、高各自用 resolveSizeAndState 按父级约束解算，只有超过上限的那一轴被夹到上限，另一轴保持固有尺寸
- 〔做法第 2 步〕位图从所在目录的密度 sdensity 缩放到设备密度 tdensity 时，像素尺寸 = (size × tdensity + sdensity / 2) / sdensity（整数除法，近似四舍五入）
- 〔做法第 2 步〕drawable 密度目录对应的 dpi：ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640
- 〔做法第 2 步〕Image 的 objectFit 不写时为 ImageFit.Cover，和安卓 ImageView 默认的 FIT_CENTER 不同；ImageFit.Contain 保持宽高比缩放，使图片完全显示在显示边界内
