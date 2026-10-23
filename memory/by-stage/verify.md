# 阶段：验证与判读（verify）

本阶段可用的 42 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/capability/degradation](../topics/app/capability/degradation/index.md) — 能力确实不可用时只降级做不到的一步，运行期显式提示

- [激励广告不可用时显式提示并按台账放行，不伪造奖励](../topics/app/capability/degradation/lesson-0f67121af7969203b76b.lesson.md) · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward

### [app/capability/sdk-lookup](../topics/app/capability/sdk-lookup/index.md) — 判定无等价前先查 Kit、ohpm、SDK 声明与权限注解

- [计费网络判定按承载显式映射，不靠单能力位](../topics/app/capability/sdk-lookup/lesson-20afdfffa13dc5bca10c.lesson.md) · 信号：isActiveNetworkMetered, @ohos.net.connection, NET_CAPABILITY_NOT_METERED, bearerTypes

### [app/cross-cutting](../topics/app/cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

- [日志迁移审计按源端调用边界列日志点，不只核对配置](../topics/app/cross-cutting/lesson-e23468a0e439f8cf53e9.lesson.md) · 信号：log2File, debugFile, BqLog, hilog.info
- [诊断日志上传按源端打包清单与协议实现，收窄先确认](../topics/app/cross-cutting/lesson-d434bb5c16bc721d9a00.lesson.md) · 信号：usesCleartextTraffic, networkSecurityConfig, presignedUrl, http.request

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入与结果回传、扩展能力与卡片登记

- [shortcuts 元数据挂 Ability 下，不挂模块级](../topics/app/entry/lesson-67118603fcc769a5edc9.lesson.md) · 信号：ohos.ability.shortcuts, module.json5, $profile:, shortcuts_config

### [app/hybrid](../topics/app/hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

