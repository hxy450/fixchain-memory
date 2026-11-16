# 调用振动接口时，module.json5 要声明 ohos.permission.VIBRATE

审的是：资源
触发（任一种）：
- 读到：AndroidManifest.xml 有 `<uses-permission android:name="android.permission.VIBRATE" />`，代码里调 Vibrator；写错的样子：目标 module.json5 的 requestPermissions 里没有 ohos.permission.VIBRATE
- 写错的样子：代码里有 vibrator.startVibration，但 module.json5 的 requestPermissions 里没有 ohos.permission.VIBRATE
适用范围：目标端移植了源端的振动反馈（按键振动、步骤切换振动等，用 vibrator.startVibration）时的模块配置
做法：
- 在 module.json5 的 module.requestPermissions 里加 { "name": "ohos.permission.VIBRATE" }；它是 system_grant，reason、usedScene 可不填，也不用运行时弹窗申请
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @permission ohos.permission.VIBRATE：startVibration 的权限要求（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，vibrator.startVibration）
- ohos.permission.VIBRATE：权限级别 normal，授权方式 system_grant：声明即授予，只要在配置里声明，不需要运行时申请（出处：permissions-for-all.md，ohos.permission.VIBRATE）
- requestPermissions 每项的 name 必填；reason 申请 user_grant/manual_settings 时必填，usedScene 申请 user_grant/manual_settings 时必填：声明权限的格式（出处：declare-permissions.md，在配置文件中声明权限）
- Vibrator 的振动方法标注 @RequiresPermission(android.Manifest.permission.VIBRATE)：源端同样要声明权限（出处：android.os.Vibrator#vibrate）
来源：2 张卡，2 个应用
- case-290eac71ee43fe336138（Cofi）：做法第 1 步 ← 建议 2、诊断
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 1 步 ← 建议 4、诊断
