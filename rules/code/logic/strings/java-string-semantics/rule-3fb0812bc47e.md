# 源端用 FileReader/InputStreamReader 读文本时，目标解码后保留 BOM

审的是：代码
触发（任一种）：
- 读到：`BufferedReader` 包着 `FileReader` 或 `InputStreamReader` 读文本文件；写错的样子：目标用 util.TextDecoder（如 new util.TextDecoder('utf-8')）解码后直接断行，没有核对 BOM；以 EF BB BF 开头的文件首行少了 U+FEFF
适用范围：Java Reader 读 UTF-8 文本、迁成 ArkTS 先读字节再解码时
做法：
- 解码后核对：原始字节以 0xEF 0xBB 0xBF 开头而结果首字符不是 '\uFEFF' 时，在结果前补回 '\uFEFF'，再按 Java 语义断行、trim（Java trim 不去 U+FEFF）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FileReader / InputStreamReader 把 BOM 当普通字符保留；util.TextDecoder 解码会丢掉 BOM：两端对 BOM 的处理不同（出处：卡里修好并验证过）
- TextDecoderOptions.ignoreBOM?: boolean，默认 false：TextDecoder 处理 BOM 的选项；文档对 false 的说法和卡里的观察相反，所以解码后要按字节核对（出处：鸿蒙 SDK 的 ets/api/@ohos.util.d.ts，TextDecoderOptions.ignoreBOM）
未核实：卡里没写 TextDecoder 用的构造和选项；卡的环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-526d6b56241863d015dd（MifareClassicTool）：做法第 1 步 ← 建议 1；取值 1 ← 建议 1、诊断
