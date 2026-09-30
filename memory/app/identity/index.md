# app/identity

应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取

[上一级](../index.md)

## 本级经验

- [沿用脚手架 bundleName/vendor 前核对所引部署期决策与签名配置；vendor 是描述字段，不随签名延后，按源端组织或作者落地](lesson-fb996956b33a1ba65861.lesson.md)
  - 时机：资源前置阶段落地应用身份字段、决定 bundleName 与 vendor 是否替换脚手架值时；以及维护流水线里身份规则与验证门的口径时
  - 情境：AppScope/app.json5 仍是 com.example.* 包名与 example 厂商，源 build.gradle 给出真实 applicationId；执行规则或身份技能的受限范围（如只写显示名与版本的开发期身份）要求这一阶段把包名、厂商一并留到部署期决策，而验证门对 com.example.* 包名或 vendor=example 判失败。
  - 例外：工程已有签名配置，或决策台账里确有已批准的部署期身份决策；这只影响 bundleName，vendor 不参与签名，仍按源端落地
- [源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量](lesson-a6ed8a9c6017ddb73beb.lesson.md)
  - 时机：接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时
  - 情境：源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。
- [落地应用显示名时同时改 AppScope 的 app_name 与入口 Ability 的 label 字符串，值取 Android 的应用名；资源迁移合并而不覆盖模板 string.json](lesson-55f44e2efdc1a49ac387.lesson.md)
  - 时机：执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时
  - 情境：目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。
  - 例外：本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理
