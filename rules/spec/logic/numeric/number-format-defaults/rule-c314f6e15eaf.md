# 格式化函数的规格写全舍入模式、区域小数点和 Float 转串规则，判例和舍入模式一致

审的是：规格
触发（任一种）：
- 读到：源码用 DecimalFormat("0.#" / "0.00")、toBigDecimal().setScale(…, HALF_EVEN) 或 Float 的 toString 生成显示文本；写错的样子：规格写了「DecimalFormat 默认 HALF_EVEN」，验收判例却写「四舍五入（15.25→"15.3"）」；或没写区域小数点和 Float→String 规则
适用范围：规格提取阶段，数值格式化函数的映射表、算法说明和验收条目
做法：
- 格式化函数的规格同时写三项：舍入模式（DecimalFormat 默认 HALF_EVEN）、小数点取默认区域、Float→String 按 Kotlin Float.toString（整数值带 .0）
- 验收判例和同一文件写的舍入模式一致：HALF_EVEN 配 15.25→"15.2" 这类例子，不配「四舍五入」式的例子
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DecimalFormat 默认舍入模式是 HALF_EVEN（中点取偶）：判例要按中点取偶写（出处：android.icu.text.DecimalFormat#setRoundingMode）
- new DecimalFormat(pattern) 用默认区域的符号：规格要写小数点随区域（出处：android.icu.text.DecimalFormat#DecimalFormat(String)）
- "0.#" 下 15.25→"15.2"，德语区域 12.5→"12,5"，30f→"30.0"：可直接放进验收条目的判例（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-90117ca805576dda1534（Cofi）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 3 ← 建议 1
