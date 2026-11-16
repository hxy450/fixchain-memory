# 源码带版本门槛和回退分支的系统能力，规格映射成「能力探测 + 原回退」，不直接降级

审的是：规格
触发（任一种）：
- 读到：源码 if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && 开关) 用动态配色，否则回退固定 light / dark scheme；设置行 enabled = SDK_INT >= S；写错的样子：规格或台账写成「固定双配色」二值解析，验收条目要求「产物不含取色 API 调用与版本门槛分支」，设置行恒可用但无效果
适用范围：源端系统能力自带「不支持时回退」分支、目标侧要决定实现还是降级时
做法：
- 规格写「能力探测 + 原回退」：取色（或该能力）成功就生成配色，失败用原固定双配色；设置行 enabled 绑定能力是否可用
- 只有确认公开 SDK 没有任何可调用入口，才登记降级，PD 保持 proposed 进入确认表
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Build.VERSION_CODES.S = 31：源端动态取色的版本门槛（出处：android.os.Build.VERSION_CODES#S）
- getColors(wallpaperType: WallpaperType): Promise<Array<RgbaColor>>，@deprecated since 9：取色能力探测用的公开入口（出处：鸿蒙 SDK 的 ets/api/@ohos.wallpaper.d.ts，wallpaper.getColors）
来源：1 张卡，1 个应用
- case-33b4b9ce51ba471ee770（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2
