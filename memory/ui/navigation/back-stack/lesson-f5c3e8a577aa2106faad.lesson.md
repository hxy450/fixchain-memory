# 源根 Activity 未覆写返回时，按系统版本与 LAUNCHER 声明判定默认返回是 finish 还是移到后台，再复现对应生命周期

ID：`lesson-f5c3e8a577aa2106faad` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与页面实现阶段，为源端没有返回处理的根 Activity 写返回契约、实现目标栈底返回的生命周期效果时；编排派工转述“源端默认返回”时

## 适用情境

源端任务根 Activity 没有覆写 onBackPressed、onKeyDown，也没有注册 OnBackPressedCallback，返回走 Activity 默认行为；它的 onDestroy 有释放逻辑（音乐 release、数据源 close），页面持有实例态（输入框文字、所选值、播放位置），另有跨 Activity 保留的静态单例。

## 例外与边界

- 源端有返回处理（覆写 onBackPressed、OnBackPressedCallback、BackHandler）时按源端逻辑实现，不套默认规则

## 原因

Activity.onBackPressed 的默认实现随平台版本变化（本机 sources/android-36.1/android/app/Activity.java 注释）：API 31（Android 12）以前 finish；API 31 起，任务根且清单声明 ACTION_MAIN 与 CATEGORY_LAUNCHER 的 Activity 连同任务移到后台，其余 Activity 仍 finish。finish 执行 onDestroy、实例态丢失、再次启动走 onCreate；移到后台不走 onDestroy、实例态保留。一律当成退后台会漏掉释放与复位，一律当成 finish 又会多做复位。

## 做法

1. 按参照系统的 API 级别、源 Activity 是否为任务根、清单是否声明 MAIN/LAUNCHER 写出预期：API ≥ 31 且三者都成立为移到后台，其余为 finish；参照设备实测与此不符时（判定在系统服务端，启动方式也可能影响），注明设备系统版本与启动方式后以实测为准。
2. 规格列出该分支的可观察效果：finish 时 onPause、onStop、onDestroy 各做什么，哪些实例态回到 onCreate 初值、哪些静态单例保留；移到后台时写 onPause/onStop 的存档与保留的实例态。
3. 目标栈底返回统一用 moveAbilityToBackground() 保住进程与静态单例；finish 分支同时执行源 onDestroy 的释放并把页面实例态复位，下次 onShown 重走 onCreate 的初始化（如背景音乐从头播放、刷新列表）；移到后台分支只退后台、不复位。onDestroy 的映射不只挂在 aboutToDisappear 上，退后台时它不会触发。
4. 编排派工转述时附上源码依据（是否覆写返回、onDestroy 做了什么、清单 LAUNCHER 声明），不把经验的通用结论写成源码事实。

## 可选检查

- 有设备时冷启动后按一次返回再启动：finish 分支页面实例态回到初值、静态局面保留；移到后台分支页面原样恢复。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-65b537ef55556598f2ee](../../../../store/cases/case-65b537ef55556598f2ee/b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7`
- [case-e8db862eb02b52da96d0](../../../../store/cases/case-e8db862eb02b52da96d0/3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b.json) · 结论：diagnosis, recommendation:2
  卡片版本：`3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b`
