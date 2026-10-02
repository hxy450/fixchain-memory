# 只经桌面快捷方式或通知点击进入的页面：module.json5 快捷方式声明、EntryAbility 的 Want 分支与目标页参数都要有确定写者

ID：`lesson-c46f182cf1d01a97e05f` · 版本：1

[本主题](index.md)

## 何时使用

规格拆分、切片实现与入口接线阶段，迁移源端只由外部 Intent（桌面快捷方式、本地通知点击）进入的页面时

## 适用情境

源端页面由静态或动态 shortcut、通知 PendingIntent 携带 extras（如 shortId、通知渠道）进入；目标规格把入口配置定为 module.json5 静态声明；页面与切片 worker 的写域不含 module.json5 和 EntryAbility。

## 原因

页面写者把“由 EntryAbility 解析 Want 后进入”写成既成事实注释，却没有登记入口接线；切片账本漏列规格里的入口验收项时，入口声明、EntryAbility 分支和路由器分支都没有写者，页面能编译却永远不可达。

## 做法

1. 在 module.json5 入口 Ability 的 metadata 加 { "name": "ohos.ability.shortcuts", "resource": "$profile:shortcuts_config" }，新建 resources/base/profile/shortcuts_config.json：每项写 shortcutId、label（$string 引用）、icon（$media 引用）与 wants（bundleName、moduleName、abilityName、parameters，parameters 的值为字符串）。
2. EntryAbility 的 onCreate/onNewWant 把 Want 交给路由器；路由器按 parameters 里的源端 extras 键识别快捷方式或通知入口，冷启暂存、热启直跳到目标页；目标页兼容路由器实际传入的参数形态（Map 或参数类）。
3. 无权写这些文件的任务，把入口声明、Want 分支、参数键与目标页参数形态作为跨切片草稿或带负责方的移交项交出；收尾验收沿“入口声明 → EntryAbility → 路由分支 → pushPathByName”逐段在代码中找到落点，排除注释命中。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c699af1f5c3b03105480](../../../store/cases/case-c699af1f5c3b03105480/8355cf8caf643dadffaa83c57e0c287cde3f437615e65ffceb2d2205f23bf324.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`8355cf8caf643dadffaa83c57e0c287cde3f437615e65ffceb2d2205f23bf324`
