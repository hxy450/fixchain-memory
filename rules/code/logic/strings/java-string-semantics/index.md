# Java 读行和字符串处理的语义

agent 会看到什么：源端用 BufferedReader.readLine、FileReader / InputStreamReader、String.split、String.trim 处理文本，对应目标的 split('\n')、JS trim()、util.TextDecoder 解码和各处的兼容函数

## 规矩

- rule-1652faf6733b｜源端 BufferedReader.readLine 逐行读时，目标按 \n、\r、\r\n 断行且末尾不多出空行｜读到：`BufferedReader.readLine()` 循环逐行读文件（常接着 line.trim()）；写错：目标读全文后 split(/\r\n|\r|\n/) 或 split('\n') 直接当行列表，文件以换行结尾时最后多出一个空串行；或只按 '\n' 断行，裸 \r 不断行
- rule-3fb0812bc47e｜源端用 FileReader/InputStreamReader 读文本时，目标解码后保留 BOM｜读到：`BufferedReader` 包着 `FileReader` 或 `InputStreamReader` 读文本文件；写错：目标用 util.TextDecoder（如 new util.TextDecoder('utf-8')）解码后直接断行，没有核对 BOM；以 EF BB BF 开头的文件首行少了 U+FEFF
- rule-49e9b477a1ce｜源端 String.split 切分文本时，目标切分后去掉结果末尾的空串｜读到：`getText().split(System.getProperty("line.separator"))` 或其他单参数 String.split(regex) 调用；写错：目标写 text.split('\n') 后直接用结果数组，以分隔符结尾的文本多出末尾空串，行数判定因此出错
- rule-6669910c515a｜源端 String.trim 时，目标只去首尾码点 ≤U+0020 的字符，不用 JS trim()｜读到：`line.trim()`（java.lang.String#trim）；写错：目标直接用 JS 的 .trim()，注释写着「trim 语义与 Java 一致」
- rule-6f700eaf75b4｜多处要用 Java 字符串和读行语义时，集中实现一组兼容函数，各处统一调用｜读到：源端多个类都用 readLine、String.split、String.trim、String.format 处理文本；写错：两个以上服务、VM 或页面各自写读行、切分、去空白、解码的近似实现（各自的 split('\n')、.trim()、TextDecoder）
- rule-4ff8147164a1｜Java split / split("") / trim 移植时去尾随空串、按码点切、只去 ≤U+0020｜读到：源码 String.split(",")、text.split("")、String.trim()；写错：目标直接用 JS split(',') 保留尾随空串，split('') 或 charCodeAt 按 UTF-16 单元切（emoji 计 2），JS trim() 去 Unicode 空白
- rule-299de789e825｜BufferedReader.readLine 迁过来按 /\r\n|\r|\n/ 分行，不写 split('\n')｜读到：源端用 BufferedReader 包装后 readLine() 逐行读脚本或文本；写错：目标端写成 text.split('\n')，只认 LF；CR 行尾的文件整份成一行
