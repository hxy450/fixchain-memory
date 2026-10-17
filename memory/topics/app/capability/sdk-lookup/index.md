# app/capability/sdk-lookup

判定无等价前先查 Kit、ohpm、SDK 声明与权限注解

[上一级](../index.md)

## 本级经验

- [三方算法库输出以库真值字面为契约，不自研子集](lesson-3f9e120416e534d4e6d5.lesson.md) · 阶段：spec/execute · 信号：ical4j, RRule, Recur, EventRecurrenceFormatter
- [动态取色用 getColors 加回退，写明弃用](lesson-9769c8f754044944d3ad.lesson.md) · 阶段：spec/execute · 信号：dynamicLightColorScheme, dynamicDarkColorScheme, @ohos.wallpaper, getColors
- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](lesson-e9890889e591196c3d0d.lesson.md) · 阶段：spec/plan/execute · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit
- [应用内开关蓝牙先查 access 开关接口再定方案](lesson-7a081dc36013a60358ac.lesson.md) · 阶段：spec/execute/repair · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable
- [无 OHOS 实现的插件先按底层能力建本地兼容插件](lesson-45739c78f9767dacbc81.lesson.md) · 阶段：spec/execute · 信号：dependency_overrides, platform_interface, MethodChannel, ohos/flutter_plugins
- [权限按目标 API 的 @permission 汇总](lesson-652974ce64a9243faebc.lesson.md) · 阶段：spec/execute · 信号：@permission, requestPermissions, module.json5, ohos.permission.READ_PASTEBOARD
- [计费网络判定按承载显式映射，不靠单能力位](lesson-20afdfffa13dc5bca10c.lesson.md) · 阶段：execute/verify · 信号：isActiveNetworkMetered, @ohos.net.connection, NET_CAPABILITY_NOT_METERED, bearerTypes
