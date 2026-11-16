# 三方 SDK 和插件

源端接了微信 OpenSDK 等三方 SDK 或 Flutter 插件；目标端有 oh-package.json5 的依赖、querySchemes，或根 pubspec.yaml 的 dependency_overrides 时

## 触发族

- [微信 OpenSDK 的工程配置](wechat-opensdk/index.md)（1 条）：源端用微信 OpenSDK（WXAPIFactory、sendReq）拉起微信登录或支付，目标 oh-package.json5 的依赖和 module.json5 的 querySchemes
- [根 pubspec.yaml 的 dependency_overrides](flutter-dependency-overrides/index.md)（1 条）：读到插件解析记录（plugin-resolution.json）或各插件 solution 里列为未决、F3 的包；根 pubspec.yaml 的 dependency_overrides 给别的插件加了本地 path:，漏了某个未决包
