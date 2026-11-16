# 桌面小组件被排除或延后时，module.json5 的扩展入口处留待决策占位

审的是：资源
触发（任一种）：
- 读到：源端 `AndroidManifest.xml` 有监听 `android.appwidget.action.APPWIDGET_UPDATE` 的 `AppWidgetProvider` 接收器，决策台账或计划把它排除或延后；写错的样子：`module.json5` 的 `extensionAbilities` 里没有 `"type": "form"` 的条目，也没有「待决策」占位
适用范围：按政策排除或延后桌面小组件时，目标工程 module.json5 和卡片配置这些入口清单
做法：
- 在 module.json5 的 extensionAbilities 处（以及卡片配置 form_config.json 的位置）留「待决策」占位，写明对应的决策条目，便于返修时直接按规格补上 type 为 form 的扩展入口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- "type": "form"，metadata: [{ "name": "ohos.extension.form", "resource": "$profile:form_config" }]：恢复时要补的卡片扩展入口；form_config.json 放在 resources/base/profile/（出处：arkts-ui-widget-configuration.md，FormExtensionAbility配置）
- 返修时新增两个 type=form 的 extensionAbilities 和 form_config.json，对应源端小组件的尺寸和更新周期声明：整簇恢复的落点（出处：卡里修好并验证过）
未核实：占位的写法卡里没有验证，出自建议
来源：1 张卡，1 个应用
- case-dc1f3f5507c9cd8ad208（omni-notes-hmos）：做法第 1 步 ← 建议 3；取值 2 ← 诊断
