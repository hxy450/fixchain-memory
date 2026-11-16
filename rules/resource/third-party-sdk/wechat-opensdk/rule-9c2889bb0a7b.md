# 接微信 OpenSDK 时，加 ohpm 依赖，querySchemes 加 weixin 和 wxopensdk

审的是：资源
触发（任一种）：
- 读到：源端用微信 OpenSDK 拉起微信登录或支付（WXAPI.sendReq）；写错的样子：oh-package.json5 里没有 @tencent/wechat_open_sdk 依赖；entry 的 module.json5 里没有 querySchemes，或缺 weixin、wxopensdk
适用范围：目标工程接入鸿蒙版微信 OpenSDK 时的工程配置
做法：
- oh-package.json5 的 dependencies 加 @tencent/wechat_open_sdk（在线装不了时用本地 HAR）
- entry 模块 module.json5 加 "querySchemes": ["weixin", "wxopensdk"]
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- querySchemes：允许当前应用跳转查询的 URL scheme，只允许 entry 类型模块配置，每个不超过 128 字节：weixin、wxopensdk 要写在 entry 模块里（出处：module-configuration-file.md，配置文件标签）
- querySchemes 增加 weixin、wxopensdk，依赖改为本地 HAR 后链路可用：修好的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-febf3c781ebde9778c30（DeepAI全能PPT）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 2 ← 诊断
