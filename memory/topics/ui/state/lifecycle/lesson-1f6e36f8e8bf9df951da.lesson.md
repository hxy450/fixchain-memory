# 翻译“离开组合即销毁”的状态复位时，同时列出目标框架会替用户恢复的界面状态

ID：`lesson-1f6e36f8e8bf9df951da` · 版本：2 · 阶段：spec · 主题：[ui/state/lifecycle](index.md)

概要：翻译 remember 复位语义时列出框架会恢复的界面态

信号：`rememberSaveable`, `pushPath`, `NavBar`, `Tabs`, `Stack`

## 何时使用

规格提取阶段，把源端 remember（非 rememberSaveable）随组合销毁的状态语义翻译成目标端复位方案时

## 适用情境

源页面离开组合时丢弃全部状态，其中 focused 等由框架事件驱动的字段直接决定显示分支；目标端该页面常驻在 Navigation 的 NavBar（或 Stack、Tabs 保活）中，经 pushPath 进入子页后再系统返回。

## 原因

只把数据字段重置成新对象不够：来源 dump 显示，子页返回后 ArkUI 把焦点交还 NavBar 上次获焦的输入框，焦点回调随之把刚复位的状态改回去。规格只写了数据复位、验收只留界面判定时，生成期没有人做往返验证。

## 做法

1. 除数据字段外，逐项列出目标框架会替用户恢复的界面状态（焦点、输入法、滚动位置、选区），为每项写明 ArkUI 侧的复位或判别手段。
2. 由框架事件驱动的业务字段（如 focused），把“返回后为初始值”写成可核对的验收步骤：一次 push → 系统返回后 dump 对应组件状态。

## 可选检查

- 有设备时，一次 push → 系统返回后确认输入框未聚焦、没有键盘，显示初始分支。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [TextInput 获焦回调先判是否用户触摸再写业务状态](lesson-4c476a62732697c56c22.lesson.md)（共享 1 张卡）
- [点击无响应先设备复现定位，未上机结论标未验证](../../../process/unverified-as-fact/lesson-afae8d13e00941efe808.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c6aa20bd8974dabefc7b](../../../../../store/cases/case-c6aa20bd8974dabefc7b/dfe06c6f03bd3718e8173a201b5078d321b3cf56a6df1b995d0f2b9e07b642a4.json) · 结论：diagnosis, rec-977d10b6cb
  卡片版本：`dfe06c6f03bd3718e8173a201b5078d321b3cf56a6df1b995d0f2b9e07b642a4`
