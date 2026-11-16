# 源端颜色取 MaterialTheme.colorScheme 又要插值时，端点读主题令牌，不写浅色常量

审的是：代码
触发（任一种）：
- 读到：源码颜色写 lerp(MaterialTheme.colorScheme.surface, MaterialTheme.colorScheme.surfaceContainer, …)，主题里有 darkColorScheme 并按 isSystemInDarkTheme() 切换；写错的样子：目标页面把插值端点写成浅色色值常量（0xFF…… 或 '#……' 十六进制），理由「Resource 无法数值插值故内联」；注释写「以后由主题切片统一」却没登记
适用范围：源端颜色来自明暗双色板、目标需要对颜色做数值插值时
做法：
- 插值端点从工程主题层的令牌对象读取（主题模块按明暗导出的 colors.surface / colors.surfaceContainer），不把浅色值复制成页面常量
- 主题层还没建好时，用 FWD-REF 或 registry 的 deferred-work 登记，不只在注释或转换报告里写「以后统一」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 顶栏背景改从主题令牌对象的 surface / surfaceContainer 取值后，深色模式下颜色正确：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 工程里提供明暗两套颜色值的主题令牌：目标工程公共组件或主题模块里导出颜色对象的文件（派工里点名可引用的主题文件）；找到按当前明暗返回 surface 等颜色数值的对象或函数，插值时直接用
来源：1 张卡，1 个应用
- case-d9c2b75062eb57796ca2（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
