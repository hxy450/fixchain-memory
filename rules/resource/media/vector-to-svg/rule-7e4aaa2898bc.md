# 源码引用 Icons.Rounded.* 等命名变体时，SVG 路径从可核来源取，不凭记忆写

审的是：资源
触发（任一种）：
- 读到：Compose 源码用 Icons.Rounded.Check、Icons.AutoMirrored.Rounded.ArrowBack 这类命名变体引用 Material 图标，工程里没有对应的矢量文件；写错的样子：media 下生成的 SVG 路径是 Filled / baseline 形状（如对勾是直角折线 M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.42z），资源映射表却标称「官方 Rounded」，且没写数据来源
适用范围：资源前置阶段为源码引用的 Material 图标变体生成 SVG 时
做法：
- 从可核来源提取对应变体的 pathData（如 Android Studio 自带图标库里 materialiconsround/<名称>/round_<名称>_24.xml，或 Gradle 缓存里的 material-icons 包），并把来源路径写进资源映射表
- 取不到时按派工写 MISSING_ 前缀的显式占位，或登记近似替代，不凭记忆写路径后标称官方
- 写完抽检变体：Rounded 版线端是圆角弧段（如对勾以 M9,16.17L5.53,12.7c-0.39,-0.39 开头），Filled 版是直角折线；不符即未完成
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 对勾的 Filled 版路径 M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.42z；Rounded 版以 M9,16.17L5.53,12.7c-0.39,-0.39 开头：两种变体的辨认样例（出处：卡里修好并验证过）
- 按 materialiconsround/<名称>/round_<名称>_24.xml 的 pathData 重写后，14 个图标里 13 个与凭记忆写的几何不同：凭记忆写的多半是错的变体（出处：卡里修好并验证过）
针对本应用要查的：
- 某个 Rounded 图标的官方 pathData：Android Studio 安装目录里 android.jar 中 images/material/icons/materialiconsround/<名称>/round_<名称>_24.xml；或 Gradle 缓存里 androidx.compose.material:material-icons-extended 包；读矢量 XML 里 <path> 的 android:pathData，原样写进 SVG 的 d 属性，并把来源路径记进资源映射表
来源：1 张卡，1 个应用
- case-4f7163b95249e9ede2ca（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 1 ← 建议 2、诊断；取值 2 ← 诊断
