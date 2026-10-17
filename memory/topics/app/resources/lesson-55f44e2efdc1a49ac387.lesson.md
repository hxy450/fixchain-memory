# 落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名；资源迁移合并而不覆盖模板 string.json

ID：`lesson-55f44e2efdc1a49ac387` · 版本：6 · 阶段：plan/execute/repair · 主题：[app/resources](index.md)

概要：应用显示名同时改 AppScope 与入口 label 值

信号：`app_name`, `EntryAbility_label`, `string.json`, `app.json5`, `AppScope`, `android:label`, `resValue`, `strings.xml`, `productFlavors`, `applicationIdSuffix`

## 何时使用

执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时

## 适用情境

目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。工程还可能有 en_US 等语言限定目录，含同名的脚手架身份键（可能由 i18n 补齐步骤以模板值填入）。 也包括源工程有多个 productFlavors，各 flavor 源集分别覆盖 app_name 与 app_package，台账或派工已指定默认 flavor。

## 例外与边界

- 本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理

## 原因

显示名有两个入口：应用级 label 读 AppScope 资源里的 app_name，入口 Ability 的 label 读 entry 模块资源里的另一个键（脚手架默认 EntryAbility_label）。只改其中一处，另一处显示的仍是脚手架名，编译与结构检查都发现不了。来源两例出自同一流水线：执行规范把身份落地划给编排者在资源阶段之后单独调用，编排者推进阶段时漏掉。一例中资源迁移任务整文件重写 entry string.json 时只改了 app_name，EntryAbility_label 保留脚手架值；另一例中资源迁移无视“合并、不覆盖”规则，只用 Android 字符串重建该文件，删掉了 module.json5 引用的三个身份键，编译修复者上下文里没有应用名，就按工程目录名自造了入口标签。两例的 AppScope app_name 都保持脚手架值，直到 App 身份校验才修。

## 做法

1. 从 AppScope/app.json5 的 label 和 module.json5 里入口 Ability 的 label 各解析出 $string 键，分别在 AppScope/resources/base/element/string.json 与 entry/src/main/resources/base/element/string.json 中改值；值取 Android 实际应用名（build.gradle 的 resValue 优先于 strings.xml，否则取被 android:label 引用的字符串；源工程有 productFlavors 时，先按台账或派工指定的构建变体选定 flavor，取 src/<flavor>/res 覆盖的 app_name，与 applicationIdSuffix 等身份串用同一 flavor，不在转换脚本里默认取第一个或自认为主要的 flavor，也不把台账的 flavor 指定缩窄为只适用包名）。
2. 资源迁移写已有模板的 element 文件时合并新条目，写完确认 module.json5、app.json5 引用的 $string 键仍然存在。
3. 编译修复补回缺失的身份字符串时，值从 Android 应用名或身份步骤的产物取；取不到就登记占位并回报，不按工程目录名自造用户可见名称。
4. 身份落地时 grep 全部 resources/*/element/string.json（含 en_US 等语言目录）里的 EntryAbility_label、app_name 等同名键并同步；i18n 审计报语言目录缺少脚手架身份键时，不以 'label'、'description' 等模板值补齐让审计通过，从 base 或源端真值派生，并在身份落地后复核。
5. 改完读回各 string.json，确认 AppScope、entry base 与各语言目录中的值都等于 Android 应用名或其译名，没有残留脚手架工程名或 'label' 一类模板值。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [推进阶段前核对约定产物与放行门，待接事项落负责方](../../process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md)（共享 3 张卡）
- [app.json5 的 icon 改指分层图标并补齐前景背景](lesson-feec63f65102f5396e51.lesson.md)（共享 2 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [Material 图标按同变体从可核来源取 pathData](../../ui/graphics/icons/lesson-74d535afb21b2270119e.lesson.md)（共享 1 张卡）
- [启动窗图标取自适应前景层，底色取源主题窗口背景](lesson-c4af68b3ee1456525e8e.lesson.md)（共享 1 张卡）

来源支持：5 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

## 来源（按需复核）

- [case-224eb9de83aa652829f4](../../../../store/cases/case-224eb9de83aa652829f4/1c6accbb95b548e17b357f44673488687037364da1317e7c01d09e4b507d3953.json) · 结论：diagnosis, rec-bdc21da4d1, rec-ad41f6ff51, rec-93271db4f7
  卡片版本：`1c6accbb95b548e17b357f44673488687037364da1317e7c01d09e4b507d3953`
- [case-4f7163b95249e9ede2ca](../../../../store/cases/case-4f7163b95249e9ede2ca/8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f.json) · 结论：diagnosis, rec-8fc1e38726
  卡片版本：`8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f`
- [case-7b64dd743c1260eb910f](../../../../store/cases/case-7b64dd743c1260eb910f/298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535.json) · 结论：diagnosis, rec-44da1cc549
  卡片版本：`298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535`
- [case-a7791275ac232a60053d](../../../../store/cases/case-a7791275ac232a60053d/b451436b2c9fe9cc9f9f1f05c7c9c854643704f4c2a6404f6ac0e2f3a4043f67.json) · 结论：diagnosis, rec-e1fe88e787, rec-1c9db7c4d1, rec-f4473c8faa
  卡片版本：`b451436b2c9fe9cc9f9f1f05c7c9c854643704f4c2a6404f6ac0e2f3a4043f67`
- [case-d78a91fb9dfa366ec2ee](../../../../store/cases/case-d78a91fb9dfa366ec2ee/12955eb675ab13f15684178d89c24e3fb02928492792473241c1bd166bde2d3e.json) · 结论：diagnosis, rec-977bee05f6
  卡片版本：`12955eb675ab13f15684178d89c24e3fb02928492792473241c1bd166bde2d3e`
