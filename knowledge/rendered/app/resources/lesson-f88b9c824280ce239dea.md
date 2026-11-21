# strings.xml 转 string.json 按 aapt2 编译语义计算值：引号外空白折叠、值中任何位置的未转义双引号都剥离（不只首尾成对，\" 保留为引号）、\n \t \uXXXX \' 还原；带内联标记的键取完整内容（样式入口存 HTML、纯字符串入口取全部文字），不用 el.text

## 何时使用

资源转换阶段，编写批量脚本把 Android strings.xml 转成 HarmonyOS string.json、确定转义、引号、空白与内联标记的处理规则时

## 适用情境

values*/strings.xml 中有跨行书写（换行加缩进）、\n、\t、\uXXXX 转义、\' \" 或未转义双引号（整值包裹，或出现在值中间，如 below "APM"）的字符串，有的键内联 `<b>`/`<i>`/`<a href>`/`<p>` 子元素（值可能以子元素开头）或用 CDATA 包裹 HTML，由 setMessage(resId)、android:text、Html.fromHtml 或 getString/stringResource 消费；目标 string.json 的值在运行时原样显示，不再经过 aapt2；资源转换 skill 的汇总表只写“\n、\t → preserved”“CDATA 提取文本”“整值被引号包裹时去外层引号”，没写值中间的引号与未包 CDATA 的子元素如何取值。

## 原因

Android 显示的是 aapt2 编译后的值：引号外连续空白折叠为一个空格、未转义双引号只用于保护空白、转义还原为字符；按 XML 原文搬运，界面会出现字面 \n 与源码缩进，只 strip 首尾则会把物理换行留成空行。内联标记被 aapt2 编成样式区间：getString/stringResource 取到去掉标记的全部文字，android:text、getText、setMessage(resId) 保留样式与链接，CDATA 内的标签则是普通文本。el.text 只取首个子元素之前的文本，值以标记开头时得到空串；itertext() 只取文字，用于样式入口会静默丢掉 <b>、<a href>。来源中主会话没读 skill 要求的详细规则，也没抽样带转义的源值，一次脚本写出的 base 有 124 个键与 Android 运行值不同，另有带链接的文案丢了 href。只剥首尾包裹的引号时，值中间的未转义引号原样显示；本条旧做法写成“成对未转义双引号剥离”，召回摘要又压成“成对双引号剥离”，另一应用的转换脚本照此只处理整值包裹，界面显示出源端没有的引号。

## 做法

1. 按 aapt2 语义计算字符串值：引号外连续空白（含换行与缩进）折叠为一个空格；值里没有样式标签时再去首尾空白，含 <b>、<i>、<a>、<p> 等样式标签的值，首尾空白只折叠成一个空格、不去掉（只含 xliff:g 或 CDATA 的值不算含样式标签，照样去首尾）；值中任何位置的未转义双引号都剥离（它只用于保护空白，不论是否成对、是否首尾包裹），\" 转义的保留为引号；\n、\t、\uXXXX、\' 还原为对应字符。不能只做 strip()，也不能只替换部分转义。
2. 写脚本前抽样跨行、含转义、含引号（整值包裹与值中间出现两种形态）与含内嵌标记的条目。<string>/<item> 取完整内容，不用 el.text；含 <b>/<i>/<u>/<a>/<br>/<p> 等子元素的键按源端消费方式输出：经 android:text、getText、setMessage(resId) 等保留样式的入口显示的，按 HTML 保存（字面 < 与 & 转义）；经 getString、stringResource 取纯字符串的，输出去掉标记的全部文字（itertext() 或等价）；CDATA 内的标签作为普通文字保留，但 CDATA 里的空白照样折叠、未转义双引号照样剥离、转义照样还原（<a href="x"> 编译为 <a href=x>）。交付带标记键清单并标出各键的消费方式（Styled 资源或 Html.fromHtml，是否设 LinkMovementMethod）。
3. skill 汇总规则含糊时先读它要求的详细规则文件；仍不明确时以源平台编译后在运行时显示的值为准。
4. 派工或脚本注释转述取值规则时原样带入“未转义双引号剥离”，不改写成“成对/外层引号剥离”。

## 可选检查

- 写后检查 string.json 不残留字面反斜杠加 n、换行后跟多个空格；逐语言列出源值非空而目标为空、或含连续 \n\n 的键复核；有原版 APK 时可用 aapt2 dump resources 逐条比对
- 源中含未转义 " 的键，目标值不残留引号；\" 转义的键保留引号。

