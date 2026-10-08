# 阶段：计划与派工（plan）

本阶段可用的 29 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/capability](../topics/app/capability/index.md) — 平台能力与厂商 SDK 的等价判定：先查 Kit、ohpm 与本地声明再选型，不可用时运行期显式降级而非阻断或伪造

- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](../topics/app/capability/lesson-e9890889e591196c3d0d.lesson.md) · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit

### [app/cross-cutting](../topics/app/cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

- [日志迁移审计按源端调用边界列日志点，不只核对配置](../topics/app/cross-cutting/lesson-e23468a0e439f8cf53e9.lesson.md) · 信号：log2File, debugFile, BqLog, hilog.info
- [退出登录先停同步再单事务清账号业务表并广播](../topics/app/cross-cutting/lesson-8b8e304a737e9fded451.lesson.md) · 信号：clearAllTables, RelationalStore, preferences, accessToken

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入声明、扩展能力与卡片登记

- [form_config 规格与刷新从源卡片声明换算，不填默认](../topics/app/entry/lesson-bc48518f40742add0054.lesson.md) · 信号：form_config, supportDimensions, defaultDimension, updateEnabled

### [app/modules](../topics/app/modules/index.md) — 多模块（壳 HAP + HAR）边界：构建常量来源、跨模块导入、资源闭包归属与可复用函数的模块放置

- [业务模块拆分按页面归属建表，不以源包分组为边界](../topics/app/modules/lesson-99b35920e77ae01076ea.lesson.md) · 信号：pageMap, NavPathStack, oh-package.json5, features/

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [应用显示名同时改 AppScope 与入口 label 值](../topics/app/resources/lesson-55f44e2efdc1a49ac387.lesson.md) · 信号：app_name, EntryAbility_label, string.json, app.json5

### [app/startup](../topics/app/startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

