# Uri.parse().path、Base64.decode(DEFAULT)、getType 照 AOSP 逐分支移植

审的是：代码
触发（任一种）：
- 读到：源码 Uri.parse(path).path 取路径后再判前缀；写错的样子：目标对原始串直接 replace(/\/+/g, '/') 后判 startsWith('/data')，file:///data/… 被放行
- 读到：源码 Base64.decode(value, Base64.DEFAULT)；写错的样子：目标手写宽松的 Base64 解码：只跳过 \n \r \t 和空格，其它字符 throw new Error(...)，'=' 只按个数校验
- 读到：源码 ContentResolver.getType(uri)，为 null 才回退 MimeTypeMap；写错的样子：目标用 Record<string, string> 静态扩展名表，未知扩展名返回 '' 并一路透传
适用范围：把 AOSP 平台类（android.net.Uri、android.util.Base64、ContentResolver）的解析、解码和默认值翻译成 ArkTS 时
做法：
- Uri.parse(path).path：先剥掉 scheme 和 authority，再做百分号解码，然后才判前缀
- Base64.decode(DEFAULT) 照 AOSP 解码状态机逐状态移植：字母表外的字符跳过，'=' 可省、有就要个数正确
- getType 对未知扩展名回退 application/octet-stream 再归类；写「等价」注释前用 file:///data/… 路径、含空白或非法字符的 Base64 自测
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Uri#getPath 返回解码后的路径：要先解析出 path 再百分号解码（出处：android.net.Uri#getPath）
- 结尾的 '=' 可省，但只要出现就必须个数正确：padding 规则（出处：android.util.Base64#decode）
- 解码表里字母表以外的字符是 SKIP（-1）：非法字符跳过而不是报错（出处：android.util.Base64.Decoder#SKIP）
- 修好后完整移植 Uri 解析和百分号解码、逐状态移植 AOSP 解码状态机、未知 MIME 回退 application/octet-stream 再归一：修好后的做法（出处：卡里修好并验证过）
未核实：未知扩展名默认 application/octet-stream 出自卡，卡里也注明没有输入写明 FileProvider 的默认值
来源：1 张卡，1 个应用
- case-e9189514e875ef00f96f（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1、建议 2；取值 4 ← 诊断