来源支持：5 张卡 · 4 次迁移 · 4 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；Android SDK build-tools 30.0.3、36.1.0、37.0.0 的 aapt2；androidx.appcompat:appcompat 1.1.0、1.8.0；androidx.compose.ui:ui-android 1.10.3、1.12.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕aapt2 对不含样式标签的字符串在折叠空白后去掉首尾空白（"   lead and trail   " 得 lead and trail）；值里含 <b>、<i>、<a>、<p> 等会编成样式区间的子元素时，首尾空白只折叠成一个空格、不去掉（换行缩进包着的 <b>Title</b> 得到前后各带一个空格的 Title）。〔成立范围：对象：values*/strings.xml 的 <string>，以及 <string-array>、<plurals> 的 <item>（item 实测同样：不含样式的去首尾，含样式的只折叠不去）。只含 <xliff:g> 或 CDATA 的值按不含样式处理、照样去首尾；参与折叠的是空格、换行、制表符（含 &#9;），U+00A0（不换行空格）不参与。版本：build-tools 30.0.3、36.1.0、37.0.0 的 aapt2 结果相同。最常见的不成立情形：空白位于未转义双引号之内，原样保留。〕
- 〔做法第 2 步〕CDATA 只让其中的 < > 标签变成普通文字，aapt2 对 CDATA 里的内容照样做空白折叠、未转义双引号剥离和 \n、\'、\uXXXX 等转义还原：<![CDATA[a\nb "q" it\'s]]> 编译为 a、换行、b q it's，<![CDATA[<a href="x">l</a>]]> 编译为 <a href=x>l</a>。〔成立范围：对象：<string> 值中的 CDATA 段。版本：build-tools 30.0.3、36.1.0、37.0.0 的 aapt2 结果相同。最常见的不成立情形：CDATA 里的空白位于未转义双引号之内，原样保留。〕
- 〔做法第 2 步〕<xliff:g> 是给翻译用的不可译标记，aapt2 编译时去掉这对标签、保留其中文字，不生成样式区间：Count: <xliff:g id="n">%1$d</xliff:g> items 编译为普通字符串 Count: %1$d items。〔成立范围：对象：声明了 xliff 命名空间（urn:oasis:names:tc:xliff:document:1.2）的 strings.xml 中的 <xliff:g>；标签内的引号与空白照常按 aapt2 规则处理。版本：build-tools 30.0.3、36.1.0、37.0.0 的 aapt2 结果相同。最常见的不成立情形：同一个值里还有 <b> 等样式标签，整串编成样式字符串，但 xliff:g 本身仍不产生区间。〕
- 〔做法第 1 步〕去掉首尾空白后整个值符合资源引用写法（@string/名字、@android:string/名字，以及 @color/名字 等别的类型和 @null）的 <string>，编译结果是引用而不是文字，引用 @string 时运行时取到的是被引用资源的文字；要按字面显示这种写法须写成 \@。不成引用写法的 @ 开头文字（如 @hello、@ mention）按普通文字保留。〔成立范围：对象：<string> 的值整体是资源引用语法时；被引用的资源不存在时 aapt2 link 报错，查不出来的是引用存在的情形。以 ? 开头的值（单独一个 ? 除外）同样按主题属性引用解析。版本：build-tools 30.0.3、36.1.0、37.0.0 的 aapt2 结果相同。最常见的不成立情形：@ 出现在值中间（如 a@b.com），按普通文字处理。〕
- 〔原因〕Resources.getString 返回去掉样式信息的纯文本，getText 返回可能带样式区间的 CharSequence；XML 的 android:text（TypedArray.getText）、TextView.setText(int)、AlertDialog.Builder.setMessage(int)（平台版与 appcompat 版）都走 getText，保留样式和链接；Compose 的 stringResource 走 getString，只得到文字。〔成立范围：对象：安卓字符串资源的读取入口。版本：平台源码 android-36.1；appcompat 1.1.0、1.8.0 的 AlertDialog.Builder.setMessage(int) 调 Context.getText；compose ui 1.10.3、1.12.0 的 stringResource 调 Resources.getString。<a href> 在 getText 结果里是 URLSpan，但 TextView 只在 autoLink 加出链接时才自动设 LinkMovementMethod，平台 AlertDialog 的消息默认也不设，样式资源里的链接要代码设 LinkMovementMethod 才能点。最常见的不成立情形：代码先 getString 再交给 setText(CharSequence) 或 Html.fromHtml（如 setText(getString(R.string.x))），样式标签在 getString 时已经丢掉。〕
