# values-* 语言目录对应的限定词目录

agent 会看到什么：源 res/ 下有 values-zh、values-zh-rTW、values-es 等语言目录，或只有默认 values/；目标 resources/ 下的限定词目录和源端对不上（少语言、values-zh 收窄成 zh_CN、合成了源端没有的 zh_CN），或限定词目录的键集比源端该语言多

## 通用查法

### 迁 values-* 语言资源时，按源端实有的语言目录逐个建限定词目录，键集照源

审的是：资源
触发（任一种）：
- 读到：源工程 res/values-zh、res/values-zh-rTW、res/values-es 等语言目录，或只有默认 res/values/strings.xml；写错的样子：目标 resources 下的限定词目录和源端对不上：少了语言、values-zh 收窄成 zh_CN、合成了源端没有的 zh_CN
- 读到：源端 values-xx/strings.xml 的键比默认 res/values/strings.xml 少；写错的样子：目标限定词目录的 string.json 补齐了键，值是自造译文或 `[TODO: translate]`
适用范围：把安卓 values-* 语言资源转成鸿蒙 resources 下限定词目录的 string.json 时
做法：
- 盘点源工程各模块 res/ 下带语言或地区的 values-* 目录（values-night、values-xlarge 不算），每个建一个：values-<语言> → <语言>/element/，values-<语言>-r<地区> → <语言>_<地区>/element/；源只有默认 values/ 时只建 base
- 每个限定词目录的 string.json 只收源端同一目录里有的 name，缺的键不写，让系统回落 base
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 语言、文字、国家或地区之间用下划线连接，如 zh_CN、zh_Hant_CN：限定词目录的写法（出处：resource-categories-and-access.md，限定词目录）
- 语言由 2~3 个小写字母组成，如 zh、en：只按语言的目录写成 zh，不带地区（出处：resource-categories-and-access.md，限定词目录）
- 区域的可选组合：语言、语言_文字、语言_国家或地区、语言_文字_国家或地区：values-zh、values-es 这类只有语言的目录对到只写语言的限定词（出处：resource-categories-and-access.md，限定词目录与设备状态的匹配规则）
- 限定词目录中找不到该资源时，才去 base 目录中查找：缺键自动回落 base，和安卓回退默认 values 一致（出处：resource-categories-and-access.md，资源匹配）
针对本应用要查的：
- 源端实际有哪些语言目录、各自的键集：源工程各模块 res/ 下的 values-<限定词> 目录名，和其中 strings.xml（及 arrays.xml、plurals.xml）的 name；只算语言或地区限定词，语言照抄、-r 后的地区码接在下划线后；例：values-zh-rTW → zh_TW，values-zh → zh
未核实：zh_CN 目录对其他中文地区设备的匹配行为按卡写，本机未上机核实
来源：3 张卡，3 个应用
- case-311b8c323b04022b2a04（Jetsnack）：做法第 1 步 ← 建议 1
- case-8a522021d6d10fded125（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3
- case-bf53fdebb87671d9eba3（Cofi）：做法第 1 步 ← 建议 3

## 规矩

- rule-2a3d64400057｜资源迁移按源端全部 values-* 建对应限定词目录，范围约定无来源时不照缩｜读到：源工程 res/values-es、res/values-zh-rTW 等多个语言目录；项目文档写「默认迁 values + values-zh」，资源转换规则写语言数不超过 10 时全部转换；写错：目标 resources/ 下只有 resources/base 和 zh_CN 两个限定词目录，源端其余语言缺失
- rule-7f6c4dfe54e1｜源只有仅语言限定的 values-zh 时，目标落 zh/ 目录，不收窄成 zh_CN/｜读到：源工程 res/values-zh/strings.xml 这类只带语言、不带地区的目录（没有 values-zh-rCN）；写错：目标 resources 下生成的是 zh_CN/element/string.json，没有 zh/element/；映射记录写成 values-zh → zh_CN
- rule-47874ab01485｜源端只有默认 values/ 时只生成 base 字符串，不合成 zh_CN 等译文｜读到：源 res 下只有默认 `values/strings.xml`，没有 `values-zh` 等 values-<locale> 语言目录（`values-night`、`values-xlarge` 不是语言目录）；写错：目标出现 `zh_CN/element/string.json`（或 `plural.json`），业务键的值是源端没有的中文译文
- rule-6d292ed1e72e｜源语言目录缺的键在目标限定词目录里也留缺，不补机器翻译或 TODO 占位｜读到：源端 values-xx/strings.xml 的键比默认 res/values/strings.xml 少，运行时缺键回退默认 values；写错：目标 zh_CN/element/string.json 的键数与 base 相同，多出源端该语言目录没有的键，值是自动翻译或带 `[TODO: translate]`
- rule-d80d94401d9a｜迁字符串资源时取含库依赖的合并资源表，不把应用源 res/ 的 values-* 当全集｜读到：Gradle 构建脚本的 dependencies 里有 androidx.appcompat、material、androidx.preference 等自带字符串资源的库；迁移 skill 要求先构建 APK 再反编译取合并资源表；写错：目标 resources 下的语言目录只有应用 res/values-* 那几种，只有库才提供的语言（如 ko、th、vi）和框架、库的译文都没有；报告写「source res/ · build=skipped」且没列缺失的库资源
- rule-8258533253e3｜某语言缺的字符串键保留缺失让运行时回退默认语言，不用 TODO 填平再交模型补译｜读到：源端某个 values-<语言> 目录的 strings.xml 缺部分 <string> 键（运行时回退默认 values）；写错：缺键用默认语言文本加 `[TODO: translate]` 前缀填平并登记待译，或该语言 string.json 里出现源端没有的模型译文
- rule-cff3c85d12e5｜语言目录只放源端有的文字资源，不复制 base 的 color/float 等 element 文件｜读到：Android 源的 values-<locale> 只含 strings.xml / arrays.xml（文字资源），color、dimen、bool、integer 只在 values/ 和 values-land 等非语言目录；写错：目标 resources/<语言_地区>/element/ 下出现 color.json、float.json、boolean.json、integer.json，内容是 base 同名文件的整份副本
