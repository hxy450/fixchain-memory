# 应用显示名的字符串键（app_name、EntryAbility_label）

agent 会看到什么：源 AndroidManifest 的 android:label="@string/app_name" 或 Gradle 的 resValue 给了应用名；AppScope 的 app_name、entry 的 EntryAbility_label 只改了一处、写成规格给的别的字面值或按目录名自造，en_US 等语言目录里仍是 label 一类模板值

## 通用查法

### 落应用名时顺着两处 label 找到字符串键，按源端 resValue 或 strings.xml 写全各语言

审的是：资源
触发（任一种）：
- 读到：源 AndroidManifest 的 android:label="@string/app_name"，或 Gradle 构建脚本用 resValue 提供 app_name；写错的样子：AppScope 的 app_name、entry 的 EntryAbility_label 只改了一处，或仍是模板值
- 写错的样子：en_US 等语言目录的 string.json 里 app_name、EntryAbility_label 仍是模板值
适用范围：应用身份落地、编译修复补身份字符串时，确定桌面和系统显示的应用名
做法：
- 从 AppScope/app.json5 的 label 和 module.json5 入口 UIAbility 的 label 解析出 $string 键（通常是 app_name、EntryAbility_label），AppScope 和 entry 两边都改
- 值按源端取：先看 Gradle 里的 resValue("string", "app_name", …)，没有再读 res/values*/strings.xml 的 app_name；各语言写进对应限定词目录，改完按值搜各目录残留的 label、MyApplication
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 入口 UIAbility 配了 icon 和 label 时系统返回它的；只有入口 UIAbility 没设 icon 或 label 时才用 app.json5 的：桌面显示名通常来自 EntryAbility_label，两处都要是源应用名（出处：layered-image.md，配置优先级和生成策略）
- 系统优先从与设备状态匹配的限定词目录取资源，找不到才去 base：只改 base 盖不住语言目录里的旧值（出处：resource-categories-and-access.md，资源匹配）
- AppScope 与模块重名资源打包时 AppScope 优先，其次 HAP 模块自身，再次依赖的 HAR：AppScope 和模块里的 app_name 等重名键要一起核对（出处：resource-categories-and-access.md，资源分类）
- 模板里 EntryAbility 写 "label": "$string:EntryAbility_label"：脚手架的默认引用（出处：module-configuration-file.md，配置文件示例）
针对本应用要查的：
- 源应用名的实际值：源工程模块构建脚本 defaultConfig、productFlavors 里的 resValue("string", "app_name", …)；没有再看 res/values*/strings.xml 的 <string name="app_name">；有 resValue 按迁移对应的 flavor 取第三个参数；否则逐个语言目录读出 app_name，原样写进目标同语言的 string.json
- 目标工程哪些目录带身份类键：AppScope/resources 与各模块 src/main/resources 下的 */element/string.json；按 EntryAbility_label、EntryAbility_desc、module_desc、app_name 搜，逐个看取值
来源：3 张卡，3 个应用
- case-224eb9de83aa652829f4（android-panorama-map-vest7）：做法第 1 步 ← 建议 2
- case-9e50f3aa8db41be6d2fe（Privacy Friendly 2048）：做法第 2 步 ← 建议 4
- case-a7791275ac232a60053d（DeepAI全能PPT）：做法第 2 步 ← 建议 2

## 规矩

- rule-a780e4186062｜app_name 和 EntryAbility_label 取安卓实际应用名（resValue 优先），不用模板值｜读到：AndroidManifest.xml 的 `android:label="@string/app_name"`，strings.xml 里 app_name 是应用名；写错：只改了一处 app_name；`EntryAbility_label` 的值还是模板 "label"，或 AppScope 的 `app_name` 仍是脚手架值
- rule-a6ff10177760｜android:label 引用 @string/app_name 时，目标三处应用名取源值，无决策 ID 不改｜读到：源 AndroidManifest 的 <application> / <activity> android:label="@string/app_name"，res/values*/strings.xml 里各语言 app_name 有确定的值；写错：AppScope 的 app_name、entry 的 EntryAbility_label 或 app_name 写成规格或派工给的另一个字面值；映射表或回执写「已批决策值」，却引不出决策 ID
- rule-65587d0b6114｜身份落地改了 EntryAbility_label/app_name 后，所有语言目录的同名键一并同步｜读到：身份落地步骤读到源端应用名（manifest `android:label` 引用的字符串），要消除脚手架默认值；写错：只改了 AppScope 和 entry `base/element/string.json` 的 `app_name`、`EntryAbility_label`，`en_US` 等语言目录里的同名键仍是模板值或旧值
- rule-f33382c4eed6｜语言目录缺脚手架身份键时，不填 'label' 等模板值让审计通过，从 base 或源端真值派生｜读到：i18n 完整性审计报 `en_US` 等语言目录缺 `EntryAbility_label`、`EntryAbility_desc`、`module_desc`（key_missing）；写错：语言目录的 `element/string.json` 里补上了这些键，值却是脚手架模板默认值（如 `"label"`、`"description"`）
- rule-846bd875fdc4｜各语言目录的入口 Ability label 取同一语言源 app_name 的解析结果，不手抄字面量｜读到：Manifest 里 application 和启动 Activity 的 android:label 都引用 @string/app_name，values-<语言>/strings.xml 里有 app_name 译名；写错：entry/src/main/resources/<语言>/element/string.json 里 EntryAbility_label 的值和该语言源 app_name 不一致（如少了字），转换脚本里它是手写的字面量
- rule-168ab61eed18｜源应用名在 values-<语言> 有译名时，AppScope 也按源语言集合建语言目录写 app_name｜读到：Manifest 的 application 或启动 Activity 的 android:label 引用的字符串在 values-<语言> 有译名；写错：AppScope/resources 下只有 base/element/string.json，没有对应语言目录的 app_name；或只在 entry 的语言目录写了 EntryAbility_label
- rule-66c436c4df8e｜有 productFlavors 时 app_name 取台账指定 flavor 的值，不取默认或第一个｜读到：源工程 src/<flavor>/res/values/strings.xml 里各 flavor 各有 app_name、app_package，派工说明或决策台账指定了某个 flavor；写错：AppScope/resources/base/element/string.json 的 app_name 是另一个 flavor 的值，或者入口 UIAbility 的 label 引用了一个另写的同值串而不是 app_name
