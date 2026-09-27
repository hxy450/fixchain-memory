# app

应用级入口与横切约定：入口 Ability 的初始化、平台级守护与 skills 声明，冷启动链路，Flutter 混合工程的原生桥接，日志写法、应用身份、设置项与平台能力

[上一级](../index.md)

## 子主题

- [entry](entry/index.md) — 入口 Ability（onCreate/onDestroy）：基础设施的显式初始化时机、需要补上的平台级守护，以及 module.json5 中入口 Ability 的 skills（深链）声明
- [hybrid](hybrid/index.md) — Flutter 与原生混合工程：MethodChannel handler 的方法集合、flutter_boost 宿主页的事件通道、原生路由分流
- [identity](identity/index.md) — 应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取
- [logging](logging/index.md) — 日志 API 选择与工程内的日志约定
- [platform](platform/index.md) — 系统平台能力（后台任务、通知、画中画回退、动态取色）的实现、替代与降级，以及后台计时的恢复和退出清理
- [settings](settings/index.md) — 设置项迁移：偏好键与默认值之外，每个开关的运行期消费方与应用入口
- [startup](startup/index.md) — 冷启动链路：闪屏路由、各去向页的初始化请求，以及登录态组合在哪里处理
