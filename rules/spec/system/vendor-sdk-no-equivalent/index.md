# 被归为「三方无等价」的厂商或三方 SDK 能力

agent 会看到什么：读到源端通过厂商或三方 SDK 用某项能力（如 HMS 账号授权），映射参考里可能写着可对到某个 Kit；规格把这个通道归入「三方无等价」HARD-DIV，写「无 1:1 等价 → 占位」，没查目标是否有系统 Kit 或厂商鸿蒙版

## 规矩

- rule-e90420906147｜源端用厂商账号 SDK 时，规格先查目标是否有系统 Kit，有就写平台 API，不归三方无等价｜读到：源端通过 HMS 账号 SDK 发起华为账号授权（反射装载实现、Empty 回退控制按钮可见性），产出 authorizationCode 交后端绑定；映射参考或 UI 规格写着「可映射华为 Account Kit」；写错：规格把这个通道归入「三方无等价」HARD-DIV，写「无 1:1 等价 → 占位」，替代路径写「Account Kit vs 占位，grill #N 裁决」
- rule-c4e5862869fc｜源端依赖高德 com.amap.api.* 时，C8 决策先查厂商鸿蒙 SDK，写明 ohpm 包、版本和 Key 前置｜读到：Android 工程依赖 com.amap.api.*（高德地图、定位、搜索、导航 SDK），api-inventory 或 feature spec 写着高德能力，skill 映射表把高德列为 hmos-sdk-docs 的厂商 SDK；写错：决策台账的 C8 决策写「优先 HarmonyOS Kit；无等价能力时使用 Web/H5 或受控降级」，依据是「未提供 SDK 资料」或用户只答「采用建议」，没有厂商鸿蒙 SDK 这一档，「鸿蒙等价 SDK 可用性」的风险项被标 answered 关闭
- rule-5907d119182a｜规格对闭源三方 SDK 写「鸿蒙无等价」前，先查 ohpm 和厂商鸿蒙版，没查只能标待确认｜读到：源端用闭源三方 SDK（如微信 OpenSDK：WXAPI.sendReq / handleIntent、WXEntryActivity、WXPayEntryActivity 回调）；写错：页面规格的转换决策写「鸿蒙端无某 SDK 官方适配，回调链路不可复刻，仅保留状态接口」，没有 ohpm 或厂商鸿蒙版的查询结果
