# Typeface.createFromAsset 装的自定义字体用在画布上

agent 会看到什么：源端 Typeface.createFromAsset 装载字体文件后 paint.setTypeface，再 measureText 参与布局，规格里的 Canvas font 串带引号或加了 bold，或只写「rawfile 注册字体 → ctx.font」、没写首次测宽前字体须可用

## 规矩

- rule-7ec16bff8670｜规格里自定义字体的 Canvas font 串只写字号和注册字族名，不加引号、不叠加 bold｜读到：源端 Typeface.createFromAsset(...) 装载单一字面的字体文件后直接 paint.setTypeface(...)，没有另外请求 Typeface.BOLD 或 ITALIC；写错：规格规定 Canvas 文本统一 font: "bold <size>px '字族名'"：字族名带引号，还加了源端没有的 bold
- rule-5760739aa70b｜源端字体同步装载并参与测宽布局时，规格写明「首次测宽前字体必须可用」｜读到：源端构造器里 Typeface.createFromAsset 同步装载后 paint.setTypeface，随后 measureText 的结果参与布局（如按测宽定字号）；写错：实现映射把 Typeface 一行只写成「rawfile 注册字体 → ctx.font 引用」，风险标低、按「字形差异 → visual 兜底」处理，没写首次测宽前字体须可用
