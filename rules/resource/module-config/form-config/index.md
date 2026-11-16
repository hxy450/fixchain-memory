# appwidget-provider 转成的 form_config.json

agent 会看到什么：源端 appwidget-provider 的 targetCellWidth / targetCellHeight、min/maxResizeWidth、resizeMode、updatePeriodMillis，目标 form_config.json 里写的 supportDimensions、defaultDimension、resizable 和刷新配置

## 规矩

- rule-143e5f19b713｜appwidget-provider 转 form_config 时，按格数和拉伸范围写规格、resizable 和刷新｜读到：appwidget-provider 的 android:targetCellWidth / android:targetCellHeight、android:minResizeWidth / android:maxResizeWidth、android:resizeMode，没有 android:updatePeriodMillis；写错：form_config.json 的 supportDimensions / defaultDimension 和源格数不符，缺 "resizable"，或源无刷新周期却写了 "updateEnabled": true 和 updateDuration / scheduledUpdateTime
- rule-fdc8d4374e05｜桌面小组件被排除或延后时，module.json5 的扩展入口处留待决策占位｜读到：源端 `AndroidManifest.xml` 有监听 `android.appwidget.action.APPWIDGET_UPDATE` 的 `AppWidgetProvider` 接收器，决策台账或计划把它排除或延后；写错：`module.json5` 的 `extensionAbilities` 里没有 `"type": "form"` 的条目，也没有「待决策」占位
