# 静态快捷方式写进 UIAbility 的 metadata 加 profile，不写 module 级字段

审的是：资源
触发（任一种）：
- 读到：源端有 android.app.shortcuts 静态快捷方式（res/xml 下带 android:shortcutId 的 <shortcut>）；写错的样子：module.json5 里与 abilities 平级写了 "shortcuts": [...]，编译报 schema validate failed，propertyName 'shortcuts'
- 写错的样子：编译门为过 schema 把 module.json5 里整块 shortcuts 删掉，在迁移报告里记 GAP
适用范围：把安卓静态快捷方式迁到 HarmonyOS 工程配置，以及编译门处理 module.json5 的 schema 报错时
做法：
- 在 resources/base/profile/ 下建 shortcuts_config.json，结构是 shortcuts 数组（shortcutId、label、icon、wants）；源端 shortcutId → shortcutId，shortcutShortLabel → label，icon → icon，intent 的目标和 extra → wants 的 abilityName 和 parameters
- 在 module.json5 对应 UIAbility 的 metadata 里加 {"name": "ohos.ability.shortcuts", "resource": "$profile:shortcuts_config"}
- 写入前按当前 SDK 的 schema 核对字段；编译门遇到不允许的字段，先查功能的新承载位置再改，不删块记 GAP
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- "metadata": [{ "name": "ohos.ability.shortcuts", "resource": "$profile:shortcuts_config" }]：写在需要快捷方式的 UIAbility 的 abilities 条目里（出处：module-configuration-file.md，shortcuts标签）
- shortcuts 是数组，子标签 shortcutId、label、icon、wants（API 20 起另有 visible）：shortcuts_config.json 的结构，放在 resources/base/profile/ 下（出处：module-configuration-file.md，shortcuts标签）
- shortcutId 不超过 63 字节，不支持用 $string 资源索引：源端 android:shortcutId 原样写字符串（出处：module-configuration-file.md，shortcuts标签）
- startShortcut 拉起 wants 里的第一个目标组件，推荐只配一个 wants 元素：源端 <intent> 对应一个 wants 元素（出处：module-configuration-file.md，shortcuts标签）
- Shortcut：shortcutId（string）、enabled、icon、shortcutShortLabel、shortcutLongLabel、shortcutDisabledMessage：源端静态快捷方式 XML 上可写的属性（出处：Android SDK 平台资源 data/res/values/attrs.xml，Shortcut（按应用的 compileSdk 取对应平台））
- abilities[0].metadata 加 ohos.ability.shortcuts → $profile:shortcuts_config 后两条静态快捷方式恢复：修好的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7f8dcb2d9341693d1225（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3；取值 6 ← 诊断
