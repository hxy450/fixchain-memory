# 靠 d.ts 没说明语义的错误码分流被拒与丢卡时，加 isConnected() 在场复核并登记真机待验

审的是：代码
触发（任一种）：
- 读到：目标 d.ts 里 authenticateSector 只列 BusinessError 201/401/3100201/3100204，没说哪个码是密钥被拒、哪个是丢卡；写错的样子：适配器只按单个 err.code（3100201 或 3100204）判被拒或丢卡，没有 isConnected() 这类在场复核，码值假设也没进真机待验项
适用范围：用 MifareClassicTag 等 NFC 标签接口的 reject 码区分被拒与丢卡时
做法：
- 被拒与丢卡不只靠单个码分流：reject 后调 isConnected() 复核在场（或配合重连），不在场才按丢卡 throw，在场按被拒返回 false
- 把所用码值的假设（哪个码当被拒、哪个当丢卡）写进真机待验项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- isConnected(): boolean：TagSession 的在场判定，MifareClassicTag 继承它（@since 12）（出处：鸿蒙 SDK 的 ets/api/tag/tagSession.d.ts，TagSession.isConnected）
- 3100201 的可能原因同时列了「Tag操作前，已经处在断开状态」和「Tag芯片返回错误状态或响应超时」：同一个码既可能是丢卡也可能是卡片拒绝，单靠它分不开（出处：errorcode-nfc.md，3100201 NFC服务读写Tag错误）
- 3100204 可能原因：NFC Tag不支持所执行的读写操作：文档没把它写成丢卡（出处：errorcode-nfc.md，3100204 NFC芯片I/O异常）
未核实：没有真机材料能确认密钥错误和拔卡时 authenticateSector 分别返回哪个码
来源：1 张卡，1 个应用
- case-68b0d7a44f60b8170647（MifareClassicTool）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
