# Application 初始化链注册的广播接收器与系统监听要读本体写进规格：锚点、触发条件、承接方法与目标 API

## 何时使用

规格提取阶段，把源端 Application 初始化链里注册的 BroadcastReceiver、系统回调与监听写入 feature 规格时；覆盖检查准备把被引用的文件归为平台胶水时；实现阶段逐项迁移初始化链时

## 适用情境

Android 源在 Application 初始化链注册接收器（如监听 CONNECTIVITY_ACTION 的网络切换），接收器本体按前后状态判断后调用业务检测或上报，并传入专用触发来源常量；上游契约已点名该接收器，但它不在 feature 锚点内；目标需用 @ohos.net.connection 等监听等价实现。

## 例外与边界

- 只对经 Context.registerReceiver 动态注册的接收器成立；在清单里静态声明的 CONNECTIVITY_ACTION 接收器，应用 targetSdkVersion ≥ 24 时收不到该广播，源端可观察行为是从不触发，不据此新增目标端网络监听，在规格里按“不触发”记录。

## 原因

隐式触发入口不在页面与 ViewModel 的调用链里：规格只写显式触发入口、常量取值域只写“各场景传对应值”时，实现者拿不到触发条件，常量留在代码里却没有调用方；覆盖检查只按引用计数把接收器归为胶水，也发现不了其中的业务调用。

## 做法

1. 对初始化链里的 register*Receiver 与监听注册，读接收器本体；含业务调用就作为锚点写入 feature，写明数据流、服务层承接方法、触发条件（例如注册时记下初始网络类型，只在蜂窝 → Wi‑Fi 时触发）与目标 API。
2. 为常量取值域写验收项时，逐个取值列出源端调用方和目标承接位置；某个取值没有承接方时写明迁移或裁剪决定。
3. 实现阶段验收项列出多个触发来源时逐个找到调用点；逐项迁移初始化链遇到注册调用，读被注册类后实现等价监听，或登记占位、决策，不静默略过。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕@ohos.net.connection 的 NetConnection 调用 register 后，网络可用时触发 netAvailable，网络从连接到断开时触发 netLost，网络能力变化（如连通性变化）时触发 netCapabilitiesChange；netCapabilitiesChange 回调的 NetCapabilityInfo.netCap.bearerTypes 给出承载网络类型
- 〔做法第 1、3 步〕NetConnection 要监听某个事件，需先调 on 订阅该事件再调 register；用完要调 unregister 取消注册
- 〔做法第 1 步〕NetConnection.register 需要 ohos.permission.GET_NETWORK_INFO，该权限的授权方式是系统授权（system_grant），在 module.json5 声明即可，不弹运行时授权框
- 〔适用情境〕ConnectivityManager.CONNECTIVITY_ACTION（android.net.conn.CONNECTIVITY_CHANGE）已废弃，javadoc 说明它只尽量保持向后兼容，不反映多个网络同时连接等新能力
