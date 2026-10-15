# 源端按 getLastNonConfigurationInstance 是否为空决定是否读启动参数时，目标按“是否配置变化重建”区分

ID：`lesson-ed571550c44efdeb321e` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与页面实现阶段，翻译源 Activity.onCreate 中“取回保留实例为空才读启动参数”的建局或建状态逻辑时

## 适用情境

源 Activity 未声明 configChanges，用 onRetain(Custom)NonConfigurationInstance 与 getLast(Custom)NonConfigurationInstance 跨配置变化保留对象，该对象可能同时是静态单例（只在退出时 destroy）；目标页面不因配置变化重建，单例跨页面常驻，同一页面有多个入口模式（如新开与续局）。

## 原因

该方法只在配置变化重建时返回非空，正常启动恒为 null；译成“单例已存在”后，只要单例还在，任何进入都复用旧对象、忽略入口参数，新开变成续旧。

## 做法

1. 规格把这段逻辑写成两种进入方式：配置变化重建时取回当前对象并忽略参数；正常进入按入口参数分支（新开 → 新实例并设参数，续局 → 取现有实例）。目标用“本次是否由配置变化重建”（如 onConfigurationUpdate 路径传入的标志）区分，不用 hasInstance 或全局状态是否存在。
2. 写“某实例优先、忽略参数”这类验收前，把入口 × 前置状态（无旧对象、旧对象未结束、旧对象已结束）与旋转重建逐一代入源条件和目标条件；任何组合结果不一致就按源语义实现，并标注与规格的差异。

## 可选检查

- 已有暂停的旧局时选新开局并设起始等级：得到空局面与所设等级；旋转后保留当前局。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6e71bead39034fb1d84f](../../../store/cases/case-6e71bead39034fb1d84f/c8b4957e633b96abdda726cad3c1317747814e18b8e7fc6902c32e7c34d368d9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c8b4957e633b96abdda726cad3c1317747814e18b8e7fc6902c32e7c34d368d9`
