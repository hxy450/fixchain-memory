# 落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名（有语言译名时 AppScope 与 entry 同建语言目录）；资源迁移合并而不覆盖模板 string.json

## 何时使用

执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时

## 适用情境

目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。工程还可能有 en_US 等语言限定目录，含同名的脚手架身份键（可能由 i18n 补齐步骤以模板值填入）。 也包括 Android 应用名在 values-<语言> 有译名（如 values-ja 的 app_name），而身份裁决只给出 base 显示名。

## 例外与边界

- 本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理

## 原因

显示名有两个入口：应用级 label 读 AppScope 资源里的 app_name，入口 Ability 的 label 读 entry 模块资源里的另一个键（脚手架默认 EntryAbility_label）。只改其中一处，另一处显示的仍是脚手架名，编译与结构检查都发现不了。来源两例出自同一流水线：执行规范把身份落地划给编排者在资源阶段之后单独调用，编排者推进阶段时漏掉。一例中资源迁移任务整文件重写 entry string.json 时只改了 app_name，EntryAbility_label 保留脚手架值；另一例中资源迁移无视“合并、不覆盖”规则，只用 Android 字符串重建该文件，删掉了 module.json5 引用的三个身份键，编译修复者上下文里没有应用名，就按工程目录名自造了入口标签。两例的 AppScope app_name 都保持脚手架值，直到 App 身份校验才修。 应用级 label 只在 AppScope 资源里按语言解析：AppScope 缺某语言目录时，系统设置等处显示 base 名，entry 语言目录里的入口标签译名替代不了；转换脚本手抄译名字面量时，误抄的值会一直留在派生键里。

## 做法

1. 从 AppScope/app.json5 的 label 和 module.json5 里入口 Ability 的 label 各解析出 $string 键，分别在 AppScope/resources/base/element/string.json 与 entry/src/main/resources/base/element/string.json 中改值；值取 Android 实际应用名（build.gradle 的 resValue 优先于 strings.xml，否则取被 android:label 引用的字符串）。源应用名有语言译名时，按源语言集合在 AppScope/resources/<语言>/element/string.json 写 app_name 译名、在 entry 对应语言目录写入口 Ability label 译名，值取源端译名（转换脚本引用同一次解析出的源值，不手抄字面量）；身份裁决只给出 base 值时，不据此省略语言变体。
2. 资源迁移写已有模板的 element 文件时合并新条目，写完确认 module.json5、app.json5 引用的 $string 键仍然存在。
3. 编译修复补回缺失的身份字符串时，值从 Android 应用名或身份步骤的产物取；取不到就登记占位并回报，不按工程目录名自造用户可见名称。
4. 身份落地时 grep 全部 resources/*/element/string.json（含 en_US 等语言目录）里的 EntryAbility_label、app_name 等同名键并同步；i18n 审计报语言目录缺少脚手架身份键时，不以 'label'、'description' 等模板值补齐让审计通过，从 base 或源端真值派生，并在身份落地后复核。
5. 改完读回各 string.json（包括 AppScope 各语言目录），确认 AppScope、entry base 与各语言目录中的值都等于 Android 应用名或其译名，没有残留脚手架工程名或 'label' 一类模板值。

来源支持：6 张卡 · 6 次迁移 · 6 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕编译时 AppScope/resources 会合入每个模块的资源，同一资源目录（如 base、en_US）同一资源组里重名的资源只保留 AppScope 的值，优先级为 AppScope > HAP 模块自身 > 依赖的 HAR；入口 Ability 的 label 若引用与 AppScope 同名的键（如 $string:app_name），只改 entry 模块里的值不会生效。〔成立范围：对象：Stage 模型工程 resources 下的同名资源条目。条件：只在同一限定词目录、同一资源组内比较；键只在模块里有时用模块的值；不同限定词目录之间不互相覆盖。依据是文档说明。最常见的不成立情形：入口 Ability 的 label 用独立键（脚手架默认 EntryAbility_label），AppScope 里没有同名键。〕
- 〔原因〕按文档的配置优先级，系统取应用的图标和名称时：入口 UIAbility（skills 含 entity.system.home 与 ohos.want.action.home）配了 label 就返回它的 label，没配才返回 app.json5 的 label；有多个入口 UIAbility 时取 mainElement 指向的那个，mainElement 未配或不是入口 UIAbility 时取 module.json5 中第一个入口 UIAbility。〔成立范围：对象：含 UIAbility 的 HAP；多 HAP 工程以 entry 类型 HAP 的 module.json5 为准，没有 entry 类型时取 moduleName 按 ASCII 字典序排在最后的 feature HAP；HAP 不含 UIAbility 时返回 app.json5 的 icon 和 label。依据是 OpenHarmony 文档说明，各显示处实际用哪个 label 在 SDK 里核不到：文档「使用场景」一节（带按发行版替换内容的标记）把设置里的应用列表和桌面、最近任务并列，与正文「原因」所述系统设置中的应用名按 AppScope 的 app_name 及其语言目录解析不一致，判断系统设置里显示的名称、要不要建 AppScope 语言目录时不用本条。最常见的不成立情形：入口 UIAbility 省略了 label（DevEco Studio 5.0.3.800 起允许省略），这时只有 app.json5 的 label 生效。〕
- 〔做法第 1 步〕资源限定词目录名里的语言、文字限定词必须与设备当前设置完全一致，该目录才参与匹配；匹配不到或目录里没有该资源时回落到 base；只写语言的目录（如 ja、en）对该语言的各地区都参与匹配。〔成立范围：对象：AppScope 与各模块 resources 下的限定词目录（语言、文字、国家或地区之间用下划线连接，如 zh_Hant_CN）。依据是文档说明；文档列出须完全一致的限定词里没有国家或地区，带地区的目录（如 en_US）能否用于同语言其他地区（如 en_GB）的设备，文档没写、未核，不据此认定会回落 base。最常见的不成立情形：应用设置了偏好语言（setAppPreferredLanguage），此时优先按偏好语言加载资源。〕
