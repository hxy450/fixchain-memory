# 源端 isActiveNetworkMetered 迁成能力位判定时，BEARER_ETHERNET 先判为不计费

审的是：代码
触发（任一种）：
- 读到：源端计费判定直接返回 ConnectivityManager.isActiveNetworkMetered()，受限判定是「计费 || 蜂窝」，刷新、下载、流播、图片许可都由它门控；写错的样子：目标端写成 !networkCap.includes(NET_CAPABILITY_NOT_METERED) 即计量，没有按 bearerTypes 区分承载
- 读到：源端同一工具类里另有对 ConnectivityManager.TYPE_ETHERNET 直接放行的分支；写错的样子：目标端同一文件里一个函数按 BEARER_ETHERNET 放行，计费、受限判定和它们门控的许可却对以太网不放行
适用范围：把安卓 ConnectivityManager 的计费、受限网络判定改写成 @ohos.net.connection 的 NetCapabilities 判定时
做法：
- 先按承载列出源端的实际结论（以太网不计费、蜂窝计费），再写目标判定，不把平台查询直译成单一能力位
- 计费判定里，无网络的判断之后先写 if (caps.bearerTypes.includes(connection.NetBearType.BEARER_ETHERNET)) return false；其余承载才按 !caps.networkCap?.includes(connection.NetCap.NET_CAPABILITY_NOT_METERED) 判为计量
- 核对同一许可工具类里各函数对同一承载的结论一致：已对 BEARER_ETHERNET 放行的，计费、受限判定及其门控的许可也放行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- NetCap.NET_CAPABILITY_NOT_METERED = 11：网络流量不计费的能力位（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetCap.NET_CAPABILITY_NOT_METERED）
- NetBearType.BEARER_ETHERNET = 3：以太网承载（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetBearType.BEARER_ETHERNET）
- networkCap?: Array<NetCap>；bearerTypes: Array<NetBearType>：NetCapabilities 的两个字段；networkCap 可选，取值前判空（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetCapabilities）
- getNetCapabilitiesSync(netHandle: NetHandle): NetCapabilities；getDefaultNetSync(): NetHandle：拿默认网络的能力集（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，connection.getNetCapabilitiesSync、connection.getDefaultNetSync）
- 模拟器以太网 bearerTypes 为 [3]、networkCap 为 [12, 15, 16]，不含 11；只看能力位时被判为受限，刷新被静默取消；加以太网分支后恢复：目标平台的以太网不置 NOT_METERED（出处：卡里修好并验证过）
- isActiveNetworkMetered()：Returns if the currently active data network is metered，结果由系统服务给出：源端的计费口径是平台按网络判定的，不是一个能力位（出处：android.net.ConnectivityManager#isActiveNetworkMetered）
未核实：安卓以太网默认带 NOT_METERED 出自修复时的注释，本机框架源码里没查到原文；Wi-Fi 承载在目标端是否按热点计费置位，卡里没有验证
来源：1 张卡，1 个应用
- case-97a68832f5589778975e（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断、建议 2；做法第 3 步 ← 建议 3；取值 5 ← 诊断
