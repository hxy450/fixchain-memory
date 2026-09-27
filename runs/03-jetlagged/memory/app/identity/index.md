# app/identity

应用身份字段（显示名及其 label 资源）从 Android 迁到 AppScope 与入口模块的写法

[上一级](../index.md)

## 本级经验

- [落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名](lesson-55f44e2efdc1a49ac387.lesson.md)
  - 时机：执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），或资源迁移任务重写 string.json 时
  - 情境：目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；Android 应用名来自 strings.xml 的 app_name，并由 Manifest 的 android:label 引用。
  - 例外：本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理
