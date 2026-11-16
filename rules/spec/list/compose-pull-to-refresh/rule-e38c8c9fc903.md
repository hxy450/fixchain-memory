# 规格映射 PullToRefreshBox 时，写明 M3 指示器外观和内容不随下拉移动

审的是：规格
触发（任一种）：
- 读到：源端 `PullToRefreshBox(isRefreshing, onRefresh)` 用默认 M3 指示器；写错的样子：转换决策表只写「PullToRefreshBox → Refresh { List } / 官方下拉刷新 / 标准映射」，没写指示器外观，也没写内容不随下拉移动
适用范围：规格里给 PullToRefreshBox 这类自带默认视觉的库组件写转换决策时
做法：
- 转换决策里写明指示器外观（M3 默认：40dp 的 surfaceContainerHigh 圆底，primary 弧和箭头，触发阈值 80dp）和「内容不随下拉移动，指示器浮在静止内容上方」
- 写明对目标的要求：Refresh 隐藏系统指示器、自绘指示器、抵消子组件的下拉位移
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 从 API version 11 开始，Refresh 子组件会跟随手势下拉而下移：规格不写明时，目标按默认会让内容随下拉下移（出处：ts-container-refresh.md，Refresh）
- M3 默认指示器：40dp surfaceContainerHigh 圆，primary 弧 / 箭头，阈值 80dp，内容不随下拉移动：规格里该写的外观和行为（出处：卡里修好并验证过）
- builder?: CustomBuilder：Refresh 自定义刷新区域显示内容的参数，规格要求自绘指示器时落在这里（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshOptions.builder）
针对本应用要查的：
- 源端下拉刷新指示器的具体外观：源码调用处是否传了自定义 indicator；没传的，查源工程依赖的 androidx.compose.material3 版本（依赖声明或 Compose BOM）里 PullToRefreshDefaults 的尺寸、颜色角色和阈值；自定义的照它写；默认的按该版本的值写进规格，颜色角色再按应用主题解析到色值
未核实：M3 指示器的 40dp、80dp 和颜色角色出自卡，本机 material3 只有编译产物，没核到原文
来源：1 张卡，1 个应用
- case-f0512caa793e1ad8016c（jerboa）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 2 ← 建议 3
