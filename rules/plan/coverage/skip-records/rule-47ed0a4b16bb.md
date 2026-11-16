# 跳过宽度限定目录时，逐键登记被覆盖的值为运行时断点并写明承接方

审的是：计划与派工
触发（任一种）：
- 读到：源工程 res 下有 values-w<N>dp、values-sw<N>dp、values-h<N>dp 这类尺寸限定目录，里面的 dimens.xml 覆盖了 values/dimens.xml 的同名键；转换规则写这类目录 skip entire directory, mark as unmapped；写错的样子：resource-mapping 里只写该目录“跳过（unmapped）”或“由某 feature 处理”，被点名的 feature spec 里并没有对应条目；placeholder-registry 里没有这项运行时断点，回执也没提
适用范围：资源迁移阶段遇到 HarmonyOS 没有对应限定词的宽度、最小宽度、高度限定目录时
做法：
- 跳过前逐键列出被覆盖的值：键名、基础值、覆盖值、阈值（如“某 dimen 基础 Xdp → 可用宽 ≥ Ndp 时 Ydp”）
- 在 resource-mapping 和 placeholder-registry 里各登记一条“运行时断点”需求，写明承接方（公共窗口模型或具体切片）和 resolve_by，并写进回执
- 写“由 Fxxx 处理”之前先 grep 该 feature spec，确认已有对应条目；没有就登记，不写空头承接
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HarmonyOS 限定词只有移动国家码和移动网络码、语言、文字、国家或地区、横竖屏、设备类型、颜色模式和屏幕密度：没有可用宽度维度，宽度限定的覆盖只能在运行时按窗口宽度判定（出处：resource-categories-and-access.md，限定词目录）
- Configuration.screenWidthDp 对应 available width 资源限定词，是应用可用显示区的宽度（dp）：values-w<N>dp 的阈值比较的是这个宽度（出处：android.content.res.Configuration#screenWidthDp）
针对本应用要查的：
- 哪些键被尺寸限定目录覆盖、基础值、覆盖值和阈值：源工程 res 下所有 values-w<N>dp、values-sw<N>dp、values-h<N>dp 目录里的 dimens.xml，和 values/dimens.xml 按键名对照；同名键在基础目录和限定目录各取一个值；目录名里的 N 就是阈值（dp），w 是可用宽、sw 是最小宽度、h 是可用高
来源：1 张卡，1 个应用
- case-99fd06c7bad0581426fb（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1、诊断
