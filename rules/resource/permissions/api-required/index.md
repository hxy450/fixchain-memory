# 系统接口要的权限

源端有 uses-permission，或目标代码调了 http、Web、振动、剪贴板、定位这类要权限的系统接口时

## 触发族

- [module.json5 的权限声明（requestPermissions）](request-permissions/index.md)（9 条）：源 AndroidManifest 有 uses-permission，或目标代码调了要权限的系统接口（http.createHttp、Web、vibrator.startVibration、getSystemPasteboard().getData()、geoLocationManager）；module.json5 的 requestPermissions 缺对应的 ohos.permission.*，或 user_grant 权限缺 reason、usedScene
