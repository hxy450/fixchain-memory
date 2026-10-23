# app/entry

入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入与结果回传、扩展能力与卡片登记

[上一级](../index.md)

## 本级经验

- [form_config 规格与刷新从源卡片声明换算，不填默认](lesson-bc48518f40742add0054.lesson.md) · 阶段：plan/execute · 信号：form_config, supportDimensions, defaultDimension, updateEnabled
- [intent-filter 逐条映射为 skills](lesson-daba8a5b555e6657d085.lesson.md) · 阶段：spec/execute · 信号：intent-filter, ohos.want.action.sendData, maxFileSupported, SEND_MULTIPLE
- [manifest 未声明的窗口缺省解析成目标值并指派](lesson-c1d7ec16bb02aa152c33.lesson.md) · 阶段：spec · 信号：AndroidManifest, screenOrientation, windowSoftInputMode, auto_rotation_restricted
- [shortcuts 元数据挂 Ability 下，不挂模块级](lesson-67118603fcc769a5edc9.lesson.md) · 阶段：execute/verify/repair · 信号：ohos.ability.shortcuts, module.json5, $profile:, shortcuts_config
- [前台服务改扩展能力先查基类导出，type 与基类成对](lesson-16c24b9a44153d703f04.lesson.md) · 阶段：spec/execute/repair · 信号：extensionAbilities, ServiceExtensionAbility, AppServiceExtensionAbility, WorkSchedulerExtensionAbility
- [卡片按实际宽高选布局，getFormRect 下发尺寸](lesson-7ad5a7d149de5bcec7da.lesson.md) · 阶段：execute · 信号：FormExtensionAbility, formProvider.getFormRect, onSizeChanged, formProvider.updateForm
- [固定快捷方式用 productViewManager](lesson-fe5cf66672ce205ee0d7.lesson.md) · 阶段：spec/execute · 信号：requestPinShortcut, isRequestPinShortcutSupported, disableShortcuts, ShortcutManager
- [外部入口页需确定快捷声明、Want 分支与参数写者](lesson-c46f182cf1d01a97e05f.lesson.md) · 阶段：spec/execute · 信号：ohos.ability.shortcuts, shortcuts_config.json, onNewWant, Want
- [多处 setResult 合并为一次带结果结束](lesson-2f8c5cc0c4cc4938ec79.lesson.md) · 阶段：spec/execute · 信号：setResult, RESULT_OK, RESULT_CANCELED, terminateSelfWithResult
- [深链声明 skills、domainVerify，隐式验收](lesson-d77baa7494930d485425.lesson.md) · 阶段：spec/execute · 信号：ohos.want.action.viewData, entity.system.browsable, pathStartWith, intent-filter
- [需显式 init 的封装在入口 onCreate 最早处调用](lesson-8a881c2e07f80f83447c.lesson.md) · 阶段：execute · 信号：UIAbility.onCreate, AbilityStage.onCreate, NetworkConfig.init, HttpClient
