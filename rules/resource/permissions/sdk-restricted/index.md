# 三方要求和受限的权限

要按三方 SDK 文档或插件默认申请在 requestPermissions 里加 ohos.permission.*，或真机安装因权限被拒时

## 触发族

- [module.json5 的 requestPermissions 权限声明](request-permissions/index.md)（3 条）：要在 module.json5 的 requestPermissions 里声明 ohos.permission.*（第三方 SDK 文档要求的、插件默认申请的），或真机安装因权限被拒；产物里声明了受限、系统级或所调接口没要求的权限
