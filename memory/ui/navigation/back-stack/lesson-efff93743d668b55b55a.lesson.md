# 唯一页面压在空 Navigation 首页之上时，栈底 NavDestination 在自身 onBackPressed 按栈深接管返回，不写在 @Entry

ID：`lesson-efff93743d668b55b55a` · 版本：6

[本主题](index.md)

## 何时使用

入口装配与页面转换阶段，搭建 Navigation 入口壳，为冷启首页、首启引导页、清栈回根后的页等可能成为栈底的 NavDestination 接返回时；规格提取阶段写栈底返回的验收锚点时

## 适用情境

源端根页（启动 Activity 或 NavHost 起始目的地）没有覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理；目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push（首屏放根内容还是压栈见 lesson-8953e390416a80d7dd8c）。

## 例外与边界

- 首屏不必是 NavDestination、作为 Navigation 根内容常驻不压栈时，空栈返回按系统默认处理，不套本条
- 源端根页有自己的返回处理时按源端逻辑实现

## 原因

“空栈时返回退出应用”只对 Navigation 首页成立；唯一页面被压栈后栈深为 1，ArkUI 默认会把它弹出，露出空白首页，应用仍在前台。栈内有 NavDestination 时返回先交栈顶 NavDestination，返回 false 即出栈，@Entry 页的 onBackPress 不会被调用，兜底写在 @Entry 页等于没写。

## 做法

1. 在每个可能成为栈底的 NavDestination（或它们共用的返回裁决函数）的 .onBackPressed 中判断：navPathStack.size() <= 1 时取 UIAbilityContext 调用 moveAbilityToBackground() 并 return true，消费返回、不出栈；不用 terminateSelf（会结束进程，丢失源端保留的静态单例）。栈深大于 1 时不拦截；页面上的对话框或抽屉打开时先由它们消费返回。
2. 源端默认返回在参照系统上是 finish 时，同一处理里一并执行源 onDestroy 的释放并复位页面实例态；是移到后台时只退后台、不复位。
3. 列出所有会把栈收成只剩根页的路径（冷启动首次 push、首启引导、深链清栈重建、删除或克隆后清栈回根），确认它们都由同一个栈底返回处理接管，不只覆盖冷启动。
4. 规格把栈底返回写成可验收项，锚点指向栈底页的 onBackPressed，不写“系统默认/默认退后台”；编排派工不把经验的通用结论写成“源 Activity 默认 = …”的源码事实。

## 可选检查

- 冷启动后按一次返回：应用退到桌面且进程保留；出现空白页或应用仍在前台，说明返回链路漏接。

来源支持：4 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-16af2a52e0c933739747](../../../../store/cases/case-16af2a52e0c933739747/546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901`
- [case-4da27202d292222a1bb5](../../../../store/cases/case-4da27202d292222a1bb5/c147289e2865814063a2dbff9ccade7f64d416b446b115f1f4bf4ed793571f68.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`c147289e2865814063a2dbff9ccade7f64d416b446b115f1f4bf4ed793571f68`
- [case-65b537ef55556598f2ee](../../../../store/cases/case-65b537ef55556598f2ee/b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7.json) · 结论：recommendation:2, recommendation:3
  卡片版本：`b79edd83d22fd2ddea6ed7662cea1f10af19efc82bfb838db0fb9cf09d0ce6e7`
- [case-e8db862eb02b52da96d0](../../../../store/cases/case-e8db862eb02b52da96d0/3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b`
