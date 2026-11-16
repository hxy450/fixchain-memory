# 数值格式化的舍入模式和区域

agent 会看到什么：源端用 DecimalFormat / NumberFormat / String.format / setScale 生成显示文本，调用里有没有显式写舍入模式和 Locale；规格映射行和验收判例里的舍入、小数点、分组符说法

## 通用查法

### 源端数值格式化没显式写舍入模式或 Locale 时，规格写出它实际取的默认值

审的是：规格
触发（任一种）：
- 读到：源端 new DecimalFormat(pattern)、NumberFormat 或 String.format 生成显示文本，调用里没有显式传 RoundingMode 或 Locale；写错的样子：规格的映射行或验收判例对舍入、小数点、分组符只写「四舍五入」「取系统 Locale」这类说法，或者干脆没写
适用范围：规格提取阶段，数字、金额、时长等格式化函数的映射行、算法说明和验收判例
做法：
- 逐个格式化调用看有没有显式给舍入模式和 Locale；没给的按类的默认写进映射：DecimalFormat 舍入默认 HALF_EVEN，按 pattern 构造时分组符和小数点取默认 Locale
- 默认 Locale 按源工程有没有设应用语言来定：设了是应用语言，没设是系统语言；映射写「Locale.getDefault() = 应用语言 → i18n.System.getAppPreferredLanguage()」
- 验收判例按写下的舍入模式和区域演算，不配和它矛盾的例子（例："0.#" 在 HALF_EVEN 下 15.25→"15.2"）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DecimalFormat 默认舍入模式是 HALF_EVEN（中点取偶）：没显式设舍入模式时判例按中点取偶写（出处：android.icu.text.DecimalFormat#setRoundingMode）
- DecimalFormat(String pattern) 用默认 FORMAT locale 的符号：没传 Locale 时分组符、小数点来自默认 locale（出处：java.text.DecimalFormat#DecimalFormat(String)）
- 安卓设置了应用语言（per-app locale）时，Locale.getDefault() 是应用语言而不是系统区域：源端「默认 Locale」的真实含义（出处：卡里修好并验证过）
- static getAppPreferredLanguage(): string：i18n.System 上取应用偏好语言（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，System.getAppPreferredLanguage）
针对本应用要查的：
- 源端的默认 Locale 是应用语言还是系统语言：源工程的 Kotlin / Java 代码里按 AppCompatDelegate.setApplicationLocales 找设置应用语言的调用；找到了就把默认 Locale 写成应用语言（例：系统语言英语、应用语言德语时小数点显示为逗号）；找不到写系统语言
未核实：族里规矩只核实了 DecimalFormat：NumberFormat、String.format 不传 Locale 时取哪个默认 Locale 类别、NumberFormat 的默认舍入模式没有核实；HALF_EVEN 的默认出自 android.icu.text.DecimalFormat 的声明，java.text.DecimalFormat 的默认舍入模式族里规矩没有另查
来源：2 张卡，2 个应用
- case-6aa988142168e8fded35（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
- case-90117ca805576dda1534（Cofi）：做法第 1 步 ← 建议 2；做法第 3 步 ← 建议 2

## 规矩

- rule-c314f6e15eaf｜格式化函数的规格写全舍入模式、区域小数点和 Float 转串规则，判例和舍入模式一致｜读到：源码用 DecimalFormat("0.#" / "0.00")、toBigDecimal().setScale(…, HALF_EVEN) 或 Float 的 toString 生成显示文本；写错：规格写了「DecimalFormat 默认 HALF_EVEN」，验收判例却写「四舍五入（15.25→"15.3"）」；或没写区域小数点和 Float→String 规则
- rule-f3062277415f｜源端数值格式化没传 Locale 时，规格写「默认 Locale = 应用语言」，不改写成系统 Locale｜读到：源端 new DecimalFormat(",##0.00")、NumberFormat 或 String.format 没有显式传 Locale，分组符和小数点取 Locale.getDefault()；写错：规格的映射行或验收写「分组符/小数点取系统 Locale」「千位分组随系统 Locale」，把默认 Locale 写成了系统区域
