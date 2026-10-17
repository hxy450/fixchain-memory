# Fragment 事务与 finish() 迁到 NavPathStack 时逐调用点按分支映射，不压成一次同步 pop/push

ID：`lesson-9a113ce21ae30365ea5b` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与页面实现阶段，把源 Activity/Fragment 的 replace、addToBackStack、popBackStack(Immediate) 与 finish() 调用翻译成 NavPathStack 操作时

## 适用情境

源端在宿主 Activity 里切换 Fragment：已有详情时 popBackStackImmediate 后 replace 一个新实例，列表 replace+addToBackStack；保存或返回时按偏好分支 popBackStack（异步，栈深满足条件才恢复标题栏）或 showToast 后 finish() 整个 Activity。目标是单 Navigation 栈，规格写成“switchToDetail → pushPathByName”一行，实现注释写“退化为 pop”“返回栈语义由 NavPathStack 天然保留”。

## 例外与边界

- 源端未覆写返回、靠 Activity 默认行为离开栈底页面时，按栈底返回的处理方式实现，不套用这里的 finish 映射

## 原因

Fragment 事务的每个分支有不同的实例与返回栈后果：replace 恒建新实例，popBackStack 在下一轮才执行且在根上无效，finish() 结束整个 Activity 而不只是出栈一页。压成一次同步 pop/push，会在同名页面仍在栈中时复用旧实例（新页初始化回调不触发），在外部入口场景退回列表而不是结束，或在根上弹出空白。

## 做法

1. 先把源端每个事务和退出调用点按分支列表：replace+addToBackStack、popBackStackImmediate+replace、popBackStack、finish()，连同触发条件（偏好、栈深判断）与前后副作用（Toast、标题栏恢复、发给宿主的事件），逐条写进规格验收。
2. 恒建新实例的跳转用 pushPath(info, { launchMode: LaunchMode.NEW_INSTANCE })；同帧先 pop 再按名压入同名页时，已观察到 ArkUI 复用栈中实例、新页 onReady 不触发。
3. popBackStack 映射为排到下一轮执行的出栈，栈只剩根页时为空操作；依赖出栈后栈深的副作用（恢复标题栏、通知宿主）在出栈完成后按实际栈深执行。
4. finish() 按它结束的承载映射：外部入口独占的 UIAbility 用 terminateSelf；源端先 Toast 再 finish 的，等 Toast 时长结束后再结束，期间屏蔽输入；不写成 pop。
5. 注释写“退化为 pop”“由 NavPathStack 天然保留”而没有实现对应分支时，登记为占位与缺口，不算等价实现。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-aebac48fa7acdb86e57e](../../../../store/cases/case-aebac48fa7acdb86e57e/aa4810e6d74ae53993bd6b3289dfc890990fa07c4f3c1423c4b210c6b25ef423.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`aa4810e6d74ae53993bd6b3289dfc890990fa07c4f3c1423c4b210c6b25ef423`
