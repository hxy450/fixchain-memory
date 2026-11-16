# 底色到透明的渐隐遮罩，终点用同 RGB、alpha 为 0 的色，不用 transparent

审的是：代码
触发（任一种）：
- 读到：源端 .fadingEdges(...) 没给 color（缺省 Color.Unspecified，走 FadeClip），内容自身在边缘淡出、不叠颜色；写错的样子：目标遮罩条写成 .linearGradient({ colors: [[底色, 0], [Color.Transparent, 1]] })，或终点写 'transparent'
适用范围：用叠在内容上的「容器底色 → 透明」linearGradient 遮罩条模拟内容淡出时
做法：
- 终点色取起点色同 RGB、alpha 0：'#AARRGGBB' 写成 '#00RRGGBB'（如 `#00${fadeColor.substring(3)}`），不写 'transparent' 或 Color.Transparent
- 起点色是 Resource 或主题令牌时，先解析成具体色值再派生透明版；主题切换时一起重算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Color.Transparent 是 rgba(0,0,0,0)：透明黑，和非黑底色插值时中段带黑（出处：ts-appendix-enums.md，Color）
- 终点用透明黑时与底色插出中段灰带；换成同色 alpha 0 后两端淡入底色、无灰带：修好后的写法和效果（出处：卡里修好并验证过）
针对本应用要查的：
- 遮罩起点用的底色具体值：目标工程里传给遮罩的底色来源：resources/base/element/color.json 按资源名找，或主题令牌表按令牌名找；解析成 '#AARRGGBB' 后把前两位 alpha 换成 00 作终点；主题切换时重新解析
未核实：ArkUI 渐变不按预乘色插值，出自卡里截图对照，声明和文档里没有写
来源：1 张卡，1 个应用
- case-9190f97a15e03668b874（GameOfLife）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
