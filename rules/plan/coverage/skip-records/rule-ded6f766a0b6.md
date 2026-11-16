# 跳过清单登记「平台无对等、降级」前先检索 SDK，写明检索词和命中接口

审的是：计划与派工
触发（任一种）：
- 读到：源端功能依赖系统级能力，源码自带版本门槛和不支持时的回退分支；写错的样子：skip-list 行写「<能力> | 平台无对等 | HMOS 无 X API；降级为固定方案」，没有检索词、命中的 d.ts 或检索为空的记录
适用范围：写 skip-list 里因平台能力缺失而跳过或降级的条目时
做法：
- 登记前在 hwsdk.dir 的 openharmony/ets/api、hms/ets/api 和 kits 导出里按能力关键词检索；有命中就不写「平台无对等」，改记接口和标注；检索为空才登记，并写明检索词和路径
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getColors(wallpaperType: WallpaperType): Promise<Array<RgbaColor>>，@deprecated since 9：例：「HMOS 无取色 API」与公开 SDK 不符（出处：鸿蒙 SDK 的 ets/api/@ohos.wallpaper.d.ts，wallpaper.getColors）
来源：1 张卡，1 个应用
- case-33b4b9ce51ba471ee770（Cofi）：做法第 1 步 ← 建议 1、诊断
