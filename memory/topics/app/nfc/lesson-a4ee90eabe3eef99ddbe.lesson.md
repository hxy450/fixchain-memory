# Android Activity 级 NFC 前台派发迁到 HarmonyOS 时按 UIAbility 前后台注册，再用可见顶页登记表仿真页面级开关与默认新标签处理

ID：`lesson-a4ee90eabe3eef99ddbe` · 版本：2 · 阶段：execute · 主题：[app/nfc](index.md)

概要：NFC 前台派发按 Ability 注册，页面用可见页表

信号：`enableForegroundDispatch`, `onNewIntent`, `tag.registerForegroundDispatch`, `onForeground`, `onBackground`, `onShown`, `onHidden`, `aboutToAppear`, `NavDestination`, `pageShown`

## 何时使用

NFC 引擎与基类行为迁移阶段，把基类 onResume/onPause 的前台派发开关、onNewIntent 统一处理与“当前标签”判定分配给服务、页面与全局状态时

## 适用情境

Android 多数页面继承基类：onResume 设置待处理组件并 enableForegroundDispatch，onPause 关闭，onNewIntent 统一处理新标签，卡或设备不支持时跳转信息页；全局保存任意技术的 Tag。目标 tag.registerForegroundDispatch 按 UIAbility 注册，页面用 Navigation/NavDestination 组织，服务切片不能改页面。

## 原因

派发开关在 Android 随 Activity 可见性启停，在目标随 UIAbility 生效：让某一页的隐藏注销整个能力级派发，其他页就收不到卡；把订阅挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在收卡；把全局 Tag 收窄为某一技术类型，非该技术的卡被判为不在场。来源中服务切片只写了注册与注销并把页面接线推给消费切片，消费切片又推回，最终只有主菜单注册、且在其隐藏时注销全应用派发；三个页面把订阅挂在组件生命周期；全局 Tag 被定义为单一技术类型。

## 做法

1. 在 EntryAbility 的 onForeground/onBackground 注册、注销能力级前台派发；服务维护可见页登记表（pageShown/pageHidden），把标签投递给最上层可见页，仿真 onPause → onNewIntent → onResume；各页在 onShown/onHidden 登记，不在 aboutToAppear/aboutToDisappear 订阅。
2. 不让单个页面的隐藏注销应用级派发，也不把“设置待处理页面”合并进通用注册函数；默认的新标签处理（不支持时跳信息页）放在服务提供的入口里。
3. 全局“当前标签”保存任意技术的标签信息，在场判定按它判断，不收窄为单一技术类型。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [基类横切行为逐方法映射，按子类布局核守卫再接线](../cross-cutting/lesson-2fcb6612ee4106b34e17.lesson.md)（共享 1 张卡）
- [每次可见的重载迁 onShown 或订阅](../../ui/state/lifecycle/lesson-b3bb0bc33f4caded78a2.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3735da03c6e544339df6](../../../../store/cases/case-3735da03c6e544339df6/38c6e0dfc90fd2fe86eb204ba199a8fd1d8df2fc6b790f9073ac59a0c02a29f8.json) · 结论：diagnosis, rec-8242452488
  卡片版本：`38c6e0dfc90fd2fe86eb204ba199a8fd1d8df2fc6b790f9073ac59a0c02a29f8`
