# app/nfc

NFC：Android Activity 级前台派发到 UIAbility 注册与可见页登记的仿真，清单声明的贴卡拉起入口（TAG_FOUND skills）及其运行时启停开关的作用范围；读卡入口前能力检查的不支持、已关闭、可用三分支

[上一级](../index.md)

## 本级经验

- [Android Activity 级 NFC 前台派发迁移时，按 UIAbility 前后台注册，再用可见顶页登记表仿真页面级开关与默认新标签处理](lesson-a4ee90eabe3eef99ddbe.lesson.md)
  - 时机：NFC 引擎与基类行为迁移阶段，把基类 onResume/onPause 的前台派发开关、onNewIntent 统一处理与“当前标签”判定分配给服务、页面与全局状态时
  - 情境：Android 多数页面继承基类：onResume 设置待处理组件并 enableForegroundDispatch，onPause 关闭，onNewIntent 统一处理新标签，卡或设备不支持时跳转信息页；全局保存任意技术的 Tag。目标 tag.registerForegroundDispatch 按 UIAbility 注册，页面用 Navigation/NavDestination 组织，服务切片不能改页面。
  - 例外：处理的是清单声明的贴卡拉起入口（intent-filter 的 TECH_DISCOVERED/TAG_DISCOVERED，目标 skills 声明）：那条路径由系统拉起应用，不经前台派发，也不受页面可见性登记影响
- [NFC 能力前置检查按源端三分支迁移：不支持、已关闭（打开系统 NFC 设置）、可用分别建模，不用一个布尔可用门折叠](lesson-5a140e45ecb578dd61ed.lesson.md)
  - 时机：规格提取与服务、ViewModel 实现阶段，把源端读卡入口前的 NFC 能力检查转写为服务接口、状态枚举、提示文案与验收条款时
  - 情境：Android 入口先判 NfcAdapter 是否为 null（设备不支持，提示后不导航），再判 isEnabled()（开关关闭时跳 Settings.ACTION_NFC_SETTINGS，返回后需再次点击），都通过才进入读卡；目标以 HarmonyOS 的 canIUse 系统能力与 nfcController 开关状态实现；用来取证的设备可能只覆盖其中一种结果（如测试机不支持 NFC）。
- [清单的 NFC TECH_DISCOVERED 贴卡拉起入口映射为 skills 的 TAG_FOUND + tag-tech，启停开关只作用于这条系统派发](lesson-89368bd540176a43d4a2.lesson.md)
  - 时机：规格提取与入口实现阶段，映射 AndroidManifest 中 NFC TECH_DISCOVERED（activity-alias 或 intent-filter 加 tech-list）入口及偏好里启停它的开关时
  - 情境：源应用用 activity-alias 声明 android.nfc.action.TECH_DISCOVERED（meta-data 指向 tech-list，如 NfcA）作为贴卡拉起入口，并在偏好里用 PackageManager.setComponentEnabledSetting 启停该 alias；各 Activity 另在 onResume 无条件开启前台派发；目标 module.json5 只有 home skill。
