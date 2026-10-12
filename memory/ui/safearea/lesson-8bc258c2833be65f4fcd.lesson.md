# 源端只在三键导航时给导航栏着色：以 TYPE_SYSTEM 底部避让高度判定导航方式，非手势时用 navigationBarColor 着色并随避让区变化更新

ID：`lesson-8bc258c2833be65f4fcd` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与入口窗口实现阶段，把源 Activity 按导航方式设置导航栏颜色的分支映射到目标窗口系统栏属性时

## 适用情境

源端在 Activity 中按是否手势导航决定导航栏底色（如非手势导航时 setNavigationBarColor(背景色带透明度)），判定依赖隐藏系统资源（config_navBarInteractionMode）或系统设置；目标为全屏沉浸窗口，入口用 getWindowAvoidArea 测避让区、用 setWindowSystemBarProperties 设置系统栏。

## 原因

源端判定导航方式的手段在目标没有同名对应，但被判定的状态可以观察：三键导航栏表现为 TYPE_SYSTEM 的底部避让区，手势导航时该高度为 0。把“检测手段无对等”当成“行为无对等”，会删掉着色分支，三键模式下导航栏恒透明。

## 做法

1. 规格先写出用户可观察的条件与效果（如“三键导航栏存在时导航栏涂背景色并带源端透明度”），再映射目标信号；检测 API 不同不构成删除该行为的理由。
2. 入口按 getWindowAvoidArea(TYPE_SYSTEM).bottomRect.height > 0 判定三键导航：此时用 setWindowSystemBarProperties({ navigationBarColor }) 写源端颜色（透明度并入 #AARRGGBB），手势导航保持透明；订阅 avoidAreaChange 在导航方式切换时重算，颜色取自主题背景时按当前深浅色取值。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:1
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
