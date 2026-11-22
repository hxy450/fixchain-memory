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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1；androidx.appcompat:appcompat 1.1.0、1.8.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 2 步〕安卓 Context.setTheme(int) 的说明要求在 Context 里实例化任何 View 之前调用（例如在 Activity.setContentView 或 LayoutInflater.inflate 之前）；实现上 ContextThemeWrapper 把新 style 用 applyStyle(resid, true) 叠加到已有主题上（不是换掉整个主题），Activity.setTheme 同时设给 Window；已经实例化的 View 在构造时读过的属性不随之改变
- 〔适用情境 / 做法第 1 步〕AppCompatDelegate 的夜间模式常量（appcompat 1.1.0 与 1.8.0 相同）：MODE_NIGHT_FOLLOW_SYSTEM = -1、MODE_NIGHT_NO = 1、MODE_NIGHT_YES = 2、MODE_NIGHT_AUTO_BATTERY = 3、MODE_NIGHT_AUTO_TIME = 0（MODE_NIGHT_AUTO 同值）、MODE_NIGHT_UNSPECIFIED = -100；setDefaultNightMode(int) 只接受 -1 到 3，值有变化时记下并立即应用到已创建的 AppCompat 界面（applyDayNightToActiveDelegates），传其他值（包括 MODE_NIGHT_UNSPECIFIED）只打一行日志、不改设置；数值与鸿蒙 ColorMode 不对应（鸿蒙 COLOR_MODE_DARK = 0、COLOR_MODE_LIGHT = 1），要按含义映射：FOLLOW_SYSTEM → COLOR_MODE_NOT_SET，NO → COLOR_MODE_LIGHT，YES → COLOR_MODE_DARK
- 〔做法第 1 步〕ConfigurationConstant.ColorMode（首段 @since 9，从 @kit.AbilityKit 导入 ConfigurationConstant）：COLOR_MODE_NOT_SET = -1（不设置，跟随系统）、COLOR_MODE_DARK = 0、COLOR_MODE_LIGHT = 1
- 〔适用情境 / 做法第 1 步〕ApplicationContext.setColorMode(colorMode: ConfigurationConstant.ColorMode): void（首段 @since 11）设置应用的深浅色模式，只能在主线程调用，参数错误抛 401、context 不存在抛 16000011；设置后应用的深浅色固定、不随系统变化；ApplicationContext 在 UIAbility 里由 this.context.getApplicationContext() 取得
- 〔做法第 1 步〕setColorMode 的调用时机文档两处说法不同：接口参考在 ApplicationContext.setColorMode 的说明里写调用前要确保窗口已创建、页面已加载，即在 onWindowStageCreate 里 loadContent 之后调用；深浅色适配指南「应用主动设置深浅色模式」和「系统判定应用深浅色模式的规则」的示例都在 UIAbility.onCreate 里调用 this.context.getApplicationContext().setColorMode(...)
- 〔适用情境〕UIAbilityContext.setColorMode(colorMode: ConfigurationConstant.ColorMode): void（@since 18）设置单个 UIAbility 的深浅色，生效优先级为 UIAbility 的设置 > 应用的设置（ApplicationContext.setColorMode）> 系统；调用后会新建资源管理器；应用用 setColorMode 手动设置深浅色后不再收到 onConfigurationUpdate 回调
- 〔原因 / 做法第 1 步〕用户启动 UIAbility 时系统依次触发 onCreate()、onWindowStageCreate()、onForeground()；页面在 onWindowStageCreate() 里经 loadContent() 加载，所以 onCreate 里同步完成的调用早于页面加载，onCreate 里发起而不等待的 Promise 不保证在 loadContent 之前完成
- 〔做法第 1 步〕preferences.getPreferencesSync(context: Context, options: Options): Preferences（首段 @since 10，import { preferences } from '@kit.ArkData'）同步取 Preferences 实例、载入文件全部数据并驻留内存，同一文件再次调用直接取缓存；Preferences.getSync(key: string, defValue: ValueType): ValueType（首段 @since 10）同步读，值为 null 或类型与 defValue 不同时返回 defValue
