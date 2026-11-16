# 按范围政策排除有对等能力的功能时，台账分别写能力可行和政策排除

审的是：规格
触发（任一种）：
- 读到：源端有 `AppWidgetProvider`、`RemoteViews`、小组件配置 Activity，功能规格已把它映射到 Form Kit（FormExtensionAbility + ArkTS 卡片）；写错的样子：台账的排除条目依据只有政策条文和源端调用链（如「仅被 APPWIDGET_UPDATE 链路触达」），没写目标平台对等能力的结论
适用范围：决策台账里按范围政策（C2 类）排除桌面小组件等扩展入口的条目
做法：
- 条目里分两项写：「能力可行：Form Kit（FormExtensionAbility + ArkTS 卡片），规格已有映射」和「政策排除：默认政策 C2」，排除理由只写范围政策，不写「无对等」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare class FormExtensionAbility，onAddForm(want: Want): formBindingData.FormBindingData：鸿蒙卡片的提供方，桌面小组件的对等能力（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.FormExtensionAbility.d.ts，FormExtensionAbility.onAddForm）
- module.json5 的 extensionAbilities 里 "type": "form"，metadata 键名固定为 "ohos.extension.form"，resource 指向 $profile:form_config：卡片入口的声明方式（出处：arkts-ui-widget-configuration.md，FormExtensionAbility配置）
来源：1 张卡，1 个应用
- case-dc1f3f5507c9cd8ad208（omni-notes-hmos）：做法第 1 步 ← 建议 2