- [插件标可用前追到原生实现核对权限与返回状态](../topics/app/hybrid/lesson-4b7012d4bdceef5e8c36.lesson.md) · 信号：requestPermissions, ohosPermissions, photoAccessHelper, Permission.storage

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [8 位颜色保持 #AARRGGBB，转换后逐项往返核对](../topics/app/resources/lesson-783faf2767a952034514.lesson.md) · 信号：colors.xml, color.json, #AARRGGBB, #RRGGBBAA
- [分层图标前景裁到可见区，前景背景同尺寸](../topics/app/resources/lesson-d838f9236f7452b82738.lesson.md) · 信号：adaptive-icon, layered-image, layered_image.json, mipmap
- [颜色只写 hex 或 $color:，数组项写成对象](../topics/app/resources/lesson-94a3f7a5ec5ad8f8a3e8.lesson.md) · 信号：colors.xml, arrays.xml, @android:color, $color:

### [app/startup](../topics/app/startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

- [首启无已选项时定义显式空态，不以空编码请求](../topics/app/startup/lesson-95aa64d6b0a5c041d326.lesson.md) · 信号：hasInit, selectedCity, cityCode, preferences
## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [build() 组件逐行书写，含组件方法用 @Builder](../topics/arkts/ui-syntax/lesson-08e71bb72d05b1d79d28.lesson.md) · 信号：build(), @Builder, ForEach, Repeat
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/model](../topics/data/model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持

- [完成态派生逐分支移植源函数，审计摘要只作线索](../topics/data/model/lesson-4ad956bab5fca6d7f418.lesson.md) · 信号：isCompleted, completedCount, completionMode, occurrenceDate

### [data/parsing](../topics/data/parsing/index.md) — JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度

- [先定目标 res.data 对应源端哪层类型，再逐层写取值键](../topics/data/parsing/lesson-dc5c370e370c2be803c1.lesson.md) · 信号：res.data, BaseResponse&lt;T&gt;, getObject, getArray

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与迁移、自增主键写入、预置数据与播种时机、fileIo 文件与目录操作

- [Room 迁移保留库名、schema 版本与显式升级分支](../topics/data/storage/lesson-a6f300f9295ba538f23b.lesson.md) · 信号：@Database(version, addMigrations, AutoMigration, fallbackToDestructiveMigration
- [单语句直接写，事务含 await 用独立事务](../topics/data/storage/lesson-a078efd3361b4abe58e3.lesson.md) · 信号：createTransaction, beginTransaction, beginTrans, rollBack

### [data/sync](../topics/data/sync/index.md) — 同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤

- [同步终态只在最后一轮后发一次，开始进度保留源门控](../topics/data/sync/lesson-34f35851208470602570.lesson.md) · 信号：SyncCoordinator, EventBus, onComplete
- [同步调度合并在途任务要补跑尾随请求，失败项重推](../topics/data/sync/lesson-cfe552e1b20080212ce9.lesson.md) · 信号：Mutex.withLock, Promise
- [重写多阶段数据流程时保留缓存写入等副作用步骤](../topics/data/sync/lesson-686bbe76f7c2c783f2bd.lesson.md) · 信号：DAO, currentId, Repository
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/check-gaming](../topics/process/check-gaming/index.md) — 用注释关键字、删功能、改产品语义或相似度阈值迎合检查与测试通过，而非落实源端语义

- [单测失败先用同一输入核对源端，不改产品语义迁就](../topics/process/check-gaming/lesson-75cb65ef5601aaa8f159.lesson.md) · 信号：BLOCKED, manual_review
- [单测预期按源端实现手算，不编造更严的过滤期望](../topics/process/check-gaming/lesson-5bc9af19bedaecaf627c.lesson.md) · 信号：@Test, assertEquals, hypium, describe(
- [相似度达标但与修复预测不符或铺不满的残差仍立单](../topics/process/check-gaming/lesson-494c9b596df7e7e788f9.lesson.md) · 信号：px

### [process/claimed-without-receipt](../topics/process/claimed-without-receipt/index.md) — 凭文本形式的调用、部分输出、过期构建或自动脚本结果宣告写入与完成，缺少真实回执核验

- [写文件以执行回执为准，覆盖入口页后内容断言读回](../topics/process/claimed-without-receipt/lesson-776ed5eb216833c6b002.lesson.md) · 信号：loadContent, Hello World, RelativeContainer, apply_patch
- [功能对齐以代码落点为准，空回调不算实现](../topics/process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md) · 信号：onClick, JSON.stringify, NavPathStack, onEventMainThread
- [编译按完整 ERROR 列表判定，失败只记 FAIL](../topics/process/claimed-without-receipt/lesson-7426a20525e52e34c2e7.lesson.md) · 信号：COMPILE RESULT, BUILD SUCCESSFUL, BUILD FAILED, hvigor
- [缺 hvigorw 时用工具自带构建，文本契约不算编译](../topics/process/claimed-without-receipt/lesson-25bc0b7518d335a947d6.lesson.md) · 信号：hvigorw, assembleHap, command-line-tools/bin/hvigorw, CompileArkTS
- [自愈脚本改写 .ets 后先审 diff，异常尺寸回滚](../topics/process/claimed-without-receipt/lesson-bdb97da6a6eb8d68435f.lesson.md) · 信号：icon-sizing, .width, .height, Image

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [占位只登记输入缺值的情况，能实现的当场实现](../topics/process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md) · 信号：forward-ref-uncertain, resource-pending-asset, .d.ts, getXxxProperties

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [Application 注册的接收器读本体写入规格](../topics/process/enumeration-gaps/lesson-4fb1c103822a8fd30b2a.lesson.md) · 信号：BroadcastReceiver, registerReceiver, CONNECTIVITY_ACTION, @ohos.net.connection
- [系统表面降级为应用内页时写明入口位置与形式](../topics/process/enumeration-gaps/lesson-238588d3cceaf707ccfe.lesson.md) · 信号：Widget, AppWidget, FormExtensionAbility, LongPressGesture

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [守卫移到调用侧时并入被调方法体内全部守卫](../topics/process/inferred-not-traced/lesson-06e3564e91948a2b05a3.lesson.md) · 信号：saveStateToFile, saveState, createNewGame, initialize()
- [页面入口只按布局与页面类实际绑定推导，不补源端没有的控件](../topics/process/inferred-not-traced/lesson-76aa7901a0ae1af9d544.lesson.md) · 信号：initView, setOnClickListener, ViewModel, onClick

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [点击无响应先设备复现定位，未上机结论标未验证](../topics/process/unverified-as-fact/lesson-afae8d13e00941efe808.lesson.md) · 信号：hitTestBehavior, uitest uiInput click, dumpLayout, hdc shell
- [颜色差异立单用像素均值和源端算式给期望值](../topics/process/unverified-as-fact/lesson-aae5f345ed2ced099757.lesson.md) · 信号：PNG, blendMode, ColorFilter
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/dialog/content](../topics/ui/dialog/content/index.md) — 弹窗内容与行为的还原：按源布局逐控件重建、复用共享弹窗组件、打开触发点、展开后加载数据、下拉关闭的手势门禁。

- [源端委托共享弹窗时复用目标共享组件不留副本](../topics/ui/dialog/content/lesson-6d3ac9a5c0382377b91e.lesson.md) · 信号：XxxDialog.show, onAction, Dialog.show, DialogFragment

### [ui/dialog/mounting](../topics/ui/dialog/mounting/index.md) — 弹窗挂载层级与宿主节点：sheet 之上、覆层挂整窗根、锚点所在页、SheetMode 与 targetId

- [依附式弹窗宿主按锚点视图所在页确定，按实测坐标定位](../topics/ui/dialog/mounting/lesson-29f62d177a17d08b4e4f.lesson.md) · 信号：AttachPopup, atView, componentUtils, Fragment

### [ui/interaction/click-binding](../topics/ui/interaction/click-binding/index.md) — 点击绑定的归属与副作用：挂在源端真正持有点击的节点、按处理器分支迁副作用、回调契约兑现、被注释的监听视为死按钮。

- [监听回调体被注释时按无响应控件迁移，审计不放行](../topics/ui/interaction/click-binding/lesson-f3e614f295aa409485fd.lesson.md) · 信号：setOnClickListener, android:clickable, onClick, TODO

### [ui/interaction/input](../topics/ui/interaction/input/index.md) — EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

- [平台正则按定义逐段移植并全串匹配](../topics/ui/interaction/input/lesson-90e0f1db3e1e13a6fd6a.lesson.md) · 信号：Patterns.WEB_URL, Patterns.EMAIL_ADDRESS, String.matches, (?i)

### [ui/navigation/handoff](../topics/ui/navigation/handoff/index.md) — 跳转动作随行的交接：点击出口落实际跳转、跳前写入的共享状态、结果回传写回、同窗口 push 的方向切换与恢复。

- [跳转前写入的共享状态是契约，按原顺序迁移](../topics/ui/navigation/handoff/lesson-dfcdbb19cd93d29159b2.lesson.md) · 信号：setPlaylist, startActivity, pushPathByName, onClick

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [全局广播浮层按源端队列语义播放不自加去重上限](../topics/ui/state/feedback/lesson-2cc8bcca579d597cb6a2.lesson.md) · 信号：addAll, remove(0), onAnimationEnd, WindowManager

### [ui/text/typography](../topics/ui/text/typography/index.md) — 文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

- [可折叠正文按测量高度判溢出，默认 Clip](../topics/ui/text/typography/lesson-c61ac79c7db81729a544.lesson.md) · 信号：onTextLayout, didOverflowHeight, hasVisualOverflow, maxLines

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [tint 着色渐变装饰层用容器 linearGradient](../topics/ui/theme/effects/lesson-fcd86aeea6209ea0718b.lesson.md) · 信号：app:tint, ?attr/colorBackground, fillColor, linearGradient

### [ui/theme/sources](../topics/ui/theme/sources/index.md) — 控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

- [视觉修复以源布局为准，截图差先折算 vp 再三方对照](../topics/ui/theme/sources/lesson-8119d8bf0b58e4daac24.lesson.md) · 信号：@Preview, docs/assets, setVisibility, getChannel
