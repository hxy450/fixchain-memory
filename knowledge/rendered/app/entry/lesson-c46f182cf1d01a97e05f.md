# 只经桌面快捷方式或通知点击进入的页面：module.json5 快捷方式声明、EntryAbility 的 Want 分支与目标页参数都要有确定写者

## 何时使用

规格拆分、切片实现与入口接线阶段，迁移源端只由外部 Intent（桌面快捷方式、本地通知点击）进入的页面时

## 适用情境

源端页面由静态或动态 shortcut、通知 PendingIntent 携带 extras（如 shortId、通知渠道）进入；目标规格把入口配置定为 module.json5 静态声明；页面与切片 worker 的写域不含 module.json5 和 EntryAbility。EntryAbility 的 onCreate、onNewWant 对点桌面图标的普通启动和其他入口同样触发（某些系统场景下实例已存在时也会触发 onNewWant），加快捷方式、通知分支时只认带源端 extras 键的 Want；不带这些键的 Want 照原有启动流程（启动页分流、首页或留在当前页）走，已有的其他 Want 分支原样保留。

## 原因

页面写者把“由 EntryAbility 解析 Want 后进入”写成既成事实注释，却没有登记入口接线；切片账本漏列规格里的入口验收项时，入口声明、EntryAbility 分支和路由器分支都没有写者，页面能编译却永远不可达。

## 做法

1. 在 module.json5 入口 Ability 的 metadata 加 { "name": "ohos.ability.shortcuts", "resource": "$profile:shortcuts_config" }，新建 resources/base/profile/shortcuts_config.json：每项写 shortcutId、label（$string 引用）、icon（$media 引用）与 wants（bundleName、moduleName、abilityName、parameters，parameters 的值为字符串）。
2. EntryAbility 的 onCreate/onNewWant 把 Want 交给路由器；路由器按 parameters 里的源端 extras 键识别快捷方式或通知入口，冷启暂存、热启直跳到目标页；目标页兼容路由器实际传入的参数形态（Map 或参数类）。
3. 无权写这些文件的任务，把入口声明、Want 分支、参数键与目标页参数形态作为跨切片草稿或带负责方的移交项交出；收尾验收沿“入口声明 → EntryAbility → 路由分支 → pushPathByName”逐段在代码中找到落点，排除注释命中。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕快捷方式要在 module.json5 abilities 里需要它的 UIAbility 下配置 metadata 才对该 UIAbility 生效；metadata 的 name 必须是 ohos.ability.shortcuts，resource 写资源索引（不超过 255 字节），如 $profile:shortcuts_config 指向 /resources/base/profile/shortcuts_config.json
- 〔做法第 1 步〕快捷方式的 shortcutId 取值为不超过 63 字节的字符串，不支持用 $string 资源索引配置，不可缺省；wants 可缺省，缺省为空
- 〔做法第 1、2 步〕快捷方式 wants 里的 parameters 是拉起快捷方式时带的自定义数据，只支持字符串类型的值，键和值都最长 1024 个字符；bundleName、moduleName、abilityName 分别是目标包名、模块名、组件名
- 〔做法第 2 步〕UIAbility 冷启动时系统依次触发 onCreate、onWindowStageCreate、onForeground，入口 want 在 onCreate 里拿到；UIAbility 实例已创建、再次被启动时不再走 onCreate，而是依次触发 onNewWant、onForeground，新的 want 在 onNewWant 里拿到
