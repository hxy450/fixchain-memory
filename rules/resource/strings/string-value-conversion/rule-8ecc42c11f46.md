# strings.xml 转 string.json 时按 aapt2 编译语义算值：折叠空白、剥引号、还原转义

审的是：资源
触发（任一种）：
- 读到：源 values*/strings.xml 的 <string> 值跨行书写（换行加缩进），或含 `\n`、`\t`、`\uXXXX`、`\'`、`\"` 转义，或含成对未转义的双引号；写错的样子：string.json 的 value 里残留字面反斜杠加 n（JSON 里写成 `\\n`），或出现换行后跟多个空格的源 XML 缩进；转换脚本只做 strip()、只替换部分转义
适用范围：资源转换阶段把安卓 strings.xml 批量转成 resources/*/element/string.json（目标运行时原样显示 value，不再经过 aapt2）
做法：
- 按 aapt2 编译语义计算每个 value：引号外的连续空白（含换行和缩进）折叠成一个空格并去掉首尾空白；成对的未转义双引号只保护其中的空白，输出时剥离；`\n`、`\t`、`\uXXXX`、`\'`、`\"` 还原成对应字符
- 写完检查 string.json：value 里不应有字面反斜杠加 n，也不应有换行后跟多个空格；有原版 APK 时用 aapt2 dump resources 逐条比对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按 aapt2 语义重算（引号外空白折叠、引号切换并剥离、\n/\t/\uXXXX/\' 还原）后，与原版 APK 的 aapt2 dump 逐条一致：卡里的修法和核对方式（出处：卡里修好并验证过）
未核实：aapt2 的空白折叠与引号规则出自卡，本机没有找到可核对的原文
来源：1 张卡，1 个应用
- case-c2c3a0497bb10ae9aa9a（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；取值 1 ← 诊断
