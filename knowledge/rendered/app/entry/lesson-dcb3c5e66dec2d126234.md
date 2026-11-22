# 源端在入口 onCreate 首帧前按偏好设主题时，目标在 EntryAbility.onCreate 同步读取偏好并在 loadContent 前 setColorMode；恢复函数返回 Promise 而调用方不等待，就是首帧后才生效

## 何时使用

入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时

## 适用情境

源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。

## 例外与边界

- 源端存的是 AppCompatDelegate 的夜间模式整数时按含义对应、不照搬数值：MODE_NIGHT_YES（2）→ COLOR_MODE_DARK（0），MODE_NIGHT_NO（1）→ COLOR_MODE_LIGHT（1），MODE_NIGHT_FOLLOW_SYSTEM（-1）→ COLOR_MODE_NOT_SET（-1，跟随系统）；「跟随系统」不写成浅色
- setColorMode 只承接深浅色；源端按偏好切换的是主题色、字号等其他 style 时，首帧前生效的要求照样成立，但目标的承接方式另定，不套用 setColorMode

## 原因

不等待的异步恢复在 loadContent 之后才完成，首帧先按系统深浅色绘制再切换；接线者只看到“请在 onCreate 调用”，按原样补调用点不会发现时序问题。源端把主题放在 super.onCreate 之前正是为了首帧生效，这一时机若只留在设计参考里、没写进功能契约，下游就收不到。来源中偏好 worker 自己注意到 setColorMode 是进程态、需跨启动恢复，仍写成 async 恢复并交接，收口者不等待地调用。

## 做法

1. 在 EntryAbility.onCreate 的同步路径用 preferences.getPreferencesSync 读取主题键，并在 onWindowStageCreate 的 loadContent 之前完成 setColorMode。
2. 规格提取读入口 Activity.onCreate 时，把 super.onCreate/setContentView 之前的调用（如 setTheme）连同“首帧前生效”的时机写进功能契约，并指定目标承接位置。
3. 为启动恢复写移交时写明时序约束（如“首帧前同步生效”）；接线者看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只机械补调用点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕Context.setTheme 设定基础主题，源码注释要求在该 Context 实例化任何 View 之前调用（例如 setContentView 或 LayoutInflater.inflate 之前）
- 〔做法第 1 步〕启动 UIAbility 时依次触发 onCreate、onWindowStageCreate、onForeground；页面在 onWindowStageCreate 中经 loadContent 加载
- 〔做法第 1 步〕preferences.getPreferencesSync 同步返回 Preferences 实例，首次获取时从持久化文件读入并缓存；getSync 在值为 null 或类型与 defValue 不同时返回 defValue
- 〔做法第 1 步〕ApplicationContext.setColorMode 只能在主线程调用；接口参考的说明要求在 onWindowStageCreate 中通过 loadContent 加载页面之后调用，而深浅色适配指南的示例在 EntryAbility.onCreate 里调用它；深浅色生效优先级为 UIAbility 的设置 > 应用的设置 > 系统
- 〔做法第 1 步〕ConfigurationConstant.ColorMode 中 COLOR_MODE_NOT_SET（-1）表示不设置、跟随系统或应用，是缺省值，COLOR_MODE_DARK（0）为深色，COLOR_MODE_LIGHT（1）为浅色；应用没有调用 setColorMode 时默认跟随系统切换深浅色
- 〔原因〕EntryAbility.onCreate 中不等待地调用一个先 await 异步偏好加载、再 setColorMode 的函数时，首帧按系统深浅色绘制，偏好加载完成后主题才切换
- 〔做法第 1 步〕在 EntryAbility.onCreate 中用 getPreferencesSync 同步读出主题并调用 ApplicationContext.setColorMode 时，首帧即按所设深浅色绘制
