# strings.xml 的值里有 <p>、<a>、<b> 等子元素时，取完整文本，不能只取 el.text

审的是：资源
触发（任一种）：
- 读到：源 strings.xml 的 <string> / <item> 值里含没包 CDATA 的 <p>、<a>、<b> 等子元素，或者值以子元素开头；写错的样子：目标 string.json 里这一项的 value 是空串 ""，或只剩第一个子元素之前的文字（转换用 el.text 取值）
适用范围：用脚本解析安卓 strings.xml / plurals 并转成鸿蒙 element JSON 时，值是混合内容的项
做法：
- 解析 <string> / <item> 时用 itertext() 或等价方式取整段文本，保留子元素里的文字
- 写完后逐语言对照源 XML：源值非空而目标为空的项全部列出复核
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 用 itertext() 补回以 <p> 开头的值：修好后的取值方式（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bf53fdebb87671d9eba3（Cofi）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 1 ← 诊断
