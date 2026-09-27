# app

应用级入口与横切约定：入口 Ability 的平台级守护与 skills 声明、日志写法、应用身份（显示名、包名厂商、版本号）、设置项与平台能力

[上一级](../index.md)

## 子主题

- [entry](entry/index.md) — 入口 Ability（onCreate/onDestroy）需要补上的平台级守护，以及 module.json5 中入口 Ability 的 skills（深链）声明
- [identity](identity/index.md) — 应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取
- [logging](logging/index.md) — 日志 API 选择与工程内的日志约定
- [platform](platform/index.md) — 系统平台能力（后台任务、通知、画中画回退、动态取色）的实现、替代与降级，以及后台计时的恢复和退出清理
- [settings](settings/index.md) — 设置项迁移：偏好键与默认值之外，每个开关的运行期消费方与应用入口
