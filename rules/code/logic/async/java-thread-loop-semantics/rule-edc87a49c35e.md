# 源码重连循环只在连上后退出时，目标循环内不加取消出口，取消留到下一轮检点

审的是：代码
触发（任一种）：
- 读到：源码 while (!isConnected()) { sleep(500); connect(); }，循环内不检查取消，取消只在外层每一轮的检点生效；写错的样子：目标的重连 while (!….isConnected()) 循环里加了 if (<取消标志>) return -1 这类出口
适用范围：把安卓 NFC 引擎里的自动重连等待循环迁到 TagSession 接口时
不适用的情形：决策台账已把新增的取消或超时出口登记为显式偏离、对应 AC 也已同步改过的
做法：
- 重连循环照源码只在 isConnected() 为真时退出，循环体内是等待加 connect()；取消在外层下一轮检点再响应，不在循环内 return
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- isConnected(): boolean：循环的退出判定（出处：鸿蒙 SDK 的 ets/api/tag/tagSession.d.ts，TagSession.isConnected）
- connect(): void：同步连接，失败以 BusinessError 3100201 等抛出（出处：鸿蒙 SDK 的 ets/api/tag/tagSession.d.ts，TagSession.connect）
未核实：修复未上真机（NFC 不可达），按源码对照
来源：1 张卡，1 个应用
- case-68b0d7a44f60b8170647（MifareClassicTool）：做法第 1 步 ← 诊断；例外 1 ← 建议 4
