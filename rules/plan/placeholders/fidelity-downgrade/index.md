# 动画和阴影的保真度降级登记

agent 会看到什么：源端有动画矢量图标、Compose elevation 阴影，交回的占位登记把永久降级登成 resolve_by 后续切片的 forward-ref 或 resource-pending-asset，或者单层 .shadow 近似没有登记成近似项

## 规矩

- rule-691cd7918e7b｜已知的永久保真度降级当场实现或报决策缺口，不登记成 resolve_by 后续切片的 forward-ref｜读到：源码有动画（如 rememberAnimatedVectorPainter 形变），实现写成静态图；写错：占位登记里有 forward-ref，resolve_by 指向后续某个 Slice，内容是「静态图标 = 动画丢失」这类永久降级
- rule-f50d9c2f8ab4｜资产已在、只缺状态帧时，不登记 resource-pending-asset 挂资源批次，在本文件实现｜读到：规格把动画矢量图标映射为 resource animation or equivalent symbol animation、要求 Keep observable state transition；目标里同名媒体已存在；写错：代码注释、占位登记或报告里给这个引用加 P-RES-ASSET-… kind=resource-pending-asset，resolve_by 写资源批次（如 Batch resource closure），或登记成 deferred
- rule-476981170f19｜单层 ShadowOptions 近似 Compose 平台阴影时，登记为需截图校准的视觉近似项｜读到：源端用 Compose elevation 投影（Modifier.shadow、Surface elevation）；写错：报告的近似项登记里没有这处阴影，代码注释把单层 .shadow 写成与 elevation「等价」的映射
- rule-5de701090ff2｜转换报告不把简化的动效记成「等价」「spec 认可」，与先例冲突时记成待修差异｜读到：规格或映射参考写「AnimatedVisibility expand/shrinkVertically → animateTo + transition（高度/透明）」，工程里已有页面只用透明度转场；写错：转换报告或代码注释把只做透明度 / scale(y) 的转场写成「展开收起动画等价」「spec 转换决策认可」「同族先例」「documented as 降级」，没有列成待修差异
