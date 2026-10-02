# 外部入口的宿主导航守卫按“目标已注册或路由命中”判断，不用导航栈成员检查

ID：`lesson-1b05b8d5cc528d5dc5bc` · 版本：1

[本主题](index.md)

## 何时使用

入口接线阶段，为推送、桌面快捷方式、通知点击等外部 Want 编写宿主导航执行器（路由器回调里的 pushPathByName）的可用性守卫时

## 适用情境

源端跳转前用 isIntentAvailable 一类判断目标是否可用；目标由单一 EntryAbility 加 Navigation pageMap 承载，外部 Want 冷启时暂存、热启时直跳，由宿主页 pushPathByName 入栈；守卫可能先写在跨切片草稿里，再被复制到闪屏页、主页等多个宿主。

## 原因

冷启首跳和热启直跳的目标本来就不在当前栈里；用 navPathStack.getAllPathName() 是否包含目标作守卫，会把所有外部入口目标静默拒绝，编译与结构检查都发现不了。草稿注释写“未注册页不分发”、表达式却检查栈成员时，偏差会随草稿复制到每个宿主。

## 做法

1. 守卫判断目标是否已注册或路由命中：查 pageMap/路由表的注册名集合，或路由解析未命中时得到的空页面名；不以栈成员判断可用性。
2. 写完按冷启（栈里只有闪屏）和热启（栈里只有主页）各推演一次外部入口首跳，确认目标能入栈；同一守卫被复制到多个宿主时逐处核对。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c699af1f5c3b03105480](../../../../store/cases/case-c699af1f5c3b03105480/8355cf8caf643dadffaa83c57e0c287cde3f437615e65ffceb2d2205f23bf324.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`8355cf8caf643dadffaa83c57e0c287cde3f437615e65ffceb2d2205f23bf324`
