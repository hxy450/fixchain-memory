# 权限声明

源 AndroidManifest 有 uses-permission，或目标 module.json5 的 requestPermissions 里要声明 ohos.permission.* 时

## 子主题

- [系统接口要的权限](api-required/index.md)（9 条）：源端有 uses-permission，或目标代码调了 http、Web、振动、剪贴板、定位这类要权限的系统接口时
- [三方要求和受限的权限](sdk-restricted/index.md)（3 条）：要按三方 SDK 文档或插件默认申请在 requestPermissions 里加 ohos.permission.*，或真机安装因权限被拒时