- [目标初始化极快时把首启加载页最短可见时长写进验收](../topics/app/startup/lesson-41bb62cd13921e4eedde.lesson.md) · 信号：SplashActivity, SplashScreen, windowStage.loadContent, setTimeout
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/network-endpoint](../topics/data/network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

- [网络权限声明进 module.json5，任务要有写者](../topics/data/network-endpoint/lesson-faec7be031b7f64752c4.lesson.md) · 信号：module.json5, requestPermissions, ohos.permission.INTERNET, ohos.permission.GET_NETWORK_INFO

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作

- [首次启动播种在启动路径落调用并保留标记门控](../topics/data/storage/lesson-dc3f2589254d02893b0e.lesson.md) · 信号：Application.onCreate, seedDemoDataOnFirstLaunch, has_seeded_demo_data, EntryAbility.onCreate
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [占位只登记输入缺值的情况，能实现的当场实现](../topics/process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md) · 信号：forward-ref-uncertain, resource-pending-asset, .d.ts, getXxxProperties
- [子代理派发失败先修参数重试，再按降级条款补跑](../topics/process/deferred-fulfillment/lesson-ae78da6f1a3669f6ef59.lesson.md) · 信号：spawn_agent, api-inventory
- [点击入口写具体导航契约，无兑现方不留 forward-ref](../topics/process/deferred-fulfillment/lesson-7f6b818559cfac767e4b.lesson.md) · 信号：forward-ref, WebView, URL, Intent
- [超时查 list_agents，running 就等待不代写](../topics/process/deferred-fulfillment/lesson-39e7e31b88e3d6176022.lesson.md) · 信号：list_agents, agent_status, PASS

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [应用壳契约枚举源导航全部入口含深链与 scheme](../topics/process/enumeration-gaps/lesson-3348c580951ef82a9737.lesson.md) · 信号：NavPathStack, onNewWant, onCreate, module.json5
- [截图页范围含其入口直达二级页，不取最窄解释](../topics/process/enumeration-gaps/lesson-91c89aff3f8c5c47bd2a.lesson.md) · 信号：startActivity, Intent, Activity, setOnClickListener

### [process/handoff-loss](../topics/process/handoff-loss/index.md) — 跨阶段推进、批次收口、重新规划或转述派工时，移交项、全局动作与规则原文在传递中丢失

- [执行替换清单先建公共门面，收尾 rg 旧写法归零](../topics/process/handoff-loss/lesson-af15c43279110b3b7692.lesson.md) · 信号：ToastService, promptAction.showToast, DialogHelper.showToast, LazyForEach
- [推进阶段前核对约定产物与放行门，待接事项落负责方](../topics/process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md) · 信号：open_questions, HARD-GATE, BLOCKER, send_message
- [派工必读清单覆盖语义来源，提速要求下也保留](../topics/process/handoff-loss/lesson-8598e0af342dd5c8ba28.lesson.md) · 信号：Modifier, .shadow(, hitTest, Screen
- [转述规则保留替代写法；禁并发构建的改动汇总后立即全量构建](../topics/process/handoff-loss/lesson-73a7dd4f78cb747f7e7e.lesson.md) · 信号：Record, HashMap
- [重新规划时把已批准未执行规格逐条映射到新计划](../topics/process/handoff-loss/lesson-b843621a5b9c279b1b2b.lesson.md) · 信号：a2h-plan, plan.md, decision-ledger, re-plan

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [页面归属按实际 Service 调用判定，不按模块默认](../topics/process/inferred-not-traced/lesson-ad7d770bd5b826e58516.lesson.md) · 信号：resolve_by, Retrofit, Service, page_id

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [共享组件挂载页面以源宿主容器 replace/add 为准](../topics/process/secondary-over-source/lesson-34c8ac69ad849f8c24e1.lesson.md) · 信号：FragmentTransaction, replace(, add(, Fragment
- [派工要求按源码确认的值回源码核对，没读到标未核实](../topics/process/secondary-over-source/lesson-93214f5a49c4d1d82316.lesson.md) · 信号：kapt stub, .kt, Interceptor, grep

### [process/unloaded-input](../topics/process/unloaded-input/index.md) — 必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

- [上下文压缩后按 spec_ref 与源码锚点重读再写计划代码](../topics/process/unloaded-input/lesson-f616adca9430826b1661.lesson.md) · 信号：spec_ref, feature-index, integration_points, Activity
- [编排者代写切片前加载 worker 的全部派工输入](../topics/process/unloaded-input/lesson-b90d7f55409a3a34253d.lesson.md) · 信号：spec_refs, feature-plan, ui-manifest, Adapter
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/layout/safearea](../topics/ui/layout/safearea/index.md) — 全屏窗口安全区：避让值单位、expandSafeArea 与前景 padding 之别、inset 只消费一次及承载层

- [下发状态栏高度参数需写明消费层，Stack 各层同基准](../topics/ui/layout/safearea/lesson-2cf2614847a8dba832b3.lesson.md) · 信号：Stack, @Param, windowTopPadding, statusBarHeight

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [多屏共享清理归外层生命周期，切屏不释放](../topics/ui/navigation/hosts/lesson-2ed8c21943925bf0ae9a.lesson.md) · 信号：DisposableEffect, onDispose, EntryAbility.onDestroy, aboutToDisappear

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [推迟通知能力时为接口返回数据定义替代去向](../topics/ui/state/feedback/lesson-9d54e42c44b0d3e78bb1.lesson.md) · 信号：NotificationManager, onData, Toast, showToast

### [ui/text/copy](../topics/ui/text/copy/index.md) — 可见文案的来源：沿资源引用链取逐字值、静态页文案取自 XML、代码格式化文案建参数化资源、语言目录按源生成。

- [可见文案沿引用链取 strings.xml 逐字值，非枚举名](../topics/ui/text/copy/lesson-31ab9f59945e5f0259ea.lesson.md) · 信号：strings.xml, @string/, stringResource
