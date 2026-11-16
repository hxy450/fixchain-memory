# 载入的领域 skill 说 SDK 可从 ohpm 取而登记写着待入仓时，报冲突，不保留占位

审的是：代码
触发（任一种）：
- 读到：载入的领域 skill 写明 SDK 从 ohpm 获取（如 @tencent/wechat_open_sdk）并给出调起、回调和配置写法，而占位登记写着该 SDK「待入仓」；写错的样子：代码写 `PLACEHOLDER` 占位标记，sendReq / handleWant / onResp 推到「入仓后回灌」，或者只留 FWD-REF 注释空实现；返回信封仍报 SDK 未入仓
适用范围：执行阶段实现三方 SDK 相关代码，占位登记和领域 skill 说法矛盾时
做法：
- 在返回信封里报告冲突：登记说待入仓，skill 说可从 ohpm 获取，交编排者改判
- 不默认保留占位；改判后按 skill 实装 createWXAPI / sendReq / handleWant 和 onResp 分派
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 实装 createWXAPI、sendReq、handleWant 和 onResp 分派，去掉占位后登录、支付链路可用：修好的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-febf3c781ebde9778c30（DeepAI全能PPT）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断
