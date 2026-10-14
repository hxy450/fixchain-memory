# 唯一页面被压在空的 Navigation 首页之上时由根页接管返回键：栈底返回用 moveAbilityToBackground 退后台、不出栈露出空白首页；源端未覆写返回时按 Activity finish() 同时执行 onDestroy 的释放并复位页面实例态，参照设备实测为 HOT 恢复时才保留实例

ID：`lesson-efff93743d668b55b55a` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与入口装配阶段，为单 Activity 应用确定根页面的返回语义、搭建 Navigation 入口壳并决定首页放在 Navigation 内容区还是首次 push 时；把注入经验转成派工要求、确定栈底返回的生命周期效果时

## 适用情境

安卓启动 Activity 未覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理（含 Compose NavHost 的起始目的地），返回键走 Activity 默认行为：默认 finish()，onDestroy 执行（如释放音乐、关闭数据源），实例态（输入框文字、所选值、播放位置）丢失，进程与静态单例保留；部分 Android 12+ 设备与启动方式下任务根 Activity 改为移到后台、onPause 存档、onResume 读档，以参照设备实测为准。目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push。

## 原因

“空栈时返回退出应用”只对 Navigation 首页成立；唯一页面被压栈后栈深为 1，返回会把它弹出，露出空白首页，应用仍在前台。来源中转换者已推出“返回 = 退出应用”，却误判了栈深，后续切片也没有接返回处理。把“Activity 默认返回”一律当成退后台，会漏掉 finish() 的释放与复位：再次进入仍保留输入框文字、所选值与音乐播放位置；改用 terminateSelf 又会结束鸿蒙进程、丢失源端保留的静态局面。另一应用中注入的一行提醒“源端无返回处理就按 Activity 默认退到后台”被编排者写进派工当作源码事实，参照设备（以 am start 启动的 SDK 37 模拟器）实测却是 finish。

## 做法

1. 在根 NavDestination 的 .onBackPressed 中按栈深判断：navPathStack.size() <= 1 时取 UIAbilityContext 调用 moveAbilityToBackground() 并 return true，消费返回、不出栈（不用 terminateSelf，以保留进程与静态单例）；源端未覆写返回时同时执行源 onDestroy 的释放并把页面实例态复位到 onCreate 初值，下次 onShown 重走 onCreate 的初始化，只有参照设备实测返回后再启动是 HOT 恢复原实例时才省略复位。栈深大于 1 时不拦截；页面上的对话框打开时先由对话框消费返回。
2. 源端有返回处理时按源端逻辑实现；首屏不必是 NavDestination 时，也可把它作为 Navigation 根内容常驻、不压栈，空栈返回按系统默认处理。
3. 列出所有会把栈收成只剩根页的路径（冷启动首次 push、深链清栈重建、删除或克隆后清栈回根），确认它们都由同一个根页返回处理接管，不只覆盖冷启动。
4. 规格提取时，源端根页没有返回处理、依赖 Activity 默认行为，也要在导航规格写出栈底返回的可验收项：列出 finish 的可观察效果（onPause、onStop、onDestroy 各做什么，哪些实例态回初值，哪些静态单例保留），无法确认参照行为时把“返回后再启动的页面状态”写成待核验收项；编排派工不把经验的通用结论写成“源 Activity 默认 = …”的源码事实。

## 可选检查

- 冷启动后按一次返回：应用退到桌面且进程与静态局面保留，再次进入时页面实例态与参照设备一致（finish 时回到初值）；出现空白页或应用仍在前台，说明返回链路漏接。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-16af2a52e0c933739747](../../../../store/cases/case-16af2a52e0c933739747/546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901`
- [case-65b537ef55556598f2ee](../../../../store/cases/case-65b537ef55556598f2ee/b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7`
- [case-e8db862eb02b52da96d0](../../../../store/cases/case-e8db862eb02b52da96d0/3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b`
