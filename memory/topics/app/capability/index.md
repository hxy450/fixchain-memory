# app/capability

平台能力与厂商 SDK 的等价判定：先查 Kit、ohpm 与本地声明再选型，不可用时运行期显式降级而非阻断或伪造

[上一级](../index.md)

## 本级经验

- [决策批准的平台能力要真实现，只在运行期按结果降级](lesson-efb94f2d70d4df1c65d7.lesson.md) · 阶段：execute · 信号：backgroundTaskManager.startBackgroundRunning, ohos.permission.KEEP_BACKGROUND_RUNNING, notificationManager.requestEnableNotification, WantAgent
- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](lesson-e9890889e591196c3d0d.lesson.md) · 阶段：spec/plan/execute · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit
- [应用内开关蓝牙先查 access 开关接口再定方案](lesson-7a081dc36013a60358ac.lesson.md) · 阶段：spec/execute/repair · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable
- [应用内计时替代后台 Worker 时恢复入口共用扣减函数](lesson-35a684862ee500f08912.lesson.md) · 阶段：execute · 信号：WorkManager, backgroundTaskManager, keepScreenOn, WakeLock
- [打开系统设置的显式 Want 包名需在目标设备核对](lesson-4bea916d1ff67e51d455.lesson.md) · 阶段：execute · 信号：startAbility, bundleName, abilityName, com.huawei.hmos.settings
- [无 OHOS 实现的插件先按底层能力建本地兼容插件](lesson-45739c78f9767dacbc81.lesson.md) · 阶段：spec/execute · 信号：dependency_overrides, platform_interface, MethodChannel, ohos/flutter_plugins
- [激励广告不可用时显式提示并按台账放行，不伪造奖励](lesson-0f67121af7969203b76b.lesson.md) · 阶段：spec/execute/verify · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward
