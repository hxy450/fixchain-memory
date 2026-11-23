# 平台计费网络判定按承载显式映射，不直译为单一能力位

## 何时使用

网络基础层实现阶段，把 isActiveNetworkMetered 等平台判定改写为 @ohos.net.connection 实现时

## 适用情境

源以平台判定计费网络并门控刷新、下载、流播或图片，同一工具类对以太网另有放行；目标只能读取 networkCap 与 bearerTypes，SDK 声明没写各承载是否会置 NOT_METERED。

## 例外与边界

- 显式分支只覆盖源端结论确定、不随网络变化的承载（如以太网不计费、蜂窝计费）；Wi-Fi 这类结论取决于网络本身计费标记的承载，仍保留按 NET_CAPABILITY_NOT_METERED 判定，不因为加了按承载的分支就统一写成不计费。

## 原因

“缺 NET_CAPABILITY_NOT_METERED 即计量”依赖目标平台对每种承载的置位；修复期模拟器实测以太网不置该位，以太网被判为受限，后台刷新被静默取消。

## 做法

1. 先按承载列出源端实际结论（以太网不计费、蜂窝计费、Wi-Fi 看热点计费标记），对结论确定的承载按 bearerTypes 显式分支，或把该假设列为真机核验项。
2. 核对同一许可工具类内各函数对同一承载的结论一致（如自动下载已对以太网放行，计费与受限判定也应放行）。

## 可选检查

- 有以太网或模拟器时打印 bearerTypes 与 networkCap，确认受限判定为 false

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕安卓 ConnectivityManager.isActiveNetworkMetered() 由系统服务对当前活动网络给出是否计费的判定（用户对流量费用、流量限制敏感的网络算计费），不是应用读某一个能力位
- 〔原因 / 做法第 1 步〕模拟器以太网下 getNetCapabilitiesSync 读到 bearerTypes 为 [3]（以太网）、networkCap 为 [12, 15, 16]，不含 NET_CAPABILITY_NOT_METERED（11）；按「缺该位即计费」判定时以太网被判为计费受限
