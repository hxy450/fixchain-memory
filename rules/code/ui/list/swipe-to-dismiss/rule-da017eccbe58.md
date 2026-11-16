# 源用 SwipeToDismissBox 默认阈值时，按依赖版本查默认值实现，不写 50% 近似

审的是：代码
触发（任一种）：
- 读到：rememberSwipeToDismissBoxState(confirmValueChange = …) 没传 positionalThreshold，SwipeToDismissBox 用默认阈值；写错的样子：代码里写死一个比例阈值（如 0.5、注释「positionalThreshold 默认 50% 近似」），没有速度阈值，也没有登记待核
适用范围：源端依赖 Compose Material3 SwipeToDismissBox 的默认阈值或吸附动画，迁成 ArkUI 滑动删除时
做法：
- 按源依赖的 material3 版本查默认的位移阈值、速度阈值和吸附动画，按「位移达到阈值或速度达到阈值即触发」实现
- 查不到默认值时登记待核验占位，不用猜测值静默实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- material3 1.4.0-alpha17 下按默认改成位移 56vp 或速度 125vp/s 触发：修好后的阈值（随依赖版本而变，换版本要重查）（出处：卡里修好并验证过）
针对本应用要查的：
- SwipeToDismissBox 默认的位移阈值、速度阈值和吸附动画：应用依赖的 androidx.compose.material3:material3 版本的库源码里 SwipeToDismissBox、rememberSwipeToDismissBoxState 和它们的默认值定义；读出默认 positionalThreshold 和速度阈值的 dp 数值，按 vp 写进目标的触发判断；例：material3 1.4.0-alpha17 下是 56dp 和 125dp/s
未核实：默认阈值出自库代码，本机只有编译产物，没能逐字核实
来源：1 张卡，1 个应用
- case-7ced02d9c41ab6f4919a（Cofi）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 建议 6；取值 1 ← 诊断
