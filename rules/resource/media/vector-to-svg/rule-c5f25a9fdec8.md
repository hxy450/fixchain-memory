# 从 AAR 字节码重建 Material 图标路径时，映射 PathBuilder 全部方法含 arcTo，未映射就报错

审的是：资源
触发（任一种）：
- 读到：源码用 `Icons.Outlined.*` / `Icons.Filled.*` 引用 Compose material-icons 矢量，res 下没有对应 drawable；AAR 里的图标是编译进 class 的 PathBuilder 调用（moveTo、curveToRelative、reflectiveCurveTo、arcToRelative、close）；写错的样子：转出的 SVG 里有只移动不绘制的子路径（如 `m-1.5,0` 后直接是下一个 M/m 或路径结束），图标只画出外框
适用范围：资源迁移时用自写转换器从 material-icons AAR 字节码重建图标的 SVG path
做法：
- 按 PathBuilder 的全部路径方法建映射，arcTo/arcToRelative 写成 A/a：参数依次为两个半径、旋转角、isMoreThanHalf、isPositiveArc（两个布尔按 0/1 写）、终点
- 遇到没有映射的 PathBuilder 调用直接报错停止，不跳过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- A 的参数顺序：rx ry x-axis-rotation large-arc-flag sweep-flag x y；large-arc-flag 大弧 1 小弧 0，sweep-flag 顺时针 1 逆时针 0：isMoreThanHalf 对 large-arc-flag，isPositiveArc 对 sweep-flag（出处：ts-drawing-components-path.md，SVG路径描述规范）
- M：在给定坐标处开始一个新的子路径：只有 M/m 的子路径不画任何东西（出处：ts-drawing-components-path.md，SVG路径描述规范）
- arcToRelative(r, r, 0, true, true, dx, 0) 写成 `a r,r 0 1,1 dx,0`：两个布尔按 0/1 写出的样子；补回弧段后图标完整（出处：卡里修好并验证过）
针对本应用要查的：
- 图标实际用到的 PathBuilder 方法：Gradle 缓存里 material-icons-core / material-icons-extended AAR 的 classes，按源码引用的变体和图标名找对应类；列出该类里所有 PathBuilder 调用的方法名，逐个确认都在映射表里
来源：1 张卡，1 个应用
- case-c09ad7a54d229f947bf8（GameOfLife）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
