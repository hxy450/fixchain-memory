# Android Activity 级 NFC 前台派发迁移时，按 UIAbility 前后台注册，再用可见顶页登记表仿真页面级开关与默认新标签处理

ID：`lesson-a4ee90eabe3eef99ddbe` · 版本：2

[本主题](index.md)

## 何时使用

NFC 引擎与基类行为迁移阶段，把基类 onResume/onPause 的前台派发开关、onNewIntent 统一处理与“当前标签”判定分配给服务、页面与全局状态时

## 适用情境

Android 多数页面继承基类：onResume 设置待处理组件并 enableForegroundDispatch，onPause 关闭，onNewIntent 统一处理新标签，卡或设备不支持时跳转信息页；全局保存任意技术的 Tag。目标 tag.registerForegroundDispatch 按 UIAbility 注册，页面用 Navigation/NavDestination 组织，服务切片不能改页面。

## 例外与边界

- 处理的是清单声明的贴卡拉起入口（intent-filter 的 TECH_DISCOVERED/TAG_DISCOVERED，目标 skills 声明）：那条路径由系统拉起应用，不经前台派发，也不受页面可见性登记影响

## 原因

派发开关在 Android 随 Activity 可见性启停，在目标随 UIAbility 生效：让某一页的隐藏注销整个能力级派发，其他页就收不到卡；把订阅挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在收卡；把全局 Tag 收窄为某一技术类型，非该技术的卡被判为不在场。服务与页面各自认为接线归对方时，页面级开关与默认新标签处理都会无人实现。

## 做法

1. 在 EntryAbility 的 onForeground/onBackground 注册、注销能力级前台派发；服务维护可见页登记表（pageShown/pageHidden），把标签投递给最上层可见页，仿真 onPause → onNewIntent → onResume；各页在 NavDestination 的 onShown/onHidden 登记，不在 aboutToAppear/aboutToDisappear 订阅。
2. 不让单个页面的隐藏注销应用级派发，也不把“设置待处理页面”合并进通用注册函数；默认的新标签处理（不支持时跳信息页）放在服务提供的入口里。
3. 负责服务的任务不能改页面时，交付 pageShown/pageHidden 等页面可直接调用的入口，并按继承基类的页面清单逐页登记带负责方的接线移交。
4. 全局“当前标签”保存任意技术的标签信息，在场判定按它判断，不收窄为单一技术类型。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3735da03c6e544339df6](../../../store/cases/case-3735da03c6e544339df6/38c6e0dfc90fd2fe86eb204ba199a8fd1d8df2fc6b790f9073ac59a0c02a29f8.json) · 结论：diagnosis, recommendation:3, recommendation:1
  卡片版本：`38c6e0dfc90fd2fe86eb204ba199a8fd1d8df2fc6b790f9073ac59a0c02a29f8`
