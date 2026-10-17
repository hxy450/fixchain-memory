# 源端“getLast(Custom)NonConfigurationInstance 为空才按启动参数建立状态”只在配置变化重建时取回实例：目标按“本次是否由配置变化重建”区分，正常进入一律按入口参数分支，不用单例是否存在代替

ID：`lesson-ed571550c44efdeb321e` · 版本：2 · 阶段：spec/execute · 主题：[app/recreation](index.md)

概要：保留实例按是否配置重建区分，不以单例存在代替

信号：`NonConfigurationInstance`, `onConfigurationUpdate`, `hasInstance`, `configChanges`

## 何时使用

规格提取与页面实现阶段，翻译源 Activity.onCreate 中“取回保留实例为空才读启动参数”的建局或建状态逻辑时

## 适用情境

源 Activity 未声明 configChanges，用 onRetain(Custom)NonConfigurationInstance 与 getLast(Custom)NonConfigurationInstance 跨配置变化保留对象，该对象可能同时是静态单例（只在退出时 destroy）；目标页面不因配置变化重建，单例跨页面常驻，同一页面有多个入口模式（如新开与续局）。

## 原因

该方法只在配置变化重建时返回非空，正常启动恒为 null；译成“单例已存在”后，只要单例还在，任何进入都复用旧对象、忽略入口参数：新开局变成续旧局，已结束的局会再弹一次结算并重复记分。来源中规格作者读到了源码，仍写下“已有实例时 mode/level 全部忽略”的验收项，实现者只核对了续局入口就照写。

## 做法

1. 规格把这段逻辑写成两种进入方式：配置变化重建时取回当前对象并忽略参数；正常进入按入口参数分支（新开 → 新实例并设参数，续局 → 取现有实例）。目标用“本次是否由配置变化重建”（如 onConfigurationUpdate 路径传入的标志）区分，不用 hasInstance 或全局状态是否存在。
2. 写“某实例优先、忽略参数”这类验收前，把入口 × 前置状态（无旧对象、旧对象未结束、旧对象已结束）与旋转重建逐一代入源条件和目标条件；任何组合结果不一致就按源语义实现，并标注与规格的差异。

## 可选检查

- 已有暂停的旧局时选新开局并设起始等级：得到空局面与所设等级；旋转后保留当前局。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6e71bead39034fb1d84f](../../../../store/cases/case-6e71bead39034fb1d84f/c8b4957e633b96abdda726cad3c1317747814e18b8e7fc6902c32e7c34d368d9.json) · 结论：diagnosis, rec-ed1cea286e, rec-bcbde3a738, rec-b2b819440c
  卡片版本：`c8b4957e633b96abdda726cad3c1317747814e18b8e7fc6902c32e7c34d368d9`
