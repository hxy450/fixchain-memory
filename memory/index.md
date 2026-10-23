# 迁移经验

经验库版本：`276c45d921fb516691f9f45b45803e79886abb4bb9e1569dd57b2bb699fda6ed`

## 怎样召回

1. 先写下当前任务的阶段、输入里出现的符号（API、组件、装饰器、文件名）和领域猜测。
2. 用 `catalog.jsonl`（每行一条经验：id、summary、topic、stage、signals、support、path）或 `signals.json`（符号 → 经验 id）按这三者过滤出候选；也可从下面的领域或阶段入口浏览，目录索引只列下一层。
3. 只读 3 到 5 条候选的正文（catalog 的 path 列，位于 `topics/<主题>/<id>.lesson.md`），核对适用条件后回到任务；无关分支可跳过，任务已获足够指导即可继续。

这是发布时的 active 快照，不会自动追踪之后的撤回；新任务应使用维护者提供的最新阅读包。

## 领域

- [app](topics/app/index.md) — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物（127 条）
- [arkts](topics/arkts/index.md) — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异（38 条）
- [data](topics/data/index.md) — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持（56 条）
- [process](topics/process/index.md) — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制（70 条）
- [ui](topics/ui/index.md) — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照（295 条）

## 阶段

- [spec](by-stage/spec.md) — 规格提取（216 条）
- [plan](by-stage/plan.md) — 计划与派工（42 条）
- [execute](by-stage/execute.md) — 执行与实现（548 条）
- [verify](by-stage/verify.md) — 验证与判读（42 条）
- [repair](by-stage/repair.md) — 修复（97 条）
- [converge](by-stage/converge.md) — 收敛与移交（29 条）

## 阅读约定

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。 来源计数按卡片、迁移身份与项目标识去重，表示历史样本覆盖，不是正确概率或成功复用次数；适用条件优先。

可选检查仅在适用条件不确定、与当前输入冲突或需要验证关键假设时按需执行；优先复用已有证据和正常测试。
不因读取经验而额外启动验证流程；项目原有必需测试照常执行。
