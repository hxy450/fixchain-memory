# Compose 文本样式的字号、字重和字体族

agent 会看到什么：读到 Compose Text 用 MaterialTheme.typography 的命名样式、FontWeight.SemiBold / Light 或 FontFamily(Font(R.font…))，产物里是 Text 的 .fontSize($r('app.float.…'))、.fontWeight(...)、.fontFamily(...) 和 registerFont

## 通用查法

### Compose 文本带 typography 样式时，按主题定义查出字号、字重、字体族逐项显式写

审的是：代码
触发（任一种）：
- 读到：源 Compose Text 的 style = MaterialTheme.typography.titleMedium 这类命名样式，或带 FontFamily(Font(R.font…, FontWeight…)) 的自定义 TextStyle；写错的样子：目标 Text 的 .fontSize($r('app.float.…')) 借别页的键，.fontWeight(...) 写枚举里没有的成员或就近换成 Medium / Lighter，没写 .fontFamily(...) 或引用未注册的族名
适用范围：源端文本的字号、字重、字体族来自 Compose Typography 或 TextStyle，迁成 ArkUI Text 时
做法：
- 按源码的样式名到源工程定义 Typography(...) 的主题文件读出 fontSize、fontWeight、fontFamily；应用没覆写的样式取 Material3 默认值
- 逐项写显式值：fontSize 引用值相同的 float 键（没有就追加）；fontWeight 写数值（如 600）；fontFamily 写按「族-字重」registerFont 注册过的名字
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontSize(value: number | string | Resource): TextAttribute：Text 的字号；传 number 时单位是 fp（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontSize）
- fontWeight(value: number | FontWeight | ResourceStr): TextAttribute；number 取值 [100, 900]，间隔 100：字重可以直接写数值（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- FontWeight 枚举只有 Lighter、Normal、Regular、Medium、Bold、Bolder：没有 SemiBold、Light，这两种只能写数值（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，FontWeight）
- registerFont(options: font.FontOptions): void：UIContext 的 Font 对象上注册自定义字体，注册名给 .fontFamily 用（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，Font.registerFont）
- 例：源样式 fontWeight = FontWeight.SemiBold 时，改为 .fontWeight(600) 后字重与源一致：带条件的例子（出处：卡里修好并验证过）
针对本应用要查的：
- 这个样式在应用里的字号、字重和字体文件：源工程里定义 Typography(...) 的 Kotlin 主题文件，按样式名找；字体族再顺着 FontFamily(Font(R.font.<文件>, FontWeight.<字重>)) 找；读出 fontSize = N.sp、fontWeight 和每个 Font(...) 的文件名与字重；没在 Typography(...) 里覆写的样式取 Material3 默认值
- 目标端已有的字号键和字体注册名：目标工程 resources/base/element/float.json，以及入口页里调用 registerFont 的地方；找值与样式字号相同的 float 键、与「族-字重」对应的 familyName；没有就新增
未核实：Material3 各命名样式的默认字号、字重，族里规矩没有查实；Compose FontWeight.SemiBold = 600、Light = 300 出自卡，本机没有 Compose 源码
来源：3 张卡，2 个应用
- case-035a088f7930911f5cc9（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2
- case-036361d8949e7daf5247（Cofi）：做法第 2 步 ← 建议 4；取值 5 ← 诊断
- case-cfcb1be64b70e328ad81（Jetsnack）：做法第 2 步 ← 建议 2

## 规矩

- rule-cd0b79a22316｜Compose 文本用 typography 命名样式时，按令牌表查字号再找值一致的 float 键，不借别页键｜读到：源 Compose Text 的 style = MaterialTheme.typography.titleMedium / bodyMedium 这类命名样式；写错：目标 Text 写 .fontSize($r('app.float.…')) 按「标题 / 正文」语义复用别页前缀的键，键值和令牌表里该样式的字号不同
- rule-96b5ad03a26d｜FontWeight.SemiBold/Light 迁成 600/300，不换成 Medium/Lighter｜读到：Compose 源里 fontWeight = FontWeight.SemiBold 或 FontWeight.Light；写错：目标写 .fontWeight(FontWeight.SemiBold) 编译报「Property 'SemiBold' does not exist on type 'typeof FontWeight'」，或被就近替换成 FontWeight.Medium / FontWeight.Lighter
- rule-647c1373f9f7｜源 FontFamily 一族多字重文件时，按「族-字重」逐文件 registerFont，入口调一次｜读到：Compose FontFamily(Font(R.font.x, FontWeight.y), …) 为同一族声明多个字重文件，目标 rawfile/fonts 下有对应 ttf；写错：全工程没有 registerFont，Text 的 .fontFamily 引用未注册的通用族名；或同族多个文件都注册成同一个 familyName
- rule-b352d5315d38｜rawfile 里字体已就位时，页面文本设注册族名，不写「资产未就绪，暂用系统字族」｜读到：源 Text 用带自定义 FontFamily 的 TextStyle；占位登记里有字体 `P-RES-ASSET-…` pending 条目；写错：页面文件头写「rawfile 资产未就绪，暂用系统字族」，Text 只设 fontSize / fontWeight、不设 .fontFamily
