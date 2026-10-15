# strings.xml 转 string.json 按 aapt2 语义取值：引号外空白折叠，值中任何位置的未转义双引号都剥离，转义还原

ID：`lesson-f88b9c824280ce239dea` · 版本：6

[本主题](index.md)

## 何时使用

资源转换阶段，编写批量脚本把 Android strings.xml 转成 HarmonyOS string.json、确定转义、引号与空白的处理规则时

## 适用情境

values*/strings.xml 中有跨行书写（换行加缩进）、\n、\t、\uXXXX 转义、\' \" 或未转义双引号（整值包裹，或出现在值中间，如 below "APM"）的字符串；目标 string.json 的值在运行时原样显示，不再经过 aapt2；资源转换 skill 的汇总表只写“\n、\t → preserved”“整值被引号包裹时去外层引号”，没写值中间的引号如何取值。

## 例外与边界

- 含 <b>/<a> 等内联标记子元素或 CDATA 的键，取完整内容与输出形态按内联标记一条处理

## 原因

Android 显示的是 aapt2 编译后的值：引号外连续空白折叠为一个空格、未转义双引号只用于保护空白、转义还原为字符。按 XML 原文搬运，界面会出现字面 \n 与源码缩进；只 strip 首尾会把物理换行留成空行；只剥首尾包裹的引号时，值中间的未转义引号原样显示。规则被转述成“成对/外层引号剥离”后，脚本就只处理整值包裹的形态。

## 做法

1. 按 aapt2 语义计算字符串值：引号外连续空白（含换行与缩进）折叠为一个空格并去首尾空白；值中任何位置的未转义双引号都剥离（不论是否成对、是否首尾包裹），\" 转义的保留为引号；\n、\t、\uXXXX、\' 还原为对应字符。不能只做 strip()，也不能只替换部分转义。
2. 写脚本前抽样跨行、含转义、含引号（整值包裹与值中间出现两种形态）的条目作为必测样本。
3. skill 汇总规则含糊时先读它要求的详细规则文件；仍不明确时以源平台编译后在运行时显示的值为准。
4. 派工或脚本注释转述取值规则时原样带入“值中任何位置的未转义双引号剥离”，不改写成“成对/外层引号剥离”。

## 可选检查

- 写后检查 string.json 不残留字面反斜杠加 n、换行后跟多个空格；逐语言列出源值非空而目标为空、或含连续 \n\n 的键复核；有原版 APK 时可用 aapt2 dump resources 逐条比对
- 源中含未转义 " 的键，目标值不残留引号；\" 转义的键保留引号。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-45fda29feaf48460ba4d](../../../store/cases/case-45fda29feaf48460ba4d/fb1be96f369eba6be849548c4c257b6ebb8cc49ab4733da977f1738ba089ce9c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`fb1be96f369eba6be849548c4c257b6ebb8cc49ab4733da977f1738ba089ce9c`
- [case-bf53fdebb87671d9eba3](../../../store/cases/case-bf53fdebb87671d9eba3/cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f`
- [case-c2c3a0497bb10ae9aa9a](../../../store/cases/case-c2c3a0497bb10ae9aa9a/337a6de0854264a66fe84ddf25276680916eecc8d4f2a6547cf3c54685778dfe.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`337a6de0854264a66fe84ddf25276680916eecc8d4f2a6547cf3c54685778dfe`
