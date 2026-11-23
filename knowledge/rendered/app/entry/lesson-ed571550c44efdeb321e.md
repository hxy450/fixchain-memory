# 源端“getLast(Custom)NonConfigurationInstance 为空才按启动参数建立状态”只在配置变化重建时取回实例：目标按“本次是否由配置变化重建”区分，正常进入一律按入口参数分支，不用单例是否存在代替

## 何时使用

规格提取与页面实现阶段，翻译源 Activity.onCreate 中“取回保留实例为空才读启动参数”的建局或建状态逻辑时

## 适用情境

源 Activity 未声明 configChanges，用 onRetain(Custom)NonConfigurationInstance 与 getLast(Custom)NonConfigurationInstance 跨配置变化保留对象，该对象可能同时是静态单例（只在退出时 destroy）；目标页面不因配置变化重建，单例跨页面常驻，同一页面有多个入口模式（如新开与续局）。

## 例外与边界

- 源 onCreate 另外还按 savedInstanceState（进程被回收后重建时非空）恢复状态的，那条路径上取回保留实例同样为空，但它不是“正常进入”：把它单独保留为恢复分支，不并进按入口参数新建的分支

## 原因

该方法只在配置变化重建时返回非空，正常启动恒为 null；译成“单例已存在”后，只要单例还在，任何进入都复用旧对象、忽略入口参数：新开局变成续旧局，已结束的局会再弹一次结算并重复记分。来源中规格作者读到了源码，仍写下“已有实例时 mode/level 全部忽略”的验收项，实现者只核对了续局入口就照写。

## 做法

1. 规格把这段逻辑写成两种进入方式：配置变化重建时取回当前对象并忽略参数；正常进入按入口参数分支（新开 → 新实例并设参数，续局 → 取现有实例）。目标用“本次是否由配置变化重建”（如 onConfigurationUpdate 路径传入的标志）区分，不用 hasInstance 或全局状态是否存在。
2. 写“某实例优先、忽略参数”这类验收前，把入口 × 前置状态（无旧对象、旧对象未结束、旧对象已结束）与旋转重建逐一代入源条件和目标条件；任何组合结果不一致就按源语义实现，并标注与规格的差异。

## 可选检查

- 已有暂停的旧局时选新开局并设起始等级：得到空局面与所设等级；旋转后保留当前局。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Activity#getLastNonConfigurationInstance 返回旧实例在 onRetainNonConfigurationInstance 里交出的对象，只在因配置变化重建出的新实例最初的 onCreate、onStart 里可取；不是配置变化重建（正常启动）时返回 null
- 〔原因〕Activity#onRetainNonConfigurationInstance 只在系统因配置变化销毁 Activity、且已知马上要为新配置建新实例时调用
- 〔适用情境〕清单里没写 android:configChanges 时，系统配置变化会重启 Activity；写进 configChanges 的变化不重启，改为调用 Activity.onConfigurationChanged
- 〔适用情境 / 做法第 1 步〕UIAbility 在环境变量（如语言、深浅色）变化时回调 onConfigurationUpdate，通过 Configuration 取最新值，页面不因此重建
