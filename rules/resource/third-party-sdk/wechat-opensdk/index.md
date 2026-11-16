# 微信 OpenSDK 的工程配置

agent 会看到什么：源端用微信 OpenSDK（WXAPIFactory、sendReq）拉起微信登录或支付，目标 oh-package.json5 的依赖和 module.json5 的 querySchemes

## 规矩

- rule-9c2889bb0a7b｜接微信 OpenSDK 时，加 ohpm 依赖，querySchemes 加 weixin 和 wxopensdk｜读到：源端用微信 OpenSDK 拉起微信登录或支付（WXAPI.sendReq）；写错：oh-package.json5 里没有 @tencent/wechat_open_sdk 依赖；entry 的 module.json5 里没有 querySchemes，或缺 weixin、wxopensdk
