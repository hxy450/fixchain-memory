# 规格要求照搬源端崩溃时，抛出点到生命周期入口之间不加 try/catch，也不放进不等待的 async

审的是：代码
触发（任一种）：
- 读到：规格、决策台账或派工写明某条源端异常照搬为崩溃（「throw 等价复刻」「勿加防护」），源端调用链上没有 catch（如 Arrays.fill 越界抛 ArrayIndexOutOfBoundsException 直接崩溃）；写错的样子：aboutToAppear 里调用 this.bootAsync() 不 await，整段包在 try { … } catch { hilog.error(…) } 里只记日志；或调用链上有 Promise.catch
适用范围：切片实现阶段，规格把某条源端未捕获异常定为照搬崩溃时，从抛出函数到生命周期入口的整条调用链
做法：
- 从抛出函数沿调用链核到生命周期入口（aboutToAppear 等），中间不新加 try/catch、Promise.catch，也不放进不被等待的 async 包装，让异常同步抛出
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 改成 aboutToAppear 同步执行、不捕获后，设备上进程退出，hilog 栈从抛出函数指回 aboutToAppear：修好的写法（出处：卡里修好并验证过）
- 被吞的 TypeError 经 JSON.stringify 只剩「{}」，日志看不出原因，ready 标志永不置位，画面空白、触摸全被丢弃：只记日志的 catch 会把崩溃变成空白页（出处：卡里修好并验证过）
未核实：返修没单独试「异步但不捕获」能否让进程退出，只验证了「同步且不捕获」
来源：1 张卡，1 个应用
- case-bc452cbde49f74ef19a3（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断；取值 2 ← 诊断
