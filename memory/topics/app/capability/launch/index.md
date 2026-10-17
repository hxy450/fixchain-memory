# app/capability/launch

拉起外部应用、系统设置与分享：Want 预检与目标核对

[上一级](../index.md)

## 本级经验

- [应用内分享面板复用应用内弹层并逐渠道映射](lesson-b366cf7ae68525577f57.lesson.md) · 阶段：spec/execute · 信号：ShareUtil, ShareItem, shareItems, platformName
- [打开系统设置的显式 Want 包名需在目标设备核对](lesson-4bea916d1ff67e51d455.lesson.md) · 阶段：execute · 信号：startAbility, bundleName, abilityName, com.huawei.hmos.settings
- [隐式 Want 先 canOpenLink 预检，不靠抛错](lesson-948d876672049969b865.lesson.md) · 阶段：spec/execute · 信号：bundleManager.canOpenLink, querySchemes, 17700056, startAbility
