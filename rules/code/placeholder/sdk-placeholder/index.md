# 第三方 SDK 的占位登记

agent 会看到什么：读过的领域 skill 写明 SDK 可从 ohpm 取（如 @tencent/wechat_open_sdk）并给了调起和回调写法，占位登记却写着待入仓；交回的代码里留着 PLACEHOLDER、FWD-REF 空实现

## 规矩

- rule-479b5a8a2aa9｜载入的领域 skill 说 SDK 可从 ohpm 取而登记写着待入仓时，报冲突，不保留占位｜读到：载入的领域 skill 写明 SDK 从 ohpm 获取（如 @tencent/wechat_open_sdk）并给出调起、回调和配置写法，而占位登记写着该 SDK「待入仓」；写错：代码写 `PLACEHOLDER` 占位标记，sendReq / handleWant / onResp 推到「入仓后回灌」，或者只留 FWD-REF 注释空实现；返回信封仍报 SDK 未入仓
