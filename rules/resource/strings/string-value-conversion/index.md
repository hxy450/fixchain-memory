# strings.xml、arrays.xml 的值转写成 element JSON

agent 会看到什么：源 strings.xml / arrays.xml 的值跨行书写、带 \n \' \" 转义或未转义双引号、含 <p> <a> <b> 子元素，或是 <string-array> 的项；产物 string.json / strarray.json 的 value 残留转义和缩进、为空、数组项是纯字符串、@string/ 引用没改写

## 规矩

- rule-8ecc42c11f46｜strings.xml 转 string.json 时按 aapt2 编译语义算值：折叠空白、剥引号、还原转义｜读到：源 values*/strings.xml 的 <string> 值跨行书写（换行加缩进），或含 `\n`、`\t`、`\uXXXX`、`\'`、`\"` 转义，或含成对未转义的双引号；写错：string.json 的 value 里残留字面反斜杠加 n（JSON 里写成 `\\n`），或出现换行后跟多个空格的源 XML 缩进；转换脚本只做 strip()、只替换部分转义
- rule-b01e574744fe｜strings.xml 的值跨多行书写时，转换先按 aapt2 折叠引号外空白再处理转义｜读到：源 res/values*/strings.xml 或 plurals 里的 <string> / <item> 值跨多行书写：正文后有物理换行和缩进，下一行行首再写 \n 转义；写错：目标 string.json 的 value 里出现 \n\n 双换行或残留的缩进空格（转换只 strip() 了首尾就把 \n 转成换行）
- rule-3a3e5291bcfd｜strings.xml 值中间有未转义双引号时，string.json 里去掉它，只有 \" 转义的保留｜读到：源 strings.xml 的 `<string>` 文本中间出现前面没有反斜杠的 `"`（不是整值首尾包裹，形如 文字 "词" 文字）；写错：目标 string.json 对应的 `value` 里残留这对引号（JSON 里写成 `\"`），或转换脚本只在值首尾都是 `"` 时才剥引号
- rule-b31bc76f2bdf｜strings.xml 的值里有 <p>、<a>、<b> 等子元素时，取完整文本，不能只取 el.text｜读到：源 strings.xml 的 <string> / <item> 值里含没包 CDATA 的 <p>、<a>、<b> 等子元素，或者值以子元素开头；写错：目标 string.json 里这一项的 value 是空串 ""，或只剩第一个子元素之前的文字（转换用 el.text 取值）
- rule-347fb582d261｜string-array 转 strarray.json 时每项写成 value 对象，镜像到限定目录前先自检结构｜读到：源端 values/arrays.xml 里的 <string-array>（或 <integer-array>、<plurals>）；写错：element/strarray.json 写成 {"name": n, "value": ["…", "…"]}，数组项是纯字符串；编译报 `The value type of node 'value's child' does not match. Expected type: object`
- rule-9cf5fdb4d1b9｜数组资源项里的 @string/ 等引用同样改写成 $string: 形式，并检查全文件无残留｜读到：源端 <string-array> 的 <item> 写成 @string/name 等资源引用；写错：strarray.json 的数组项原样保留 `@string/`；转换脚本只对 string、integer、bool 标量做了引用改写
- rule-f18e77438e1c｜带 <b>/<a>/CDATA 的 strings.xml 串按 HTML 存进 string.json 并列清单｜读到：strings.xml 的 <string> 里内联 <b> / <i> / <u> / <a href> / <br>，或用 <![CDATA[ … ]]> 包 HTML；写错：string.json 里这些键的标记和 href 被丢掉成了纯文本，转换脚本用 ''.join(el.itertext()) 之类只取文本的写法；或 CDATA 键原样留着 HTML 却没人登记
- rule-db73b1503125｜strings.xml 的值带反斜杠转义时，转成 string.json 前全部还原，不留反斜杠｜读到：values*/strings.xml 的 <string> 值里有 \'、\"、\@、\?、\#、\\、\n、\t、\uXXXX 这类反斜杠转义；写错：element/string.json 的 value 里还留着反斜杠加字符（文件里是 \\@、\\? 这样），或者只还原了 \' 和 \" 两种
- rule-33da03ce179a｜strings.xml 的值整体用双引号包着时，string.json 去掉这对引号、保留引号内首尾空格｜读到：values*/strings.xml 里有 <string> 的值整个用一对双引号包着（aapt 写法，多为保留首尾空格，如以空格结尾的前缀片段）；写错：element/string.json 里对应的 value 首尾是字面引号（文件里写成 "\"…\""）；或者去了引号却把引号内的首尾空格 strip 掉了
- rule-2ad8bbb9e4a2｜string-array 条目引用 @string/ 时，strarray.json 不原样保留 '@string/…'｜读到：res/values 里 <string-array> 的 <item>@string/…</item>（如 ListPreference 的 android:entries 数组）；写错：strarray.json 的 value 原样是 "@string/…" 这种安卓语法，zh_CN 等语言目录也照样复制
