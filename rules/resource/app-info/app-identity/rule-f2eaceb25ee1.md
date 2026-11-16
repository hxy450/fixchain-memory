# app.json5 的 vendor 仍是模板值 example 时，改成非模板的厂商名，bundleName 可保留

审的是：资源
触发（任一种）：
- 读到：目标工程的 AppScope/app.json5 由 DevEco 模板生成，app 段是模板默认值（`"vendor": "example"`、`"versionCode": 1000000`）；写错的样子：交回的 app.json5 里 `"vendor": "example"` 原样保留（只改了 versionCode、versionName、label 等）
适用范围：迁移中同步目标工程 AppScope/app.json5 的应用身份字段时，包括只做开发身份范围的同步
做法：
- 把 app 段的 vendor 改成非模板值：取现有 bundleName 的组织段（反域名第二段），或安卓模块 namespace / applicationId 的组织段；不随 bundleName 一起跳过
- bundleName 和签名配置保持现值不动，只改 vendor
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- vendor：字符串，长度不超过 255 字节，可缺省，缺省值为空：应用开发厂商的描述，用于展示（如关于页面）（出处：app-configuration-file.md，配置文件标签）
- "vendor": "example"：官方 app.json5 配置示例里的写法，即模板遗留值（出处：app-configuration-file.md，配置文件示例）
- bundleName 推荐反域名：第一级域名后缀，第二级厂商/个人名，第三级应用名：厂商名可取 bundleName 的第二段（出处：app-configuration-file.md，配置文件标签）
- 只把 vendor 改成与 bundleName 组织段一致的值、bundleName 与签名不动，签名全量构建通过，回读 vendor 已改：单独替换 vendor 不会引起签名不一致（出处：卡里修好并验证过）
针对本应用要查的：
- vendor 取什么值：目标工程 AppScope/app.json5 的 bundleName；或源工程应用模块的 Gradle 构建脚本里 android 块的 namespace / applicationId；取反域名的第二段（组织段）作 vendor。例：bundleName 是 com.acme.player 时取 acme
来源：1 张卡，1 个应用
- case-c164fb6e384f47fb7ecf（话费流量查询助手）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
