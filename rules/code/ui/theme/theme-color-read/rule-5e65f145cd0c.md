# 源端颜色取自 Compose 主题对象时，按主题文件解析明暗两套实际值，再落到目标主题令牌

审的是：代码
触发（任一种）：
- 读到：Compose 组件的颜色取 MaterialTheme.colorScheme.surface 或自定义 Theme.colors.textPrimary 这类主题字段（经 CompositionLocal 下发）；写错的样子：目标写成名字相近的已有 $r('app.color.…') 资源，或把浅色色值写成常量（'#……'、0xFF……），深色下不变
适用范围：把 Compose 主题色迁成 ArkUI 颜色资源或主题令牌时
做法：
- 去源工程 Compose 主题文件（定义颜色数据类、lightColorScheme / darkColorScheme 或自定义调色板的 Kotlin 文件）按字段名找它在浅色、深色两套里的赋值，顺着引用跟到 Color(0x…)
- 在目标主题层找同值令牌：color.json 资源，或按明暗导出颜色数值的主题对象；要做数值插值的读主题对象，不把浅色值复制成常量
- 缺令牌就补同值令牌或报告 `design_tokens_missing`，不拿名字相近的资源代替；主题层没建好时用 FWD-REF 登记
针对本应用要查的：
- 这个主题字段在浅色、深色下的实际值：源工程的 Compose 主题文件：定义颜色数据类的 Kotlin 文件里该字段的默认值，以及 lightColorScheme / darkColorScheme 或自定义调色板对它的赋值；顺着赋值跟到具体的 Color(0x…) 或别的语义字段（例：某主题里 textPrimary 默认取 brand），两套各读出一个值
- 目标工程里同值的颜色令牌：目标工程资源目录下的 color.json，以及公共组件或主题模块里按明暗导出颜色数值的对象（派工里点名可引用的主题文件）；按读出的色值找同值令牌；找不到就是缺令牌
未核实：源端没有自定义 colorScheme、直接用 Material3 默认配色时，各颜色角色的默认值定义在依赖库的哪个符号里，族里规矩没有查过；源端开着动态取色（dynamicLightColorScheme / dynamicDarkColorScheme）时实际色随壁纸变，从主题文件读不出
来源：2 张卡，2 个应用
- case-d9c2b75062eb57796ca2（Cofi）：做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-ed8b01a83bca9f70218f（Jetsnack）：做法第 1 步 ← 建议 2；做法第 3 步 ← 建议 2
