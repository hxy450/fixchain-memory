# 规格写权重布局时同时写 weightSum 和子权重之和，标出溢出和份额为 0 的项

审的是：规格
触发（任一种）：
- 读到：源布局 LinearLayout 写了 android:weightSum，和子项 android:layout_weight 之和不等；写错的样子：规格只列各子项权重（如「weight 4 / weight 1 / weight 9」），没写 weightSum、子权重合计，也没写哪块溢出被裁、哪几项份额为 0
适用范围：规格提取时描述安卓 LinearLayout 权重布局的那一节
做法：
- 每个权重布局写成：「weightSum=S，子权重 w1/w2/… 合计 T」；T > S 时写明末块溢出被裁，T < S 时写明留白的份额；剩余 weightSum 分完后的子项写明份额为 0、只保留自然尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- weightSum：Defines the maximum weight sum. If unspecified, the sum is computed by adding the layout_weight of all of the children.：weightSum 写了就按它做分母，和子权重和不是一回事（出处：Android SDK 平台资源 data/res/values/attrs.xml，LinearLayout 的 weightSum（按应用的 compileSdk 取对应平台））
- share = (int) (childWeight * remainingExcess / remainingWeightSum)，分母从 weightSum 起逐项递减：按这个顺序算才能写出哪项溢出、哪项份额为 0（出处：android.widget.LinearLayout#measureVertical）
来源：1 张卡，1 个应用
- case-4e7e0e12d7b6b08c08b0（Privacy Friendly 2048）：做法第 1 步 ← 建议 4
