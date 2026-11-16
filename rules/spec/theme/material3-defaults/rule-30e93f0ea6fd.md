# 规格写了 M3 组件的默认尺寸时，同一组件的标题 inset 和槽位规则一并写出

审的是：规格
触发（任一种）：
- 读到：源是 Compose Material3 TopAppBar 等库组件，源码里没有横向 padding，留白来自库的内部布局；写错的样子：规格或验收项写了「TopAppBar 容器高 64vp（Material3 默认）」这类默认值，却没写标题 inset 在哪一侧、导航/动作槽怎么撑开
适用范围：规格提取阶段为 Material3 TopAppBar 一类库组件写默认外观时
做法：
- 同一组件的默认值一并写：标题 inset 作用在哪一侧、取值（无导航图标时只在起始侧 16dp）、导航/动作槽是否存在及宽度
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 无导航图标时标题只在起始侧有 inset，末端没有；IconButton 贴末端：M3 TopAppBar 标题槽的横向留白（出处：卡里修好并验证过）
针对本应用要查的：
- 这个库组件各槽位的 inset 和宽度：androidx.compose.material3:material3 的组件布局实现（按应用依赖的 compose BOM 版本）；读出每个槽位两侧的留白，按侧写进规格
未核实：M3 内部留白没在本机核实（缓存里没有 material3 源码），按卡写
来源：1 张卡，1 个应用
- case-2280cf8a2bf7682ff26b（Jetsnack）：做法第 1 步 ← 建议 3、建议 1；取值 1 ← 诊断
