# 源端以杀进程实现“重启应用”时用 ApplicationContext.restartApp，不译成 terminateSelf 退出

ID：`lesson-73618bb856a8a7dfe7fc` · 版本：3 · 阶段：spec/execute · 主题：[app/recreation](index.md)

概要：杀进程意在重启用 restartApp 不用退出

信号：`System.exit`, `Runtime.exit`, `Process.killProcess`, `ApplicationContext.restartApp`, `terminateSelf`, `16000053`, `16000064`, `windowStageEvent`, `savedInstanceState`

## 何时使用

规格提取与实现阶段，迁移 System.exit(0)、Runtime.exit、Process.killProcess 等进程退出调用时

## 适用情境

源方法注释或调用点表明意图是重启（如通知点击的重启动作、切换语言、恢复或重置数据之后调用）；Android 前台进程被杀后，系统按残留任务栈与 savedInstanceState 重建 Activity；目标准备写 context.terminateSelf()。

## 例外与边界

- 调用点只在用户主动退出或致命错误时结束进程，源端也不期待重新进入；此时按退出处理

## 原因

前台进程被杀后 Android 按任务栈重新拉起界面，用户看到的是重启；terminateSelf 只结束当前 Ability，语言切换、数据恢复后的界面不会重新加载，也与“重启后进入主页”一类验收矛盾。

## 做法

1. 先 grep 该方法的全部调用方并读方法注释，确认期望终态；多个规格对同一方法口径不一时，以描述用户可见终态的验收（重启进入主页、界面状态保留）为准修正服务层契约。
2. 重启用 ApplicationContext.restartApp(want) 拉起入口 UIAbility；该接口只能在主线程、应用处于获焦状态时调用（不在顶层报 16000053，3 秒内重复调用它或 UIAbilityContext.restartApp 报 16000064，见 SDK application/ApplicationContext.d.ts，API 12 起；HarmonyOS 文档 js-apis-inner-application-applicationcontext，访问于 2026-10-17）；重启不触发 Ability 的 onDestroy，依赖 onDestroy 落盘的数据在调用前保存；后台触发时推迟到窗口重新激活（windowStageEvent ACTIVE）再调用，失败时以 terminateSelf 兜底。
3. 源端依赖系统重建保留的界面状态（抽屉开合、列表位置、搜索条件）经 Want 参数带到新进程并在入口恢复；重启后的冷启动入口仍经过源端的验密等前置门。
4. 实现者读到源注释与规格契约相反时，登记差异并回报，不沉默沿用规格。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [隐式 Want 先 canOpenLink 预检，不靠抛错](../capability/launch/lesson-948d876672049969b865.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）
- [后台拷贝用异步 IO 或 taskpool，不包 *Sync](../../arkts/async-mapping/lesson-c54d1c8af2177b819837.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-29db923e9cadbe8ce53c](../../../../store/cases/case-29db923e9cadbe8ce53c/aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761.json) · 结论：diagnosis
  卡片版本：`aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761`
- [case-f85c825bb16d5a79901c](../../../../store/cases/case-f85c825bb16d5a79901c/3b1b9007616b4e373f4e7b0c5200cd412af7e5a4336c4ddc52d6a4b465a5b552.json) · 结论：diagnosis, rec-5135cf0fef, rec-5aab75d6a4, rec-5bf750b34c
  卡片版本：`3b1b9007616b4e373f4e7b0c5200cd412af7e5a4336c4ddc52d6a4b465a5b552`
