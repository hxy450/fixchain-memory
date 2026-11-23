# Compose 以 Brush 渐变着色的背景迁为 linearGradient：把调色板名解析成具体色序，透明 Surface 背景设透明，不压成单一品牌色

## 何时使用

界面实现与共享组件实现阶段，把 Compose 按钮、卡片的 Brush.horizontalGradient(colors.xxx) 背景，或页面里已有的渐变字面色值落为 ArkUI linearGradient 与颜色资源时

## 适用情境

源组件用主题中的渐变列表（如 JetsnackTheme.colors.interactivePrimary、gradient2_2）经 Brush 着色，常配 Surface(color = Transparent)；目标要求颜色走 color.json 资源引用，而 color.json 只收录了调色板的部分色阶。

## 例外与边界

- GradientDirection.Right 只对应 Brush.horizontalGradient；源端是 Brush.verticalGradient 时用 GradientDirection.Bottom（自上而下，也是 linearGradient 不写方向时的默认值），带起止坐标的 Brush.linearGradient 按坐标换算方向或角度，不统一写成 Right。
- linearGradient 的 colors 每项都要带位置：源端没给色标位置时颜色沿渐变线均匀分布，n 个颜色的第 i 个位置取 i/(n−1)；源端给了 colorStops 的按源端的位置写，不要改成等分。

## 原因

调色板名只是颜色列表的别名，不解析就只能用一个品牌色或名称相近的现有令牌代替：按钮从浅紫到深蓝的渐变变成单色块，分类卡的两组渐变被换成错值令牌。来源两例：共享按钮作者读到 Brush.horizontalGradient(interactivePrimary) 仍写 backgroundColor(brand)；页面 worker 把已正确的渐变字面色值替换为三处值不同的现有令牌，没有新增缺失色阶，也没回报缺令牌。

## 做法

1. 源背景是 Brush.horizontalGradient(colors.xxx) 时保留为 linearGradient({ direction: GradientDirection.Right, colors: [...] })，先在主题与 Color 定义中把调色板名解析成具体色阶顺序（如 interactivePrimary = Shadow4 → Shadow11）；源 Surface 为 Transparent 时目标 backgroundColor 也设透明。
2. 渐变色阶用 $r 引用时逐个核对令牌值与源色值；缺的色阶按调色板命名新增条目后引用，或按流程回报 design_tokens_missing。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕linearGradient 的选项里 direction 没写时为 GradientDirection.Bottom（自上而下），angle 没写时为 180；colors 每项是 [颜色, 位置]
- 〔做法第 1 步〕linearGradient 设了非 undefined 的 angle 后 direction 不生效；colors 的位置取值 [0, 1.0]，小于 0 按 0、大于 1.0 按 1.0 处理，多个颜色时位置应递增
- 〔做法第 1 步〕GradientDirection.Right 表示从左到右
- 〔做法第 2 步〕color.json 的标准十六进制颜色值由八位十六进制数字组成，前两位是透明度、后六位是颜色值（如 #ffff0000）
