# 组件里读取的 Compose 主题色

agent 会看到什么：读到 Compose 组件取 MaterialTheme.colorScheme.X 或自定义 Theme.colors.X（经 CompositionLocal 下发）；产物里对应的颜色写成名字相近的资源、浅色常量，或在字段初始化器、@Param 默认值里只取一次

## 通用查法

### 源端颜色取自 Compose 主题对象时，按主题文件解析明暗两套实际值，再落到目标主题令牌

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

## 规矩

- rule-d01dc69b2244｜源端用 textPrimary 这类主题语义色时，先解析实际值再选资源，缺令牌就报告或补同值令牌｜读到：Compose 源码里 Text / Icon 的 color = …Theme.colors.textPrimary、iconPrimary 这类主题语义色；写错：目标写成 fontColor($r('app.color.text_secondary')) 这类名字相近的已有资源；目标 color.json 里没有对应令牌，也没报 `design_tokens_missing`
- rule-c96c01b5dae2｜源端颜色取 MaterialTheme.colorScheme 又要插值时，端点读主题令牌，不写浅色常量｜读到：源码颜色写 lerp(MaterialTheme.colorScheme.surface, MaterialTheme.colorScheme.surfaceContainer, …)，主题里有 darkColorScheme 并按 isSystemInDarkTheme() 切换；写错：目标页面把插值端点写成浅色色值常量（0xFF…… 或 '#……' 十六进制），理由「Resource 无法数值插值故内联」；注释写「以后由主题切片统一」却没登记
- rule-c3c66f6a7b0c｜源端在组合期读主题色时，目标在 build() 或 getter 里取色，不写进字段初始化器和 @Param 默认值｜读到：Compose 组件在 @Composable 函数体里读主题对象的 colors（经 CompositionLocal 下发），或把主题色写成参数默认值（每次组合求值）；写错：ArkTS 组件写 `private colors = 取色函数()` 这类字段初始化器，或 `@Param colors: ... = 取色函数().某色` 默认值，构造期只取一次
- rule-af845f858cb4｜源码读 MaterialTheme 颜色和字体时，目标经单一主题入口取值，不写某套 light 值的静态 $r｜读到：Compose 源码里 MaterialTheme.colorScheme.xxx、MaterialTheme.typography.xxx 读值，源端有多套 lightColorScheme / darkColorScheme 色板、明暗模式或字号缩放；写错：用 $r('app.color.…')、$r('app.float.…') 直接绑定某一套色板的 light 色值和 M3 字号；接收颜色的参数类型写成 Resource；没有登记 FWD-REF
- rule-c00db90636c7｜源端应用内切深浅档和多套调色板时，页面主题色读主题对象的令牌，不用 $r 资源色｜读到：Compose MaterialTheme(colorScheme = if (darkTheme) palette.dark else palette.light) 包住全部页面，darkTheme 和 palette 来自应用内设置（Light/Dark/System、多套调色板）；写错：页面和组件里调色板角色色写成 $r('app.color.<角色>') 或 getColorSync 取资源色；按压层、禁用色用按默认调色板预混的资源色
- rule-43f7547bd8ee｜MaterialTheme.colorScheme 取色改读共享主题状态，不直接 import LightColors｜读到：主题函数按 isSystemInDarkTheme() 在 DarkColors / LightColors 间选择并经 MaterialTheme(colorScheme = …) 下发；组件取色写 MaterialTheme.colorScheme.primary 等；写错：组件或页面 import { LightColors } 后写 LightColors.surface 之类，或保留只有亮色值的本地色板常量；应用壳没读取系统 colorMode
- rule-965a77ffd630｜缓存颜色或在 Canvas 里取色的组件改读主题令牌，并用 @Monitor 监听令牌变化后重绘｜读到：源端 Canvas 或绘制回调里取 MaterialTheme.colorScheme.primary / error / onSurface，颜色随应用内主题设置变化；写错：Canvas 组件声明 Resource 类型的颜色参数（默认 $r(...)），绘制时 getColorSync 取默认资源值；或把颜色缓存在成员里，没有订阅主题变化
- rule-b5b2baab87e6｜源端容器色角色在目标 color 资源里缺失时，补齐或登记，不换成相邻的 surface｜读到：源端用 `colorScheme.surfaceContainer`、`surfaceContainerLow` 等容器色角色（含 NavigationBar、ModalDrawerSheet 的默认容器色）；写错：目标 color.json 里没有这个角色，代码换成相邻的 surface 色，注释写「spec 已登记差异降级」
