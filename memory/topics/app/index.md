# app

应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

[上一级](../../index.md)

## 子主题

- [capability](capability/index.md) — 平台能力与厂商 SDK 的等价判定、运行期降级与外部能力拉起（15 条）
- [cross-cutting](cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线（8 条）
- [entry](entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入声明、扩展能力与卡片登记（10 条）
- [hybrid](hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对（5 条）
- [map](map/index.md) — 地图与定位接入：SDK 单例初始化与就绪、定位权限成组、坐标系与行政区名补齐、原生地图组件生命周期（5 条）
- [media](media/index.md) — 媒体文件的用户可见出入口：安全控件与 picker 授权时序、沙箱落点与导出、播放 URI、预取与快照尺寸限制（9 条）
- [modules](modules/index.md) — 多模块（壳 HAP + HAR）边界：构建常量来源、跨模块导入、资源闭包归属与可复用函数的模块放置（5 条）
- [nfc](nfc/index.md) — NFC 读卡：能力三态前置检查、贴卡拉起的 skills 声明、按 UIAbility 前台派发与页面仿真（3 条）
- [notification](notification/index.md) — 通知与代理提醒：WantAgent 按钮 requestCode 与刷新、通知字段约束、代理提醒边界与回退（2 条）
- [playback](playback/index.md) — 音视频播放：AVPlayer/SoundPool 设源与状态机、错误通道、装载令牌与释放、后台播放（9 条）
- [recreation](recreation/index.md) — 源端 Activity 重建语义：配置变化、进程回收与重启在不重建的 UIAbility 上显式处理与恢复（5 条）
- [resources](resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验（11 条）
- [startup](startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫（8 条）
- [system-state](system-state/index.md) — 系统能力的异步状态真值：终态回读、分协议聚合、回调会话归属、同步抛错收敛、读后增量写回与返回值判定（6 条）
- [window](window/index.md) — 窗口级行为：Activity 窗口标志与画中画映射到共享主窗口/PiPWindow 的作用范围与状态（2 条）
