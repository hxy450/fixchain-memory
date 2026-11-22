# 落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名（有语言译名时 AppScope 与 entry 同建语言目录）；资源迁移合并而不覆盖模板 string.json

## 何时使用

执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时

## 适用情境

目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。工程还可能有 en_US 等语言限定目录，含同名的脚手架身份键（可能由 i18n 补齐步骤以模板值填入）。 也包括 Android 应用名在 values-<语言> 有译名（如 values-ja 的 app_name），而身份裁决只给出 base 显示名。“Android 应用名”按两层取：application 的 android:label 对应 AppScope 的 app_name；桌面上显示的名称先取启动器 Activity 的 MAIN/LAUNCHER intent-filter 的 label、再取该 Activity 的 android:label，都没设才用 application 的 label，所以启动器 Activity 自己设了不同的 label 时，入口 Ability 的 label 取它，不统一改成 application 的值。

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕系统取应用图标和名称时：module.json5 的 mainElement 是入口 UIAbility 的，返回它配置的 icon 和 label；mainElement 没配或不是入口 UIAbility 的，返回第一个入口 UIAbility 的 icon 和 label；只有该入口 UIAbility 没设置 icon 或 label、或 HAP 里没有 UIAbility 时，才返回 app.json5 的 icon 或 label
- 〔原因 / 做法第 1 步〕app.json5 的 label 是应用名称，取值为字符串资源的索引以支持多语言，不超过 63 字节，不可缺省；module.json5 里 UIAbility 的 label 是该组件对用户显示的名称，同样取字符串资源索引，不超过 255 字节，可缺省
- 〔适用情境 / 做法第 1、2 步〕模板工程里 app.json5 写 "label": "$string:app_name"，读 AppScope/resources/base/element/string.json 的 app_name；module.json5 的入口 UIAbility 写 "label": "$string:EntryAbility_label"，读 entry/src/main/resources/base/element/string.json 的 EntryAbility_label
- 〔适用情境 / 做法第 4 步〕应用使用资源时，系统优先从与设备状态匹配的限定词目录（如语言目录）里找；只有没有匹配的限定词目录、或限定词目录里找不到该资源时才去 base 目录找，所以语言目录里留着的同名键会盖过 base 里的值
- 〔原因 / 做法第 1、2 步〕编译构建时 AppScope 目录下的资源合入各模块资源，相同资源目录和资源组目录下的重名资源按 AppScope、HAP 模块自身、依赖的 HAR 的优先级打包，重名时只保留 AppScope 的
- 〔做法第 1 步〕资源的语言限定词由 2~3 个小写字母组成（如 zh、en），取值按 ISO 639
- 〔原因 / 做法第 1 步〕设备上应用级名称（系统设置等处显示的应用名）只在 AppScope 的资源里按语言解析：AppScope 缺某个语言目录时，该语言环境下显示 base 里的名称，entry 语言目录里的入口 Ability 标签译名替代不了
