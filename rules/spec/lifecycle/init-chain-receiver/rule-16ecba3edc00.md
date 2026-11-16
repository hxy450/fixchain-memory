# Application 初始化链注册的广播接收器调业务时，规格要把它作锚点并写明触发条件和目标 API

审的是：规格
触发（任一种）：
- 读到：源端 Application 初始化链里调用 register*Receiver 注册 BroadcastReceiver（如 CONNECTIVITY_ACTION），或上游契约文档点名某个接收器会触发业务检测、上报；写错的样子：feature 规格的 android_source_anchors 没有这个接收器，数据流、服务层承接方法和 AC 里都没有这个触发入口，也没有迁移或裁剪决定
适用范围：规格提取阶段处理 Application 初始化里注册的广播接收器、系统回调和监听这类隐式触发入口时
做法：
- 读接收器本体（onReceive）；其中调用业务检测或上报的，把它作为锚点写进 feature
- 在数据流、服务层承接方法和 AC 里写明触发条件（如“注册时记录初始网络类型，仅上次为蜂窝、本次为 Wi‑Fi 时调用检测并传对应来源常量”）和目标 API（网络切换用 @ohos.net.connection 的 createNetConnection）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ConnectivityManager.CONNECTIVITY_ACTION = "android.net.conn.CONNECTIVITY_CHANGE"（已废弃，建议改用 registerNetworkCallback 等）：源端网络切换广播（出处：android.net.ConnectivityManager#CONNECTIVITY_ACTION）
- function createNetConnection(netSpecifier?: NetSpecifier, timeout?: number): NetConnection：目标端网络状态监听的入口（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，connection.createNetConnection）
针对本应用要查的：
- 接收器里的触发条件和调用的业务方法：源工程里 Application 初始化链注册的接收器类的 onReceive，以及注册前给状态变量赋初值的那段；记下前后状态怎么比较、在什么条件下调用哪个业务方法、传什么来源常量
来源：1 张卡，1 个应用
- case-c234d95411230bdbffda（DeepAI全能PPT）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
