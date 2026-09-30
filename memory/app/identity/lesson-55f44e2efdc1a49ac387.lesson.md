# 落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名；资源迁移合并而不覆盖模板 string.json

ID：`lesson-55f44e2efdc1a49ac387` · 版本：2

[本主题](index.md)

## 何时使用

执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时

## 适用情境

目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。

## 例外与边界

- 本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理

## 原因

显示名有两个入口：应用级 label 读 AppScope 资源里的 app_name，入口 Ability 的 label 读 entry 模块资源里的另一个键（脚手架默认 EntryAbility_label）。只改其中一处，另一处显示的仍是脚手架名，编译与结构检查都发现不了。来源两例出自同一流水线：执行规范把身份落地划给编排者在资源阶段之后单独调用，编排者推进阶段时漏掉。一例中资源迁移任务整文件重写 entry string.json 时只改了 app_name，EntryAbility_label 保留脚手架值；另一例中资源迁移无视“合并、不覆盖”规则，只用 Android 字符串重建该文件，删掉了 module.json5 引用的三个身份键，编译修复者上下文里没有应用名，就按工程目录名自造了入口标签。两例的 AppScope app_name 都保持脚手架值，直到 App 身份校验才修。

## 做法

1. 从 AppScope/app.json5 的 label 和 module.json5 里入口 Ability 的 label 各解析出 $string 键，分别在 AppScope/resources/base/element/string.json 与 entry/src/main/resources/base/element/string.json 中改值；值取 Android 实际应用名（build.gradle 的 resValue 优先于 strings.xml，否则取被 android:label 引用的字符串）。
2. 资源迁移写已有模板的 element 文件时合并新条目，写完确认 module.json5、app.json5 引用的 $string 键仍然存在。
3. 编译修复补回缺失的身份字符串时，值从 Android 应用名或身份步骤的产物取；取不到就登记占位并回报，不按工程目录名自造用户可见名称。
4. 改完读回两个文件，确认两处值都等于 Android 应用名，没有残留脚手架工程名。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-224eb9de83aa652829f4](../../../store/cases/case-224eb9de83aa652829f4/1c6accbb95b548e17b357f44673488687037364da1317e7c01d09e4b507d3953.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`1c6accbb95b548e17b357f44673488687037364da1317e7c01d09e4b507d3953`
- [case-7b64dd743c1260eb910f](../../../store/cases/case-7b64dd743c1260eb910f/298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535.json) · 结论：diagnosis, recommendation:2
  卡片版本：`298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535`
