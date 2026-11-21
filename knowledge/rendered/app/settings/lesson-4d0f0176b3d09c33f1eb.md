# 迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只调持久化 setter、只写远端设置不算完成

## 何时使用

功能接线阶段实现设置页开关与偏好仓库，或页面转换遇到按偏好切换的渲染与行为分支时；迁移设置页的保存逻辑，或切换即持久化的界面状态（如首页视图位置）时

## 适用情境

源端设置用 DataStore/SharedPreferences 持久化，并被主题、计时器、反馈等运行期代码实时读取；目标端的设置页、偏好仓库、主题状态和消费页面由不同任务编写，靠占位登记传递“持久化并立即生效”的契约。也包括源端设置保存除远端同步外还更新本地配置缓存并发刷新事件（如排序设置保存后各列表按新配置排序），目标只写远端设置；以及源端切换视图即写偏好、启动时读取恢复，目标只改内存状态。也包括应用内语言选择只调用持久化的偏好语言接口，而规格要求保存后立即切换。

## 原因

设置页只调持久化 setter 时，开关看起来能切换，行为却不变；消费方在另一个文件，编译和结构审计都不检查。来源中主题与波浪计时器开关只写偏好，主题状态类除默认值外无人读写；步骤提示音与振动开关同样没有消费方，振动封装也没移植；页面转换者以“偏好未知”为由只写了进度样式的一个分支，还是源端默认值之外的那个。另一应用的排序设置保存只写远端设置，列表查询不读任何本地排序配置，重构时又原样抽进 ViewModel；首页视图位置的持久化规格获批后没有排期，视图选择只写内存，重启总回默认视图。

## 做法

1. 为每个开关写出“键 → 读取点 → 效果”：主题类接到全局主题状态（@ObservedV2/@Trace），由应用入口在启动和 onConfigurationUpdate 时应用（如 ApplicationContext.setColorMode）；渲染样式类接到对应组件的分支；反馈类在事件分支里读开关再播放或振动。
2. 页面转换遇到按偏好切换的渲染分支时，两个分支都实现并以源端默认值为初值，或在该位置登记指向设置切片的前向占位；不要静态只写一个分支。
3. 反馈类：本地提示音用 rawfile 加 AVPlayer（resourceManager.getRawFd 设给 fdSrc）；振动移植源端封装，并在 module.json5 的 requestPermissions 声明 ohos.permission.VIBRATE。
4. 收尾 grep 偏好 getter 与状态字段：除默认值和 setter 外没有读取点的开关就是没完成。
5. 迁移设置页保存逻辑时列出源端保存处理的全部副作用（远端同步、本地配置缓存、刷新事件），每一项在目标端指明消费者；配置键或加载函数在仓库、查询服务中没有调用点就是未接通。
6. 切换即持久化、启动恢复的界面状态，写入与恢复两端都落地：切换时先持久化再更新状态，恢复放在偏好异步加载完成之后，非法值按源端规则回退。
7. 应用内语言切换核对所选 API 的生效时机：偏好语言接口（setAppPreferredLanguage）按偏好在应用启动时加载资源；要求保存后立即切换时另行让当前进程即时生效（来源采用 ApplicationContext.setLanguage），并刷新已显示的代码内取值文案，以 SDK 声明或真机确认。

