# 自定义组件委托 material3 Snackbar 时，几何按库的 SnackbarTokens 取值

审的是：代码
触发（任一种）：
- 读到：自定义组件直接调用 `androidx.compose.material3.Snackbar`，只覆盖 shape、几种颜色和 `actionOnNewLine`；写错的样子：目标自绘 Snackbar 写死带库出处注释的常量（单一 `minHeight` 48、文本垂直内距 14），没有多行高度和左右内距
适用范围：组件几何全部由 material3 库决定、源工程里没有库源码，迁成 ArkUI 自绘实现时
做法：
- 几何从应用依赖的 material3 版本的 SnackbarTokens 或 Snackbar 源码取：单行容器高 48、多行 68，文本垂直内距 6、左右 16
- 思考中带问号或决定不深究的数值，不写成带库出处注释的常量；取不到就在规格或报告里标为缺口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 单行容器高 48、多行 68，文本 padding 垂直 6、左右 16：改成这组值后，用 Android 布局 dump 的 68dp 复核过（出处：卡里修好并验证过）
针对本应用要查的：
- 应用依赖的 material3 版本里 Snackbar 的容器高度和内距：源工程 Gradle 依赖里 androidx.compose.material3:material3 的版本（或 compose BOM 映射到的版本），对应版本库源码的 SnackbarTokens 和 Snackbar.kt；读单行、多行容器高度和文本内距常量，换成 vp 写进目标组件
来源：1 张卡，1 个应用
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 建议 6；取值 1 ← 诊断
