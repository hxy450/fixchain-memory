# ConnectivityManager 的网络类型和计费判断

agent 会看到什么：读到源端注册 CONNECTIVITY_ACTION 接收器、getActiveNetworkInfo 按 TYPE_WIFI / TYPE_MOBILE / TYPE_ETHERNET 分支，或 isActiveNetworkMetered；交回的没有 createNetConnection 监听，或计费只看 NET_CAPABILITY_NOT_METERED、不按 bearerTypes 区分

## 规矩

- rule-0b82bc0ca2d3｜初始化链注册网络切换接收器时，目标用 createNetConnection 实现等价监听｜读到：源端 Application 初始化链调用 register…Receiver() 注册 CONNECTIVITY_ACTION 接收器，注册前给“上次网络类型”赋初值，onReceive 里按前后网络类型调用业务检测；写错：目标只声明了对应的来源常量，没有任何调用方，也没有 createNetConnection 监听；或逐项迁移 init 链时静默略过这个接收器，没有占位也没有决策记录
- rule-8d5e1acaa121｜源端 isActiveNetworkMetered 迁成能力位判定时，BEARER_ETHERNET 先判为不计费｜读到：源端计费判定直接返回 ConnectivityManager.isActiveNetworkMetered()，受限判定是「计费 || 蜂窝」，刷新、下载、流播、图片许可都由它门控；写错：目标端写成 !networkCap.includes(NET_CAPABILITY_NOT_METERED) 即计量，没有按 bearerTypes 区分承载
