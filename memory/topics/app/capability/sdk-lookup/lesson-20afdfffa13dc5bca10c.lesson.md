# 平台计费网络判定按承载显式映射，不直译为单一能力位

ID：`lesson-20afdfffa13dc5bca10c` · 版本：2 · 阶段：execute/verify · 主题：[app/capability/sdk-lookup](index.md)

概要：计费网络判定按承载显式映射，不靠单能力位

信号：`isActiveNetworkMetered`, `@ohos.net.connection`, `NET_CAPABILITY_NOT_METERED`, `bearerTypes`, `networkCap`

## 何时使用

网络基础层实现阶段，把 isActiveNetworkMetered 等平台判定改写为 @ohos.net.connection 实现时

## 适用情境

源以平台判定计费网络并门控刷新、下载、流播或图片，同一工具类对以太网另有放行；目标只能读取 networkCap 与 bearerTypes，SDK 声明没写各承载是否会置 NOT_METERED。

## 原因

“缺 NET_CAPABILITY_NOT_METERED 即计量”依赖目标平台对每种承载的置位；修复期模拟器实测以太网不置该位，以太网被判为受限，后台刷新被静默取消。

## 做法

1. 先按承载列出源端实际结论（以太网不计费、蜂窝计费、Wi-Fi 看热点计费标记），对结论确定的承载按 bearerTypes 显式分支，或把该假设列为真机核验项。
2. 核对同一许可工具类内各函数对同一承载的结论一致（如自动下载已对以太网放行，计费与受限判定也应放行）。

## 可选检查

- 有以太网或模拟器时打印 bearerTypes 与 networkCap，确认受限判定为 false

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-97a68832f5589778975e](../../../../../store/cases/case-97a68832f5589778975e/c2829f25cb0576de59b8512a1174405a3df508a28bbc196c7c716cd182d55970.json) · 结论：diagnosis, rec-55dbbe9e7d, rec-1f87f7a851, rec-f790a42738
  卡片版本：`c2829f25cb0576de59b8512a1174405a3df508a28bbc196c7c716cd182d55970`
