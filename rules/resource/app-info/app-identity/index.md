# AppScope/app.json5 的应用身份字段

agent 会看到什么：源模块 Gradle 构建脚本里有 applicationId / namespace（反域名，第二段是组织）；AppScope/app.json5 的 bundleName、vendor、versionName 仍是模板值（com.example.myapplication、example、1.0.0），理由写成部署期、与签名绑定，或交回里没指出

## 规矩

- rule-3e13091f989b｜AppScope/app.json5 的 bundleName 要等于安卓 applicationId，不留脚手架值｜读到：源模块 Gradle 构建脚本 defaultConfig 的 `applicationId`，或没有时的 `namespace`；写错：`AppScope/app.json5` 的 `bundleName` 仍是脚手架的 `com.example.…`，`vendor` 仍是 `example`
- rule-21676859b60f｜app.json5 的 vendor 仍是 example 时，开发期就从安卓来源落地，不随 bundleName 延后｜读到：安卓模块 Gradle 构建脚本里的 namespace / applicationId（反域名形式，第二段是组织），或源工程 README 里的作者、组织；写错：AppScope/app.json5 的 app.vendor 仍是 "example"，理由写成与签名或 AGC 绑定、部署期再改
- rule-f2eaceb25ee1｜app.json5 的 vendor 仍是模板值 example 时，改成非模板的厂商名，bundleName 可保留｜读到：目标工程的 AppScope/app.json5 由 DevEco 模板生成，app 段是模板默认值（`"vendor": "example"`、`"versionCode": 1000000`）；写错：交回的 app.json5 里 `"vendor": "example"` 原样保留（只改了 versionCode、versionName、label 等）
- rule-3138ba928aae｜身份落地写 app.json5 前，逐项比对验收门禁的模板值规则，冲突在交回前指出｜读到：派工或技能要求以受限范围（如 scope=dev-identity）只改部分身份字段，跳过 vendor、bundleName；写错：交回的 app.json5 里 vendor 为 "example"、bundleName 匹配 com.example.*，或 versionName 仍为 "1.0.0"，交回报告里没提这些正是验收门禁的 FAIL / WARN 项
- rule-37294b2e1fb7｜无部署期身份步骤而验收要求非 com.example 时，交付前按 applicationId 落 bundleName｜读到：安卓 app 模块 Gradle 构建脚本里 defaultConfig 的 `applicationId`（只有两段时尤其要注意）；写错：交付时 AppScope app.json5 的 `bundleName` 仍是 `com.example.*`、`vendor` 仍是 example
- rule-951b855e39fd｜bundleName/vendor 是模板值时按 applicationId 加 flavor 后缀写入｜读到：源工程构建脚本里有 applicationId 和 productFlavors 下的 applicationIdSuffix、namespace；skill 规则或派工写「不碰 bundleName / vendor（部署期）」「scope=dev-identity」；写错：app.json5 的 bundleName 仍是 com.example.* 模板值、vendor 仍是 example，交回说明写「原样保留，部署期 scope=full 落地」，而流水线里没有部署期步骤
