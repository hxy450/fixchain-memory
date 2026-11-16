# 桌面快捷方式配置和图标

agent 会看到什么：源端有 App Shortcuts（shortcuts.xml、ShortcutManager / ShortcutInfo）或规格定了快捷方式入口；module.json5 的 ohos.ability.shortcuts metadata 缺失或放在 module 级，profile 下没有快捷方式配置，或图标是整张拉伸到 1024×1024

## 规矩

- rule-751bc619c874｜快捷方式入口裁定由 shortcuts 配置承担时，ability 的 metadata 引用快捷方式配置｜读到：规格或页面规格写明桌面快捷方式入口由鸿蒙侧 module.json5 shortcuts 配置承担；写错：module.json5 的 abilities 里没有 name 为 ohos.ability.shortcuts 的 metadata，resources/base/profile 下也没有对应的快捷方式配置文件
- rule-33a601cf185b｜ohos.ability.shortcuts 写进入口 UIAbility 的 metadata，不放 module 级｜读到：要把安卓长按应用图标的 App Shortcuts 迁成静态快捷方式，工程 module.json5 的 module 级已有 metadata 数组；写错：module.json5 里 {"name": "ohos.ability.shortcuts", "resource": "$profile:…"} 追加在 module 级 metadata 数组里，入口 UIAbility 的 abilities[].metadata 里没有它
- rule-bdb4474c5e86｜快捷方式图标在 1024×1024 透明画布里把图形缩放居中到约 450×450px，不整张拉伸｜读到：源端快捷方式图标只有 res/drawable-xxhdpi 下 72×72 的透明 PNG；写错：目标 shortcuts 的 icon 资源是把整张源图直接放大到 1024×1024（如 PIL 的 `resize((1024, 1024))`），图形随画布同比放大、占满画布，没收进 450×450px 显示区
- rule-5da26c03e43a｜静态快捷方式写进 UIAbility 的 metadata 加 profile，不写 module 级字段｜读到：源端有 android.app.shortcuts 静态快捷方式（res/xml 下带 android:shortcutId 的 <shortcut>）；写错：module.json5 里与 abilities 平级写了 "shortcuts": [...]，编译报 schema validate failed，propertyName 'shortcuts'
