# 源端在入口 onCreate 首帧前按偏好设主题时，目标在 EntryAbility.onCreate 同步读取偏好并在 loadContent 前 setColorMode；恢复函数返回 Promise 而调用方不等待，就是首帧后才生效

## 何时使用

入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时

## 适用情境

源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。

## 原因

不等待的异步恢复在 loadContent 之后才完成，首帧先按系统深浅色绘制再切换；接线者只看到“请在 onCreate 调用”，按原样补调用点不会发现时序问题。源端把主题放在 super.onCreate 之前正是为了首帧生效，这一时机若只留在设计参考里、没写进功能契约，下游就收不到。来源中偏好 worker 自己注意到 setColorMode 是进程态、需跨启动恢复，仍写成 async 恢复并交接，收口者不等待地调用。

## 做法

1. 在 EntryAbility.onCreate 的同步路径用 preferences.getPreferencesSync 读取主题键，并在 onWindowStageCreate 的 loadContent 之前完成 setColorMode。
2. 规格提取读入口 Activity.onCreate 时，把 super.onCreate/setContentView 之前的调用（如 setTheme）连同“首帧前生效”的时机写进功能契约，并指定目标承接位置。
3. 为启动恢复写移交时写明时序约束（如“首帧前同步生效”）；接线者看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只机械补调用点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕UIAbility.onCreate 是同步回调，系统不等待其中的异步操作：在 onCreate 里调用返回 Promise 的恢复函数而不等待，或把 onCreate 写成 async 再 await，onCreate 都会先返回，系统接着执行 onWindowStageCreate 和其中的 loadContent，恢复逻辑可能晚于首帧才完成。〔成立范围：对象：Stage 模型的 UIAbility.onCreate、AbilityStage.onCreate（声明返回 void，注释写明同步返回、不支持异步回调）。对照：UIAbility.onDestroy 声明为 void | Promise<void>，注释说明可借返回的 Promise 让后续生命周期等它完成。依据是 SDK 声明注释，实现里看不到。最常见的不成立情形：恢复函数内部读偏好全用同步接口（getPreferencesSync、getSync），读取在 onCreate 返回前完成。本条只说读取的先后；setColorMode 在 loadContent 之前调用时首帧是否已按目标深浅色绘制，SDK 声明没写、API 参考与适配指南说法不一，本条不作依据。〕
- 〔做法第 1 步〕深浅色生效优先级为 UIAbility 级（UIAbilityContext.setColorMode）> 应用级（ApplicationContext.setColorMode）> 系统；应用没设时为默认的 COLOR_MODE_NOT_SET、跟随系统，设成深色或浅色后深浅色固定、不随系统变化，onConfigurationUpdate 等订阅也收不到系统深浅色的变化。〔成立范围：对象：ApplicationContext.setColorMode 与 UIAbilityContext.setColorMode，只能在主线程调用。例外：应用从未调用 setColorMode 且工程 dark 目录下没有任何深色资源时，系统组件在系统深色模式下仍保持浅色，文档建议显式设为 COLOR_MODE_NOT_SET 才让它们跟随系统。依据是文档说明。最常见的不成立情形：工程里某个 UIAbility 自己调过 UIAbilityContext.setColorMode，应用级设置对这个 UIAbility 不起作用。〕
- 〔适用情境〕用户首选项默认的 XML 存储模式下，put / putSync 只改内存中的 Preferences 实例，调用 flush / flushSync 后才写入持久化文件；设置页只 put 不 flush 时，进程被杀后冷启动同步读到的仍是旧值。〔成立范围：对象：@ohos.data.preferences 的 Preferences 实例。条件：同一进程内实例常驻内存，未 flush 也能读到新值。例外：API 18 起可选的 GSKV 存储模式写入实时落盘，无需 flush。依据是 SDK 声明注释和文档说明。最常见的不成立情形：创建实例时选了 GSKV 存储模式。〕
- 〔做法第 2 步〕安卓 Context.setTheme 的注释要求在该 Context 实例化任何视图之前调用（例如 Activity.setContentView 或 LayoutInflater.inflate 之前）。〔成立范围：对象：Activity 等 Context 的 setTheme。依据是 SDK 源码注释。最常见的不成立情形：源端不调用 setTheme，而是在 Manifest 的 android:theme 里静态指定主题，这时没有调用时机问题。〕
