# 源开关只启停系统派发入口时，替代开关也只拦系统派发，规格写明前台派发不受影响

审的是：规格
触发（任一种）：
- 读到：偏好保存时只对 activity-alias 调 setComponentEnabledSetting(…ENABLED/DISABLED, DONT_KILL_APP)；基类 onResume 无条件 enableForegroundDispatch；写错的样子：替代方案写成「开关 true = 注册前台 tag listener，false = 不注册」，验收条目要求开关两态下前台贴卡响应 / 不响应
适用范围：为「运行时启停系统派发入口」这类平台差异设计替代开关、写决策台账和验收条目时
做法：
- 先列出源开关实际影响的路径（只影响被启停组件的系统派发和选择列表可见性，不影响前台派发），替代实现只作用于同一路径
- 决策台账和验收条目里写明：开关关闭时只拦系统派发拉起（冷启动 terminateSelf、热启动退回后台），前台派发照常响应
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setComponentEnabledSetting：设置包内组件（activity、receiver、service、provider）的启用状态：源开关的作用范围只是被启停的组件（出处：android.content.pm.PackageManager#setComponentEnabledSetting）
- 开关只拦系统派发：关闭时 TAG_FOUND 冷启动 terminateSelf、热启动退回后台，前台派发不受影响：修复后的替代语义（出处：卡里修好并验证过）
针对本应用要查的：
- 源开关实际影响的组件和路径：源工程里调用 setComponentEnabledSetting 的代码，以及各 Activity 基类的 onResume / onPause；看被启停的 ComponentName 是哪个清单组件；看 enableForegroundDispatch 是否受同一偏好控制
来源：1 张卡，1 个应用
- case-d923c5dbfc1e66ce5f8b（MifareClassicTool）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
