# 规格或账本已把外部意图入口归给别的 feature 时，不判「平台无入口」，登记 FWD-REF

审的是：计划与派工
触发（任一种）：
- 读到：决策账本或规格写意图协议（ACTION_VIDEO_CAPTURE、EXTRA_OUTPUT、EXTRA_VIDEO_QUALITY 等）由另一个 feature 实现；写错的样子：文件头或源码笔记写「目标平台无第三方 intent 入口」「运行时无注入路径」，意图参数只留默认空的注入函数，没有登记跨切片 FWD-REF
适用范围：切片实现时，外部意图入口归另一个切片或 feature 负责，本切片只管录像、保存管线的情形
做法：
- 为 EXTRA_VIDEO_QUALITY / EXTRA_DURATION_LIMIT / EXTRA_SIZE_LIMIT / EXTRA_OUTPUT 保留注入面，登记跨切片 FWD-REF，写明由入口页面从 launch want 构造并注入
- 组内接线时检查每个 worker 留下的注入面是否都有调用方
来源：1 张卡，1 个应用
- case-76fcde297f6a5406e58f（opencamera-hmos）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 5
