# string.json 条目的文案来源

agent 会看到什么：源控件的 android:text 引用 @string/…、写死字面量、走平台 @android:string/cancel，或代码格式化出标题和数量；产物 string.json 里的值是自拟、概括或按键名猜的，缺源端有的文案或格式串，建了源端没有的条目，或只写了 base 一种语言

## 通用查法

### string.json 的条目值顺着源端引用读出原文照抄，找不到来源就登记缺口

审的是：资源
触发（任一种）：
- 读到：源控件 android:text 引用 @string/…、写死字面量，或引用平台的 @android:string/…；写错的样子：string.json 里的 value 是按键名、截图或概括自拟的文案，和源端原文不一致
- 读到：代码里新出现的 $r('app.string.…') 在 string.json 里没有定义；写错的样子：string.json 新建了源端找不到出处的条目，或多语言只在 base 写了一种
适用范围：给 string.json 写或补条目的值时（迁移、收口补键、多语言目录）
做法：
- 顺着源端引用读原文：@string/x → 源工程 res/values*/strings.xml 里 name="x" 的值（各语言目录各取一份）；写死的 android:text → 逐字照抄，分行写成 \n；@android:string/x → Android SDK 平台资源 data/res/values-<语言>/strings.xml 里的同名条目
- 找不到来源时在交回里登记缺口，不按键名推断、不自拟文案
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- {"string": [{"name": "<名>", "value": "<原文>"}]}：string.json 的结构（出处：resource-categories-and-access.md，资源文件示例）
- $r('app.string.<名>')：页面里引用字符串资源的写法（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- 平台 cancel：values 里是 Cancel，values-zh-rCN 里是 取消，values-de 里是 Abbrechen：例：平台字符串的各语言值从平台资源的同名条目读（出处：Android SDK 平台资源 data/res/values/strings.xml 与 values-zh-rCN/strings.xml、values-de/strings.xml，cancel（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 条目对应的源端原文：源工程布局 XML 里对应控件的 android:text；是 @string/… 的到 res/values*/strings.xml 按 name 找，是 @android:string/… 的到 Android SDK 平台资源 data/res/values-<语言>/strings.xml 按 name 找；收口补键时再看目标代码改成 $r 之前的字面量；照抄成 value，多语言目录按对应语言的文件取；例：偏好对话框没写 android:negativeButtonText 时负按钮取平台 cancel
来源：3 张卡，3 个应用
- case-2caef8782962c0b30088（实时公交）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-dadda7b6820516f5f415（Privacy Friendly 2048）：做法第 1 步 ← 建议 2
- case-f663597a71756594de10（骑行记录）：做法第 1 步 ← 建议 3

## 规矩

- rule-7d0fa34e8016｜说明文案写死在布局 android:text 时，string.json 逐字照抄源文、保留分行｜读到：布局 XML 的 TextView 上 android:text 是写死的长文案（不是 @string/ 引用）；写错：目标 resources/base/element/string.json 里对应条目的 value 是概括、改写或通用的说明文字，或者源文的分行没了
- rule-04a97f4e0903｜弹窗文案迁到 string.json 时按源布局引用的 strings 逐条写，不只写自拟的标题和按钮｜读到：源弹窗布局里标题、前缀、说明文字都以 @string/… 引用 strings.xml；写错：目标 base 和 en_US 的 string.json 只写了自拟的标题和按钮键，缺源布局里的说明、前缀文案，标题文案也和源不同
- rule-37d37ced4406｜为新引用的字符串键补值时，回查源布局或原字面量，不按键名自拟文案｜读到：代码里新出现的 `$r('app.string.…')` 引用在 `string.json` 里没有定义，交接只给了键名；写错：`string.json` 里按键名自拟了新文案（如 step 类键写成「第1站」），和源端 `android:text` 或替换前的字面量不一致
- rule-fedb8f994681｜新增字符串资源前确认源端 strings.xml 有对应文案，没有就不建｜读到：源端 res/values/strings.xml 里没有对应的 `<string>` 条目；写错：目标 string.json 里新建了源端没有的文案条目（随补出的按钮一起加）
- rule-5400bc6dadeb｜追加 string.json 键时，把源端代码格式化的标题、数量、单位格式串一并登记｜读到：源端代码用 `SimpleDateFormat`、`String.format` 或拼接生成带单位的标题、数量（如 `"yyyy年M月"`、`"%02d月"`）；写错：模块 `string.json` 追加了一批静态文案键，却没有这段文案的格式串（如 `%s年%s月`）
- rule-457ed414cc66｜接入 App 内分享渠道时各语言 string.json 都补上渠道名称｜读到：源端分享面板的 App 内渠道有自己的显示名称；写错：各语言的 string.json 只新增分享不可用一类提示，没有这个渠道的名称条目
- rule-61230ef8885c｜偏好对话框用平台 cancel 文案时，string.json 按源端语言建多语言资源，不写死英文｜读到：<ListPreference> 或 <EditTextPreference> 没写 android:negativeButtonText，按钮文案取平台 @android:string/cancel；写错：目标各语言目录的 element/string.json 里没有对应的 cancel 文案，或只在 base 写死 "Cancel"，或代码里直接写 'Cancel' / "CANCEL" 字面量
- rule-cca0aaafa0df｜外部模板弹窗的文案从依赖 AAR 的字符串取，string.json 不写源端没有的文案｜读到：源端模板方法的 Config 只传标题和条目数组，源码里 grep 不到按钮文案；写错：string.json 里新增了取自 Config 条目的分区标题和摘要，或写入源码和依赖库里都没有的按钮文案（如「同意并继续」）
- rule-0df82c432896｜代码引用 android.R.string.* 系统文案时，替代的应用字符串要补到每个已有语言目录｜读到：Kotlin / Compose 里 stringResource(android.R.string.ok) 或 getString(android.R.string.cancel) 这类平台字符串引用；写错：新加的键只写进 base/element/string.json（值是英文 OK），工程已有的各语言目录里没有这个键，也没登记 `resource-pending-translation`
- rule-998db9bbe2da｜框架默认的 ok、cancel 要落成目标资源，各语言值从 Android 框架对应语言目录取｜读到：源端对话框按钮用框架默认的 @android:string/ok、@android:string/cancel（偏好 XML 没声明按钮文案）；写错：base 和各语言 string.json 里没有框架 ok / cancel 对应的条目，只有应用自己的 ok、cancel、confirm
