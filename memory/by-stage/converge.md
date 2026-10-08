# 阶段：收敛与移交（converge）

本阶段可用的 22 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/strict-mode](../topics/arkts/strict-mode/index.md) — ArkTS 严格类型系统对对象字面量、接口实现、异常收窄与类声明顺序的限制，不编译时也会留到编译门

- [接口参数用 implements 的具名类，不传函数字面量](../topics/arkts/strict-mode/lesson-931ef95a3d0cf202fe5b.lesson.md) · 信号：Port, Repository, Adapter

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [@BuilderParam 传值写箭头闭包不传方法引用](../topics/arkts/ui-syntax/lesson-7d643db6ab406ae64c77.lesson.md) · 信号：@BuilderParam, 10905102, @Builder, content: this.
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/model](../topics/data/model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持

- [带本月语义的保存与查询按源实体构造参数建关联键](../topics/data/model/lesson-6a95a3ae5f47a15892fc.lesson.md) · 信号：Budget(month, getBudgetByTimestamp, Repository, @Query

### [data/network-endpoint](../topics/data/network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

- [网络权限声明进 module.json5，任务要有写者](../topics/data/network-endpoint/lesson-faec7be031b7f64752c4.lesson.md) · 信号：module.json5, requestPermissions, ohos.permission.INTERNET, ohos.permission.GET_NETWORK_INFO

### [data/network-request](../topics/data/network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

- [cryptoFramework 规格串只写算法位数，结果判空](../topics/data/network-request/lesson-3684e08592c85de82204.lesson.md) · 信号：cryptoFramework, createAsyKeyGenerator, convertPemKeySync, doFinalSync

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作

- [首次启动播种在启动路径落调用并保留标记门控](../topics/data/storage/lesson-dc3f2589254d02893b0e.lesson.md) · 信号：Application.onCreate, seedDemoDataOnFirstLaunch, has_seeded_demo_data, EntryAbility.onCreate
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/claimed-without-receipt](../topics/process/claimed-without-receipt/index.md) — 凭文本形式的调用、部分输出、过期构建或自动脚本结果宣告写入与完成，缺少真实回执核验

- [自愈脚本改写 .ets 后先审 diff，异常尺寸回滚](../topics/process/claimed-without-receipt/lesson-bdb97da6a6eb8d68435f.lesson.md) · 信号：icon-sizing, .width, .height, Image

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [占位只登记输入缺值的情况，能实现的当场实现](../topics/process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md) · 信号：forward-ref-uncertain, resource-pending-asset, .d.ts, getXxxProperties
- [子代理派发失败先修参数重试，再按降级条款补跑](../topics/process/deferred-fulfillment/lesson-ae78da6f1a3669f6ef59.lesson.md) · 信号：spawn_agent, api-inventory
- [解前向占位按触发文本逐项兑现，写常量不算闭合](../topics/process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md) · 信号：FWD-REF, forward-ref-uncertain, TODO, return false
- [超时查 list_agents，running 就等待不代写](../topics/process/deferred-fulfillment/lesson-39e7e31b88e3d6176022.lesson.md) · 信号：list_agents, agent_status, PASS

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [应用壳契约枚举源导航全部入口含深链与 scheme](../topics/process/enumeration-gaps/lesson-3348c580951ef82a9737.lesson.md) · 信号：NavPathStack, onNewWant, onCreate, module.json5
- [截图页范围含其入口直达二级页，不取最窄解释](../topics/process/enumeration-gaps/lesson-91c89aff3f8c5c47bd2a.lesson.md) · 信号：startActivity, Intent, Activity, setOnClickListener

### [process/handoff-loss](../topics/process/handoff-loss/index.md) — 跨阶段推进、批次收口、重新规划或转述派工时，移交项、全局动作与规则原文在传递中丢失

- [执行替换清单先建公共门面，收尾 rg 旧写法归零](../topics/process/handoff-loss/lesson-af15c43279110b3b7692.lesson.md) · 信号：ToastService, promptAction.showToast, DialogHelper.showToast, LazyForEach
- [推进阶段前核对约定产物与放行门，待接事项落负责方](../topics/process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md) · 信号：open_questions, HARD-GATE, BLOCKER, send_message
- [派工必读清单覆盖语义来源，提速要求下也保留](../topics/process/handoff-loss/lesson-8598e0af342dd5c8ba28.lesson.md) · 信号：Modifier, .shadow(, hitTest, Screen
- [转述规则保留替代写法；禁并发构建的改动汇总后立即全量构建](../topics/process/handoff-loss/lesson-73a7dd4f78cb747f7e7e.lesson.md) · 信号：Record, HashMap

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [共享组件替换页面片段前逐项比对源码视觉](../topics/process/secondary-over-source/lesson-ad6f23b88f09b55dd92a.lesson.md) · 信号：orphan component, @Builder, borderRadius, fontColor

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [点击无响应先设备复现定位，未上机结论标未验证](../topics/process/unverified-as-fact/lesson-afae8d13e00941efe808.lesson.md) · 信号：hitTestBehavior, uitest uiInput click, dumpLayout, hdc shell
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [NavDestination 首屏只注册并压栈不作根内容](../topics/ui/navigation/hosts/lesson-8953e390416a80d7dd8c.lesson.md) · 信号：Builder function is empty, current stack is not navPathStack, navDestination, NavDestinationContext

### [ui/state/lifecycle](../topics/ui/state/lifecycle/index.md) — 生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

- [重载入口改订阅，子页返回不触发 aboutToAppear](../topics/ui/state/lifecycle/lesson-b3bb0bc33f4caded78a2.lesson.md) · 信号：aboutToAppear, onShown, onPageShow, pushPathByName

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [elevation 阴影按 vp2px 换算并集中到共享函数](../topics/ui/theme/effects/lesson-d0aad947e26220fb43fa.lesson.md) · 信号：ShadowOptions, Modifier.shadow, vp2px, .shadow(
