# arkts/api-signatures

调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定

[上一级](../index.md)

## 本级经验

- [intl 货币格式化须显式传 currency 码](lesson-19cedec8ad1bc4b08b2c.lesson.md) · 阶段：execute/repair · 信号：intl.NumberFormat, getCurrencyInstance, style: 'currency', @kit.LocalizationKit
- [tabBar 不接受 { title } 对象字面量](lesson-b402fa546504a1dd6db7.lesson.md) · 阶段：execute/repair · 信号：TabContent, .tabBar(, TabBarOptions, BottomTabBarStyle
- [依赖 API 单位与作用范围时两端都读语义说明](lesson-f5cf8413ebea57f3b415.lesson.md) · 阶段：spec/execute · 信号：vp2px, px2vp, .d.ts, uiContext
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](lesson-6e558834938be19c04e2.lesson.md) · 阶段：execute/repair · 信号：ets/component, ets/api, AppStorageV2.connect, getHostContext
- [单调计时映射 getUptime 并选 TimeType](lesson-ce456d60534d97524aa4.lesson.md) · 阶段：spec/execute/repair · 信号：System.nanoTime, SystemClock.elapsedRealtime, systemDateTime.getUptime, TimeType.ACTIVE
- [属性方法不传 ResourceStr 联合值按重载定型](lesson-63660a8304f7d3920bfc.lesson.md) · 阶段：spec/execute · 信号：accessibilityText, ResourceStr, @Computed, contentDescription
- [禁编译写大页后对照this成员常量导入与$r键声明](lesson-e04e26f1f98116275982.lesson.md) · 阶段：execute/repair · 信号：$r('app., resources/base/element, @Local, @Param
