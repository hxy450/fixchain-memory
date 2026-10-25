# strings.xml 转 string.json 按 aapt2 编译语义计算值：引号外空白折叠、值中任何位置的未转义双引号都剥离（不只首尾成对，\" 保留为引号）、\n \t \uXXXX \' 还原；带内联标记的键取完整内容（样式入口存 HTML、纯字符串入口取全部文字），不用 el.text

ID：`lesson-f88b9c824280ce239dea` · 版本：5

[本主题](index.md)

## 何时使用

资源转换阶段，编写批量脚本把 Android strings.xml 转成 HarmonyOS string.json、确定转义、引号、空白与内联标记的处理规则时

## 适用情境

values*/strings.xml 中有跨行书写（换行加缩进）、\n、\t、\uXXXX 转义、\' \" 或未转义双引号（整值包裹，或出现在值中间，如 below "APM"）的字符串，有的键内联 `<b>`/`<i>`/`<a href>`/`<p>` 子元素（值可能以子元素开头）或用 CDATA 包裹 HTML，由 setMessage(resId)、android:text、Html.fromHtml 或 getString/stringResource 消费；目标 string.json 的值在运行时原样显示，不再经过 aapt2；资源转换 skill 的汇总表只写“\n、\t → preserved”“CDATA 提取文本”“整值被引号包裹时去外层引号”，没写值中间的引号与未包 CDATA 的子元素如何取值。

## 原因

Android 显示的是 aapt2 编译后的值：引号外连续空白折叠为一个空格、未转义双引号只用于保护空白、转义还原为字符；按 XML 原文搬运，界面会出现字面 \n 与源码缩进，只 strip 首尾则会把物理换行留成空行。内联标记被 aapt2 编成样式区间：getString/stringResource 取到去掉标记的全部文字，android:text、getText、setMessage(resId) 保留样式与链接，CDATA 内的标签则是普通文本。el.text 只取首个子元素之前的文本，值以标记开头时得到空串；itertext() 只取文字，用于样式入口会静默丢掉 <b>、<a href>。来源中主会话没读 skill 要求的详细规则，也没抽样带转义的源值，一次脚本写出的 base 有 124 个键与 Android 运行值不同，另有带链接的文案丢了 href。只剥首尾包裹的引号时，值中间的未转义引号原样显示；本条旧做法写成“成对未转义双引号剥离”，召回摘要又压成“成对双引号剥离”，另一应用的转换脚本照此只处理整值包裹，界面显示出源端没有的引号。

## 做法

1. 按 aapt2 语义计算字符串值：引号外连续空白（含换行与缩进）折叠为一个空格并去首尾空白；值中任何位置的未转义双引号都剥离（它只用于保护空白，不论是否成对、是否首尾包裹），\" 转义的保留为引号；\n、\t、\uXXXX、\' 还原为对应字符。不能只做 strip()，也不能只替换部分转义。
2. 写脚本前抽样跨行、含转义、含引号（整值包裹与值中间出现两种形态）与含内嵌标记的条目。<string>/<item> 取完整内容，不用 el.text；含 <b>/<i>/<u>/<a>/<br>/<p> 等子元素的键按源端消费方式输出：经 android:text、getText、setMessage(resId) 等保留样式的入口显示的，按 HTML 保存（字面 < 与 & 转义）；经 getString、stringResource 取纯字符串的，输出去掉标记的全部文字（itertext() 或等价）；CDATA 内的标签按原文保留。交付带标记键清单并标出各键的消费方式（Styled 资源或 Html.fromHtml，是否设 LinkMovementMethod）。
3. skill 汇总规则含糊时先读它要求的详细规则文件；仍不明确时以源平台编译后在运行时显示的值为准。
4. 派工或脚本注释转述取值规则时原样带入“未转义双引号剥离”，不改写成“成对/外层引号剥离”。

## 可选检查

- 写后检查 string.json 不残留字面反斜杠加 n、换行后跟多个空格；逐语言列出源值非空而目标为空、或含连续 \n\n 的键复核；有原版 APK 时可用 aapt2 dump resources 逐条比对
- 源中含未转义 " 的键，目标值不残留引号；\" 转义的键保留引号。

来源支持：5 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-45fda29feaf48460ba4d](../../../store/cases/case-45fda29feaf48460ba4d/fb1be96f369eba6be849548c4c257b6ebb8cc49ab4733da977f1738ba089ce9c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`fb1be96f369eba6be849548c4c257b6ebb8cc49ab4733da977f1738ba089ce9c`
- [case-59da3f8259cbad8d67c1](../../../store/cases/case-59da3f8259cbad8d67c1/12a452f6b381692553b162d5d04160f345147b09206b18a84d1600dbf9f49a5d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`12a452f6b381692553b162d5d04160f345147b09206b18a84d1600dbf9f49a5d`
- [case-7456fcf259be55a8834b](../../../store/cases/case-7456fcf259be55a8834b/0fcbb858330dc0692a5ef76947e2ee1aae9990c5195f78148938c87b3ce94fe8.json) · 结论：recommendation:1
  卡片版本：`0fcbb858330dc0692a5ef76947e2ee1aae9990c5195f78148938c87b3ce94fe8`
- [case-bf53fdebb87671d9eba3](../../../store/cases/case-bf53fdebb87671d9eba3/cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f`
- [case-c2c3a0497bb10ae9aa9a](../../../store/cases/case-c2c3a0497bb10ae9aa9a/337a6de0854264a66fe84ddf25276680916eecc8d4f2a6547cf3c54685778dfe.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`337a6de0854264a66fe84ddf25276680916eecc8d4f2a6547cf3c54685778dfe`
