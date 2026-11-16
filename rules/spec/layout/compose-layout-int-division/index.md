# Compose 自定义 Layout 在 constraints 上的 Int 整除

agent 会看到什么：源端 Compose 自定义 Layout / MeasureScope 在 constraints.maxWidth、placeable 宽高上做 Int 整除或 .toInt() 截断，规格里把这条公式写成 vp 域、或只给整数宽的用例

## 规矩

- rule-10c5afb28e91｜Compose Layout 对 constraints 整除或 .toInt() 时，规格写明在 px 域算｜读到：Compose 自定义 Layout / MeasureScope 里在 constraints.maxWidth、placeable 宽高上做 Kotlin Int 整除或 .toInt() 截断（如 constraints.maxWidth / (itemCount + 1)）；写错：规格把这条公式写成 vp 域整除（W 标「vp，整数」、注释对应 constraints.maxWidth，u = floor(W/(n+1))），把 onAreaChange 的回调宽写成「vp，整数」，映射表写「measureText 返回 px，须 px2vp 后进入 vp 域公式」
- rule-f03620947978｜规格给整除公式写用例和等价声明时，放非整数 vp 宽与对应 px 宽，两个域各算一遍｜读到：Compose 自定义 Layout 里在 constraints.maxWidth 上做 Int 整除来分配槽宽；写错：公式的用例只用整数宽（如 W=360、361）；或者写「W 不能被 n 整除时右侧留 W mod n vp 空白，Android 原样」这类等价性声明，没有按 px 和 vp 各算一遍
