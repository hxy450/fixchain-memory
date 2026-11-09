# 源端按导航方式着色时保留条件与可见目标：先核目标系统栏颜色能力，再选择实现或登记平台差异

ID：`lesson-8bc258c2833be65f4fcd` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与入口窗口实现阶段，把源 Activity 按导航方式设置导航栏颜色的分支映射到目标窗口系统栏属性时

## 适用情境

源端在 Activity 中按是否手势导航决定导航栏底色（如非手势导航时 setNavigationBarColor(背景色带透明度)），判定依赖隐藏系统资源（config_navBarInteractionMode）或系统设置；目标为全屏沉浸窗口，入口用 getWindowAvoidArea 测避让区、用 setWindowSystemBarProperties 设置系统栏。

## 原因

源端判定导航方式的手段在目标没有同名对应，但被判定的状态可以观察：三键导航栏表现为 TYPE_SYSTEM 的底部避让区，手势导航时该高度为 0。检测手段不同不自动意味着行为可删除；但检测到三键导航也不证明目标着色 API 可用，颜色设置须另核版本与设备能力。

## 做法

1. 规格先写出用户可观察的条件与效果（如“三键导航栏存在时导航栏涂背景色并带源端透明度”），再映射目标信号；检测 API 不同不构成删除该行为的理由。
2. 先在目标设备验证 TYPE_SYSTEM.bottomRect.height 与导航模式的对应，再核着色能力。本轮官方 SystemBarProperties.navigationBarColor 明示 HarmonyOS 各设备不支持该能力，不能把字段赋值算着色成功；仅在目标版本有可用实现证据时采用，否则登记具体平台差异并核其他受支持方案。导航/主题变化时更新条件与可见结果，保持源端透明度语义。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:1
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