来源支持：6 张卡 · 4 次迁移 · 4 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 6 步〕用户首选项默认的 XML 存储模式下，put / putSync 只改内存中的 Preferences 实例，flush / flushSync 后才写入文件；用 on('change') 订阅的回调也要等 flush 执行后才触发。只 put 不 flush 时，同进程内读得到新值，但进程被杀后重启读回旧值，订阅方也收不到变更。〔成立范围：对象：@ohos.data.preferences 的 Preferences 实例。例外：API 18 起可选的 GSKV 存储模式写入实时落盘，订阅回调不需 flush 即触发。依据是 SDK 声明注释和文档说明。最常见的不成立情形：创建实例时选了 GSKV 存储模式。〕
- 〔做法第 7 步〕i18n.System.setAppPreferredLanguage 设置的偏好语言在应用启动时用于加载资源；设为 'default'（恢复跟随系统语言）要应用冷启动后才生效。〔成立范围：对象：@ohos.i18n 的 System.setAppPreferredLanguage。依据是 SDK 声明注释和文档说明；设为具体语言后当前进程已显示的界面是否立即切换，开发指南写「界面会切换为目标语言」、声明注释写「启动时按偏好语言加载」，两处没说清（记入 device_todo）。最常见的不成立情形：传入的既不是合法语言 ID 也不是 'default'，接口抛 890001 参数错误。〕
- 〔做法第 7 步〕ApplicationContext.setLanguage 设置应用语言，只能在主线程调用，文档要求在窗口创建完成、loadContent 加载页面之后调用；设置后应用不再能订阅系统语言的变化。〔成立范围：对象：ApplicationContext.setLanguage。依据是文档说明；进程重启后是否保留，文档没写。最常见的不成立情形：在 EntryAbility.onCreate 或 loadContent 之前调用，不在文档保证的范围内。〕
- 〔做法第 1 步〕深浅色生效优先级为 UIAbility 级（UIAbilityContext.setColorMode）> 应用级（ApplicationContext.setColorMode）> 系统；应用没设时为默认的 COLOR_MODE_NOT_SET、跟随系统，设成深色或浅色后深浅色固定、不随系统变化，onConfigurationUpdate 等订阅也收不到系统深浅色的变化。〔成立范围：对象：ApplicationContext.setColorMode 与 UIAbilityContext.setColorMode，只能在主线程调用。例外：应用从未调用 setColorMode 且工程 dark 目录下没有任何深色资源时，系统组件在系统深色模式下仍保持浅色，文档建议显式设为 COLOR_MODE_NOT_SET 才让它们跟随系统。依据是文档说明。最常见的不成立情形：工程里某个 UIAbility 自己调过 UIAbilityContext.setColorMode，应用级设置对这个 UIAbility 不起作用。〕
- 〔做法第 3 步〕resourceManager.getRawFd 返回的 fd 是 rawfile 所在 HAP 包的文件描述符，offset 是该 rawfile 在 HAP 内的起点、length 是它的长度；AVPlayer 的 fdSrc（AVFileDescriptor）不传 offset 时按 0、不传 length 时读到文件末尾，所以只传 fd 会从 HAP 包头开始读，fd、offset、length 要一起传。〔成立范围：对象：getRawFd 的返回值交给 AVPlayer.fdSrc。依据是 SDK 声明注释。最常见的不成立情形：fd 来自自己打开的沙箱文件（整个文件就是媒体），只传 fd 即从文件头播放。〕
- 〔做法第 3 步〕AVPlayer 播纯音频时 audioRendererInfo 的 usage 默认是 STREAM_USAGE_MUSIC；按系统音频焦点策略，后开始的音乐流会让先在播的音乐流（如别的应用以音乐类型播放的歌曲）停止，所以用默认 usage 播提示音会打断用户正在听的音乐。audioRendererInfo 只能在 initialized 状态、首次 prepare 之前设置。〔成立范围：对象：AVPlayer（媒体源含视频时默认 usage 为 STREAM_USAGE_MOVIE）。条件：焦点处理按双方的 usage 决定，例如音乐流与游戏流可并发混音、互不影响；打断针对别的应用的流，同一应用创建的多个流默认是共享焦点模式（SHARE_MODE），彼此不按焦点策略打断；应用用音频会话管理（AudioSession）改了焦点策略时按其设置。依据是 SDK 声明注释和文档说明。最常见的不成立情形：已在 initialized 状态把 usage 设成别的类型，按那种类型的焦点策略处理。〕
