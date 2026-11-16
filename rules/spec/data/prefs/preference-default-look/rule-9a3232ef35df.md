# 三方 UI 组件在本仓没有源码时，规格只写调用点可见的结构，不写未核实的装饰

审的是：规格
触发（任一种）：
- 读到：ProvidePreferenceTheme 里直接排列 Preference(title, icon, onClick)，调用点没有 divider，也没有尾部图标；库（me.zhanghai.compose.preference）在本仓没有源码；写错的样子：规格写「Preference 自带分隔线/内边距主题」，转换决策给每行加 chevron_right，或给出行高等未查实的近似几何值
适用范围：规格提取阶段，源端用本仓没有源码的三方 Compose/View 组件时的页面结构和转换决策
做法：
- 只写调用点可见的结构（如「Column 内直接排列，无 divider，无尾部图标」），不把「自带分隔线」「chevron」这类未核实的装饰写进转换决策
- 需要库的默认几何时，先到依赖缓存或 sources/aar 里查实；查不到就在规格里标「待核」，不给近似值
针对本应用要查的：
- 三方 UI 库的默认几何（行高、图标槽宽、内边距）：Gradle 缓存里该库的 aar 或 sources jar（按应用依赖的版本，坐标如 me.zhanghai.compose.preference）；有 sources 读默认参数；只有 class 的用 javap 读常量；都没有就在规格里标「待核」
来源：1 张卡，1 个应用
- case-69c1c089176794fbe5db（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
