# strings.xml 的值整体用双引号包着时，string.json 去掉这对引号、保留引号内首尾空格

审的是：资源
触发（任一种）：
- 读到：values*/strings.xml 里有 <string> 的值整个用一对双引号包着（aapt 写法，多为保留首尾空格，如以空格结尾的前缀片段）；写错的样子：element/string.json 里对应的 value 首尾是字面引号（文件里写成 "\"…\""）；或者去了引号却把引号内的首尾空格 strip 掉了
适用范围：资源迁移阶段用脚本把 strings.xml（含各 locale）转成 element/string.json 时，解码每个 <string> 的值
做法：
- 解码时先看值的两端：有成对、未转义的双引号就去掉这一对，引号内的文字连同首尾空格原样保留，不再对它 strip；然后再还原反斜杠转义
- 缺 key 的 locale 拿 base 值补位时，用的是已经去过引号的 base 值；写完对全部 locale 核对：源里以双引号开头的每个 <string>，目标值等于去掉引号后的文本（含首尾空格），首尾同时是双引号的目标值为 0
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 资源值不带外层引号，保留引号内的首尾空格：返修后各 locale 的 string.json 去掉了语法引号，页面拼接显示正确（出处：卡里修好并验证过）
- {"string": [{"name": "…", "value": "…"}]}：element/string.json 的写法，value 是普通 JSON 字符串，不需要 aapt 的引号语法（出处：resource-categories-and-access.md，资源文件示例）
来源：1 张卡，1 个应用
- case-59da3f8259cbad8d67c1（jerboa）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；取值 1 ← 诊断
