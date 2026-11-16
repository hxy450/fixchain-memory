# 给 Compose Icons.* 补 SVG 取 Material Icons，不取 Material Symbols

审的是：资源
触发（任一种）：
- 读到：Compose 源里 Icons.Outlined.* / Icons.Filled.* 图标，res/drawable 里没有对应文件；资源参考给的下载地址是 materialsymbolsoutlined/{name}/default/24px.svg；写错的样子：media 下补的 SVG 是 viewBox="0 -960 960 960"（Material Symbols 坐标系），或留着 fill="none" 的透明包围盒 path
适用范围：资源补齐阶段，为 Compose material-icons 库的图标下载 SVG 放进 media 时
做法：
- 从 google/material-design-icons 的 src/<category>/<name>/materialicons/24px.svg（Filled）或 materialiconsoutlined/24px.svg（Outlined）下载，这一套与 Compose material-icons 同源，viewBox 是 0 0 24 24
- 下载后抽查一枚的 viewBox 与外形，并删掉 fill="none" 的包围盒 path
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Material Icons 的 24px.svg 是 viewBox 0 0 24 24；Material Symbols 是 viewBox 0 -960 960 960，两套外形不同：看 viewBox 就能分出取错了族（出处：卡里修好并验证过）
- 返修下载 124 枚 Material Icons 原矢量、剥离透明包围盒后替换全部图标：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4f4db97a21303734c63e（jerboa）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断；取值 2 ← 诊断
