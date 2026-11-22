# 经验后面挂的「已核实的平台事实」（试验分支 `memory/shadow-v7-20261121`）

## 这个分支相对 main 改了什么

派生自 main `369bbbf3`（store `e797fb15`，active 651 条、retired 1 条）。相对 main：

1. **store**：照维护流程写提案、apply（共 4 次：建分支时一次，之后每并入一批带正文改动的知识一次，见「并入记录」），store 版本 `e797fb15` → `b5e76f80`（`b5e76f80d2a1cfb41787446f87371b13468e8f60afdd1284387f548f33ac452b`）。
   - 退役 4 条通用审查式经验（没有具体触发情景，要求把某一类东西全部核一遍或交付前做通用动作）：`lesson-6e558834938be19c04e2`、`lesson-25bc0b7518d335a947d6`、`lesson-42df1ac4d4030421da34`、`lesson-0c9e222422d81871b464`；理由写在 store 快照的 `retirement_reason` 里。
   - 45 条经验按本目录知识文件里核实过的 `changes` 改正文（共 104 处），版本各 +1；`evidence`、`requires`、`topic`、`status` 原样。
   - 现在 active 647 条、retired 5 条（其中 1 条在 main 上就已退役）。
2. **memory/**：从新 store 用维护脚本重新导出（开发版，带卡片链接，`--link-cards`），通过发布脚本用的严格校验（manifest 的版本等于 store HEAD、每个文件 sha256 对得上、没有多余文件）；`MEMORY.md` 的发布版本行同步改了。和 main 比：4 个退役经验的文件没了，45 个经验文件和 18 个索引 / manifest 文件变了，其余经验文件逐字节相同。
3. **新增两个目录**：`knowledge/`（本目录）和 `shadow/`（定向核对版影子的提示词和用法）；`.gitignore` 放行这两个目录。仓库根 `README.md` 没改。

## 并入记录

建分支之后每并入一批知识文件记一行：知识文件拷进 `lessons/`；有改句的经提案 apply 进 store、从新 store 重新导出 `memory/`（严格校验）；重新渲染；一批一个提交。

| 批 | 日期 | 经验（id 前 8 位） | 条目 | 正文改动 | store | 知识的规则和复核 |
|---:|---|---|---:|---|---|---|
| 1 | 2026-11-21 | 9 条：`2fcb6612`、`4f81eeea`、`7083c6ad`、`92aee54a`、`99080bd3`、`bc5b8558`、`c8e645a5`、`cf111aad`、`eb4de4fd` | 37 | 7 处、5 条经验：`7083c6ad` 3、`92aee54a` 1、`99080bd3` 1、`bc5b8558` 1、`c8e645a5` 1 | `7312cbfe` → `09bd22c2` | 第七版规则，写完后经另一个人逐条独立复核 |
| 2 | 2026-11-21 | 24 条：`08e71bb7`、`1696967d`、`18d9c9a3`、`29744eb6`、`3f3e1ff0`、`4567f9f7`、`4a4f8d84`、`4d0f0176`、`55f44e2e`、`776ed5eb`、`8a881c2e`、`8b145360`、`8d297954`、`9147be4d`、`943544ce`、`b58df29f`、`c4af68b3`、`d80ced7b`、`d9143de0`、`dcb3c5e6`、`ea965b7b`、`f6b95d7d`、`f80ae7c3`、`f88b9c82` | 86 | 9 处、5 条经验：`18d9c9a3` 1、`4a4f8d84` 2、`943544ce` 3、`b58df29f` 1、`f88b9c82` 2 | `09bd22c2` → `1e791453` | 第七版规则，写完后经另一个人逐条独立复核 |
| 3 | 2026-11-21 | 24 条：`0a26e0cf`、`19dd006e`、`1e972af4`、`31ab9f59`、`39d1dee4`、`6d6ba721`、`6dae0bf2`、`783faf27`、`824031d5`、`8390913d`、`8953e390`、`8e0e9fe5`、`94a3f7a5`、`a58ebfe7`、`a6ed8a9c`、`ad6f23b8`、`ae093ded`、`b1916207`、`c1968bdf`、`c4a6eaaf`、`cf018b76`、`dbfae443`、`fb996956`、`feec63f6` | 72 | 21 处、12 条经验：`0a26e0cf` 2、`19dd006e` 2、`6d6ba721` 2、`824031d5` 2、`8953e390` 1、`8e0e9fe5` 1、`a58ebfe7` 3、`b1916207` 2、`c4a6eaaf` 2、`cf018b76` 1、`dbfae443` 1、`feec63f6` 2 | `1e791453` → `b5e76f80` | 第七版规则，写完后经另一个人逐条独立复核 |

## 是什么

每条经验后面挂几条已经核实过的平台事实：默认值、单位、取值范围、调用时序、实际行为、两个平台的差异、安卓框架和依赖库的默认外观和行为。交给模型时接在经验正文后面（写法见下面「怎么渲染」），模型照着经验去写或去核代码时直接用，不再自己查。事实和具体应用无关；其中的默认值只在应用自己没有另设时成立。

知识文件里的 `changes` 是对经验正文某句的改动（核到的事实和正文对不上、或缺条件时）；本分支已经把它们经提案发布进 store 和 `memory/`，交出去的正文只有一个说法。

## 目录

| 路径 | 内容 |
|---|---|
| `lessons/lesson-<id>.json` | 每条经验的知识源文件（格式见下） |
| `rendered/<主题>/lesson-<id>.md` | 渲染好的样子（交给模型的那一段），给人看；由 `render.py` 生成 |
| `render.py` | 把 `memory/` 里的正文和知识文件渲染成交给模型的那一段 |
| `check.py` | 检查知识文件（字段、条数、本机路径、应用名、改句是否已在正文里） |
| `RULES.md` | 配知识的规则（第七版） |

## 格式

现在有两种格式：旧格式（下面前两种，第三版和第七版规则的文件，`sdk` 只记 `harmony`、`android`）和 2026-11-21 起的新格式（第三种）。还没有经验换成新格式，106 个知识文件都是旧格式。

共同：`sdk` 是核实时用的版本（`harmony`、`android` 两个键；新格式另有三个键）；`changes` 每项有 `where`（正文哪一部分）、`before`（原句）、`after`（新句）、`basis`（依据）、`type`（改动类别）；`entries` 是平台事实；`device_todo` 是要上机才能定的事项，只留给维护的人；`dropped_notes` 是配的人删掉的条数。交给模型的只有正文（已含改句）和条目的 `step`、`fact`、`scope`；`source`、`code`、`origin`、`basis`、`device_todo` 不交。

- **第三版规则的格式（27 个文件）**：顶层 `id`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`（个别有 `note`）。条目栏 `step`、`fact`、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证）、`origin`，个别带 `code`；**没有 `scope`**，条数比第七版多（共 319 条，一条经验最多 29 条）。
- **第七版规则的格式（79 个文件）**：顶层 `lesson`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`、`note`。条目栏 `step`、`fact`、`scope`（成立范围：对什么成立、什么条件下成立、最常见的不成立情形）、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库）、`origin`，可选 `code`；每条经验最多 6 条（共 319 条）。规则见 `RULES.md`。
- **新格式（2026-11-21 起，0 个文件）**：和第三版同一种结构（顶层 `id`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`，没有条目时有 `note`），`sdk` 另记 `verified_on`（核实日期）、`docs_commit`、`docs_date`（核实时用的 OpenHarmony 文档 master 的提交和日期）。条目栏 `step`、`fact`、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证）、`origin`；没有 `scope`，条数不设上限（共 0 条）。渲染时段头在鸿蒙 SDK 版本后面多写文档 master 的日期和提交，条目不带成立范围。

## 覆盖

106 个知识文件。其中 4 个对应本分支退役的经验（文件原样留着，不渲染，它们的 8 处改句没有套）；其余 **102 / 647 条 active 经验**有知识文件（第三版 23 条、第七版 79 条），其中 93 条有条目（`29744eb6`、`447ba581`、`4f81eeea`、`6dae0bf2`、`776ed5eb`、`8390913d`、`9147be4d`、`c1968bdf`、`eb4de4fd` 是流程类经验，没有可挂的条目）。其余 active 经验还没有知识。

| id | 主题 | 规则 | 条目（带成立范围） | 改句（已进正文） | 标题 |
|---|---|---|---:|---:|---|
| `lesson-2fcb6612ee4106b34e17` | app/base-page | 第七版 | 5（5） | 0 | Android 业务基类的横切行为逐方法映射到组合式 BasePag… |
| `lesson-51651155ed8226212e55` | app/entry | 第七版 | 6（6） | 0 | 源 Activity 的 SEND 分享接收入口（standard … |
| `lesson-8a881c2e07f80f83447c` | app/entry | 第七版 | 4（4） | 0 | 源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封… |
| `lesson-94715d0df4c03a8fb5a5` | app/entry | 第三版 | 16（0） | 6（是） | 源 Activity 未声明 configChanges 时，旋转（… |
| `lesson-a23ad0b53c75e49ca117` | app/entry | 第七版 | 6（6） | 0 | intent-filter 逐条映射为 module.json5 s… |
| `lesson-dcb3c5e66dec2d126234` | app/entry | 第七版 | 4（4） | 0 | 源端在入口 onCreate 首帧前按偏好设主题时，目标在 Entr… |
| `lesson-ea965b7baf2488be23cd` | app/entry | 第七版 | 3（3） | 0 | 裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无… |
| `lesson-55f44e2efdc1a49ac387` | app/identity | 第七版 | 3（3） | 0 | 落地应用显示名时同时改 AppScope 的 app_name 与入… |
| `lesson-a6ed8a9c6017ddb73beb` | app/identity | 第七版 | 1（1） | 0 | 源端 BuildConfig.VERSION_NAME/VERSIO… |
| `lesson-c4af68b3ee1456525e8e` | app/identity | 第七版 | 6（6） | 0 | 启动窗按源端实际启动画面映射：未自定义 SplashScreen 时… |
| `lesson-fb996956b33a1ba65861` | app/identity | 第七版 | 2（2） | 0 | 沿用脚手架 bundleName/vendor 前核对所引部署期决策… |
| `lesson-feec63f65102f5396e51` | app/identity | 第七版 | 3（3） | 2（是） | 应用级图标只认 app.json5 里写的引用，AppScope 同… |
| `lesson-11e9d15d947b30d2ce7e` | app/logging | 第三版 | 4（0） | 0 | 新增错误日志沿用工程的 hilog 约定，不写 console.* |
| `lesson-a4ee90eabe3eef99ddbe` | app/nfc | 第七版 | 5（5） | 0 | Android Activity 级 NFC 前台派发迁到 Harm… |
| `lesson-652974ce64a9243faebc` | app/platform | 第七版 | 6（6） | 1（是） | 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的… |
| `lesson-ea9a6cfecca9e091c7ea` | app/platform | 第七版 | 5（5） | 0 | 源端 Activity 对自身 getWindow() 加的标志（F… |
| `lesson-783faf2767a952034514` | app/resources | 第七版 | 3（3） | 0 | 8 位颜色保持 #AARRGGBB 字节序，转换后与源逐项往返核对 |
| `lesson-94a3f7a5ec5ad8f8a3e8` | app/resources | 第七版 | 3（3） | 0 | values 批量转 element JSON 按目标格式出口：颜色… |
| `lesson-f88b9c824280ce239dea` | app/resources | 第七版 | 5（5） | 2（是） | strings.xml 转 string.json 按 aapt2 … |
| `lesson-4d0f0176b3d09c33f1eb` | app/settings | 第七版 | 6（6） | 0 | 迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只… |
| `lesson-9fa98065e5de983b7c01` | app/settings | 第七版 | 5（5） | 0 | SharedPreferences 迁移保留同步时序：onCreat… |
| `lesson-843a70afd7e08bfed97c` | arkts/async | 第三版 | 7（0） | 0 | 异步初始化里，用户可编辑的输入状态在第一个 await 之前写入初值… |
| `lesson-b19162077a2ab886d809` | arkts/async | 第七版 | 4（4） | 2（是） | Kit API 的 catch 值按 BusinessError 取… |
| `lesson-b1991f633e5307abdc4d` | arkts/async | 第三版 | 7（0） | 0 | 源端阻塞到完成才返回的 void 方法（排空队列、关闭设备、停录）改… |
| `lesson-8b145360b447a10d52ef` | arkts/decorators | 第七版 | 5（5） | 0 | V2 组件成员装饰器裸写（@Local/@Param/@Once/@… |
| `lesson-c1968bdf112ed3e6b259` | arkts/decorators | 第七版 | 0（0） | 0 | 自定义组件的成员不与组件通用属性方法同名（position、widt… |
| `lesson-0cbafc2ad4096001d0e8` | arkts/stdlib | 第七版 | 6（6） | 0 | Java/ICU 正则、String/List 方法与 Androi… |
| `lesson-237091b9b04bc4cd340b` | arkts/stdlib | 第七版 | 6（6） | 1（是） | Java 文本读行、split/trim、BOM、String.fo… |
| `lesson-ae093dedda604fddf17e` | arkts/stdlib | 第七版 | 6（6） | 0 | DecimalFormat、BigDecimal 舍入与 Float… |
| `lesson-1696967d1320c7735732` | arkts/strict-mode | 第七版 | 2（2） | 0 | ArkTS 里给对象字面量写显式 class/interface 类… |
| `lesson-dbfae443e671c568e14e` | arkts/strict-mode | 第七版 | 2（2） | 1（是） | catch 中继续抛出时先把异常收窄为 Error，不直接 thro… |
| `lesson-f80ae7c3747420ef16f7` | arkts/strict-mode | 第七版 | 4（4） | 0 | 静态字段初始化器或模块级常量里把类当值使用时，该类要声明在使用者之前… |
| `lesson-08e71bb72d05b1d79d28` | arkts/ui-syntax | 第七版 | 2（2） | 0 | build() 与 @Builder 里每个组件、条件与循环渲染各占… |
| `lesson-18d9c9a34c1952f43f53` | arkts/ui-syntax | 第七版 | 5（5） | 1（是） | justifyContent/alignItems 只属于 Colu… |
| `lesson-39d1dee415d4a252fc5c` | arkts/ui-syntax | 第七版 | 2（2） | 0 | stateStyles 各状态只写 @Styles 方法引用、全局 … |
| `lesson-ff5e8fbfb9ed491d99ee` | data/files | 第七版 | 6（6） | 0 | 源端在后台线程执行的文件拷贝与导入改用异步 IO 或 taskpoo… |
| `lesson-29744eb694376e8acaca` | process/build | 第七版 | 0（0） | 0 | 编译修复只改报错定位的行与符号，不以删掉功能或语义不同的替代换取通过… |
| `lesson-6dae0bf2657b0e339742` | process/build | 第七版 | 0（0） | 0 | 用 shell 一行命令或脚本改写含 $ 或反斜杠转义的 ArkTS… |
| `lesson-776ed5eb216833c6b002` | process/gates | 第七版 | 0（0） | 0 | 写文件以真实执行回执为准：只有文本形式的工具调用即未写入；覆盖模板入… |
| `lesson-8390913de64b0adc00fc` | process/gates | 第七版 | 0（0） | 0 | 处理孤儿检测报出的无调用方页面或弹窗时，已登记为范围内的产物不删除：… |
| `lesson-9147be4d87153de9c5b6` | process/gates | 第七版 | 0（0） | 0 | 功能对齐与验收结论逐项以代码落点为准：按规格验收项与导航出口检索实际… |
| `lesson-ad6f23b88f09b55dd92a` | process/gates | 第七版 | 2（2） | 0 | 用共享组件替换页面已实现片段前（关闭孤儿组件检查或按计划收口），完整… |
| `lesson-f6b95d7d6d0159cb0436` | process/gates | 第七版 | 2（2） | 0 | 修复安全区等按关键字判定的结构检查时逐页落实实现，不用含检查关键字的… |
| `lesson-447ba5818e4e203272e8` | process/task-handoff | 第三版 | 0（0） | 0 | 页面先于共享组件或共享工具实现时，页内等价实现登记为待收敛项；共享件… |
| `lesson-4f81eeea17b94190c2de` | process/task-handoff | 第七版 | 0（0） | 0 | 要靠其他文件或任务补实现的功能，登记成带负责方、验证方式和源端确定值… |
| `lesson-a2f6a4ae9a72be740de6` | process/task-handoff | 第三版 | 8（0） | 0 | “不确定”“待补资源”“无等价”“延期”“契约未确认”这类占位只登记… |
| `lesson-eb4de4fd7452308a0483` | process/task-handoff | 第七版 | 0（0） | 0 | 解决前向占位时按登记的触发文本逐项兑现：只接一半、写成常量或删掉标记… |
| `lesson-d80ced7be82765244889` | ui/accessibility | 第七版 | 4（4） | 0 | 图标无障碍文本按源 contentDescription 转写：nu… |
| `lesson-6d6ba721c81206d45fbe` | ui/animation | 第七版 | 6（6） | 2（是） | 帧时钟动画（Animatable、ValueAnimator）改自驱… |
| `lesson-0a26e0cfc44a183d3a02` | ui/dialog | 第七版 | 5（5） | 2（是） | 用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的… |
| `lesson-368c4592e4c7075c1871` | ui/dialog | 第七版 | 5（5） | 0 | 源端 XPopup/DialogFragment 真弹窗（居中、锚点… |
| `lesson-3f3e1ff0a4d0e0299bda` | ui/dialog | 第七版 | 6（6） | 0 | @ComponentV2 页面的弹窗不用 CustomDialogC… |
| `lesson-9c4de55af3c1ecd8eaa4` | ui/dialog/appearance | 第七版 | 6（6） | 3（是） | 只靠平台默认外观的 AlertDialog（含 DialogPref… |
| `lesson-1a66114fb7523a1f9af1` | ui/effects | 第三版 | 13（0） | 3（是） | 位图着色（ColorFilter.tint、setColorFilt… |
| `lesson-8335bc404934f58c6f31` | ui/feedback | 第七版 | 5（5） | 1（是） | 公共 Toast 封装把时长做成每次调用的参数，逐调用点映射源端 L… |
| `lesson-7708f650eb4b55dce045` | ui/graphics | 第三版 | 11（0） | 2（是） | android:background 的整屏背景位图按拉伸铺满映射，… |
| `lesson-943544ce27bf04f9faf8` | ui/graphics | 第七版 | 6（6） | 3（是） | 图标按源端原始资源落实：缺失时从 Android 密度目录、SDK … |
| `lesson-bdc493f5950835f9bfcc` | ui/graphics | 第三版 | 27（0） | 1（是） | 图标按资源固有 dp 显示、触摸盒放在外层：centerInside… |
| `lesson-4da9eabca745b3b2be91` | ui/graphics/canvas | 第三版 | 13（0） | 0 | SurfaceView 自建线程的 lockCanvas 循环按线程… |
| `lesson-7083c6ad69ab19ad17dd` | ui/graphics/canvas | 第七版 | 6（6） | 3（是） | 按 Android px 公式移植自绘 View 时先定画布上下文单… |
| `lesson-c3bd9c8b2f24c209a659` | ui/graphics/canvas | 第三版 | 11（0） | 1（是） | 源端位图按密度解码、createScaledBitmap 预缩放后原… |
| `lesson-1150c0c721e6dc0dede4` | ui/input | 第七版 | 6（6） | 0 | 按 EditText 对齐 TextInput 时，未声明 back… |
| `lesson-edc9465d3902807c386b` | ui/input | 第七版 | 6（6） | 1（是） | 菜单 SearchView 迁成自绘搜索栏时把展开、焦点、提交、收起… |
| `lesson-4a4f8d845a204ffa244b` | ui/interaction | 第七版 | 6（6） | 2（是） | Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆… |
| `lesson-68023ac5f088c72a775a` | ui/interaction | 第三版 | 14（0） | 3（是） | 源端 onTouch 自己按未掩码 getAction 只跟随首指时… |
| `lesson-7389433391eddbaea827` | ui/interaction | 第三版 | 7（0） | 1（是） | Image 承载点击/长按按钮或自绘拖拽柄时设 draggable(… |
| `lesson-99080bd3bfc1bcbb9c5f` | ui/interaction | 第七版 | 5（5） | 1（是） | 源端禁用态只靠代码换背景、文字色固定时，不用 ArkUI .enab… |
| `lesson-cf018b76af68b4c00895` | ui/interaction | 第七版 | 4（4） | 1（是） | 弹窗防穿透的 Block 只放在无子控件的遮罩层，内容面板与根容器保… |
| `lesson-fde79829831c2269e925` | ui/interaction | 第七版 | 6（6） | 0 | 源端可点击容器自带的按压反馈（Compose clickable、C… |
| `lesson-51bf52bc666b921ef2e9` | ui/layout | 第三版 | 7（0） | 1（是） | values-sw<N>dp(-land) 覆盖按设备屏幕短边 mi… |
| `lesson-786a04847bf10d364d9d` | ui/layout | 第七版 | 6（6） | 1（是） | 源应用声明 supportsRtl=true 时保留逻辑方向：sta… |
| `lesson-c8e645a542254d96997e` | ui/layout | 第七版 | 5（5） | 1（是） | 源布局（含 include 引入的布局）有 layout-land、… |
| `lesson-08b9064f678f1635e647` | ui/layout/constraints | 第三版 | 18（0） | 3（是） | 源端默认起始对齐和贴顶要显式写出：Android 与 Compose… |
| `lesson-92aee54a305ea0bde363` | ui/layout/constraints | 第七版 | 6（6） | 1（是） | Stack 中内容尺寸的子项按 alignContent 定位：子项… |
| `lesson-80dd4e626e1c207028e6` | ui/layout/scrolling | 第三版 | 17（0） | 7（是） | ScrollView 未写 overScrollMode、Compo… |
| `lesson-0ef2cd00e1a91491b350` | ui/layout/sizing | 第三版 | 11（0） | 4（是） | 源端在整数 px 上取整的布局公式：规格写明运算域，实现在 px 域… |
| `lesson-a58ebfe7a4c55b041b14` | ui/layout/sizing | 第七版 | 6（6） | 3（是） | 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_… |
| `lesson-396d54479492828eeea3` | ui/navigation/back-stack | 第七版 | 5（5） | 0 | 源端对话框、底部弹层或下拉菜单改成页内覆盖层后，在宿主 onBack… |
| `lesson-803ba029eea852122e77` | ui/navigation/back-stack | 第三版 | 7（0） | 0 | 被 @Entry 页直接组合、未进入 Navigation 栈的子组… |
| `lesson-efff93743d668b55b55a` | ui/navigation/back-stack | 第七版 | 6（6） | 0 | 唯一页面被压在空的 Navigation 首页之上时，由栈底 Nav… |
| `lesson-19dd006e049c3f9d7563` | ui/navigation/hosts | 第七版 | 2（2） | 2（是） | 源端在导航目的地内用 LocalLifecycleOwner 观察 … |
| `lesson-8953e390416a80d7dd8c` | ui/navigation/hosts | 第七版 | 4（4） | 1（是） | 入口页 Navigation 宿主：NavDestination 首… |
| `lesson-c4a6eaaf6a22c0b8823f` | ui/navigation/hosts | 第七版 | 3（3） | 2（是） | main_pages.json 只登记经 router 进入或由 l… |
| `lesson-0e1c846868f2683cc280` | ui/safearea | 第三版 | 29（0） | 14（是） | 仅当源窗口内容延伸到系统栏下，或窗口背景是按窗口尺寸拉伸或定位的位图… |
| `lesson-824031d5fddf81036b54` | ui/safearea | 第七版 | 3（3） | 2（是） | 系统栏图标深浅按源端浅色状态栏标志推导：未设标志时安卓图标为白色，不… |
| `lesson-8e0e9fe5373a2bbe47af` | ui/safearea | 第七版 | 5（5） | 1（是） | 页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入… |
| `lesson-a8452bfea5d42d3dcae3` | ui/safearea | 第三版 | 15（0） | 2（是） | 开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 n… |
| `lesson-cf111aadb8804649b578` | ui/safearea | 第七版 | 5（5） | 0 | getWindowAvoidArea 与 windowRect 的数… |
| `lesson-2e636699fa65aefd63f0` | ui/state | 第七版 | 6（6） | 0 | 列表条目以新对象替换或整表重建时，ForEach/Repeat 键要… |
| `lesson-8d2979542fa2cd65150c` | ui/state | 第七版 | 5（5） | 0 | 随状态变化的控件参数不作 @Builder 值参，改为内联读取状态或… |
| `lesson-b3bb0bc33f4caded78a2` | ui/state | 第七版 | 6（6） | 0 | 源页面在每次可见时、或由事件订阅与结果回调触发的重新加载，要迁成可见… |
| `lesson-d9143de006714935afe2` | ui/state | 第七版 | 4（4） | 0 | 源端 Activity 实例字段承载的会话态映射为页面实例作用域：服… |
| `lesson-22432022455bff6f849b` | ui/text | 第七版 | 4（4） | 1（是） | resourceManager 代码内取值（字符串、数组、复数、颜色… |
| `lesson-31ab9f59945e5f0259ea` | ui/text | 第七版 | 3（3） | 0 | Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 stri… |
| `lesson-4567f9f77f4280ec1747` | ui/text | 第七版 | 1（1） | 0 | 可见文案改为资源引用时值取自源端原文：目标字符串表缺键就新建专属键并… |
| `lesson-b58df29f032cc6a8c9d6` | ui/text | 第七版 | 3（3） | 1（是） | 字符串语言目录与键集按源端实际存在的 values-<语言>（含依赖… |
| `lesson-cce58a1538fedfda3695` | ui/text | 第三版 | 9（0） | 1（是） | 源端 textAllCaps（含 Material、AppCompa… |
| `lesson-1e972af4bc7e27b23d9c` | ui/theme | 第七版 | 3（3） | 0 | 追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追… |
| `lesson-47785524c7f132ea7efe` | ui/theme | 第三版 | 24（0） | 8（是） | 把主题、控件默认样式或依赖库隐式提供的外观写成目标显式样式：按“控件… |
| `lesson-4e9507a2a793c5583aa8` | ui/theme | 第三版 | 9（0） | 1（是） | 按源端实际色值与字号在资源里反查同值键：主题语义色、排版样式先解析到… |
| `lesson-5a82d62ff7e087616968` | ui/theme | 第七版 | 6（6） | 0 | 委托 Material/AppCompat 库或平台框架（Theme… |
| `lesson-bc5b8558ab086168b462` | ui/theme | 第七版 | 5（5） | 1（是） | 引用 style 或抽成共享 @Builder 的控件：先展开共享默… |

退役经验的知识文件（不渲染）：

| id | 主题 | 规则 | 条目（带成立范围） | 改句（已进正文） | 标题 |
|---|---|---|---:|---:|---|
| `lesson-6e558834938be19c04e2` | arkts/api-signatures | 第三版 | 19（0） | 5（否，经验已退役） | 写 SDK 调用前按本地 .d.ts 核对成员名、所属类型、调用链每… |
| `lesson-25bc0b7518d335a947d6` | process/build | 第三版 | 10（0） | 2（否，经验已退役） | 交付前要编译：项目根没有 hvigorw 时改用 DevEco 或命… |
| `lesson-42df1ac4d4030421da34` | process/input-loading | 第三版 | 0（0） | 0 | 写码前要读全必读 skill、规格、参考文档与源布局/源码：批量读取… |
| `lesson-0c9e222422d81871b464` | process/spec-handoff | 第三版 | 6（0） | 1（否，经验已退役） | 源码或布局引用的资源值（getColor/getDimension(… |

## 两版规则各做了哪些

- **第三版规则（早先那版，27 条）**：条目多（共 319 条）、没有 `scope`，kind 里有「卡里验证」；不是按 `RULES.md` 做的。文件：`08b9064f`、`0c9e2224`、`0e1c8468`、`0ef2cd00`、`11e9d15d`、`1a66114f`、`25bc0b75`、`42df1ac4`、`447ba581`、`47785524`、`4da9eabc`、`4e9507a2`、`51bf52bc`、`68023ac5`、`6e558834`、`73894333`、`7708f650`、`803ba029`、`80dd4e62`、`843a70af`、`94715d0d`、`a2f6a4ae`、`a8452bfe`、`b1991f63`、`bdc493f5`、`c3bd9c8b`、`cce58a15`。
- **第七版规则（79 条）**：按 `RULES.md` 做，每条事实写了成立范围；写完由另一个人逐条独立复核了成立范围（建分支时那批 22 个文件 124 条，复核改了约三成，多数是漏了例外；之后各批见「并入记录」）。文件：`08e71bb7`、`0a26e0cf`、`0cbafc2a`、`1150c0c7`、`1696967d`、`18d9c9a3`、`19dd006e`、`1e972af4`、`22432022`、`237091b9`、`29744eb6`、`2e636699`、`2fcb6612`、`31ab9f59`、`368c4592`、`396d5447`、`39d1dee4`、`3f3e1ff0`、`4567f9f7`、`4a4f8d84`、`4d0f0176`、`4f81eeea`、`51651155`、`55f44e2e`、`5a82d62f`、`652974ce`、`6d6ba721`、`6dae0bf2`、`7083c6ad`、`776ed5eb`、`783faf27`、`786a0484`、`824031d5`、`8335bc40`、`8390913d`、`8953e390`、`8a881c2e`、`8b145360`、`8d297954`、`8e0e9fe5`、`9147be4d`、`92aee54a`、`943544ce`、`94a3f7a5`、`99080bd3`、`9c4de55a`、`9fa98065`、`a23ad0b5`、`a4ee90ea`、`a58ebfe7`、`a6ed8a9c`、`ad6f23b8`、`ae093ded`、`b1916207`、`b3bb0bc3`、`b58df29f`、`bc5b8558`、`c1968bdf`、`c4a6eaaf`、`c4af68b3`、`c8e645a5`、`cf018b76`、`cf111aad`、`d80ced7b`、`d9143de0`、`dbfae443`、`dcb3c5e6`、`ea965b7b`、`ea9a6cfe`、`eb4de4fd`、`edc9465d`、`efff9374`、`f6b95d7d`、`f80ae7c3`、`f88b9c82`、`fb996956`、`fde79829`、`feec63f6`、`ff5e8fbf`。

核实时用的版本：鸿蒙 API 23（SDK 6.1.0.105）和 OpenHarmony 中文文档；安卓源码 android-36.1，平台资源 android-30 至 36；依赖库版本写在各文件的 `sdk` 和条目出处里。

## 怎么渲染

```
python knowledge/render.py                 # 渲染全部，写到 knowledge/rendered/（每次重写）
python knowledge/render.py lesson-<id>     # 一条打印到标准输出
python knowledge/render.py --check         # 只核对，不写
```

交给模型的那一段 = 经验正文（`memory/<主题>/lesson-<id>.lesson.md` 去掉 ID 行和「[本主题](index.md)」，截到「## 来源」之前，「来源支持：…」一行保留）；知识文件有条目时，空一行接「已核实的平台事实（核实时用的是 …；安卓 …。…）：」一段，每条「- 〔step〕fact」，有成立范围的再接「〔成立范围：scope〕」；不带出处和写法。和影子提示词生成器里的经验块是同一种写法：本分支建好后拿一套此前用 main 正文加这些知识文件生成的影子提示词核过，其中 27 条经验（32 个经验块，12 条的改句现在已在正文里）和 `render.py` 的输出逐字相同。

新格式的文件（`sdk` 里有 `docs_date` 或 `docs_commit`）知识段照写知识时用的渲染脚本：段头写成「核实时用的是 <harmony>；OpenHarmony 文档 master <docs_date>（提交 <docs_commit 前 8 位>）；安卓 …」，每条只有「- 〔step〕fact」，没有成立范围；同一个文件、同一份正文，和那个脚本的输出逐字节相同。旧格式的渲染不变。

知识文件里的改句：已在正文里的只核对；还没进正文的（新写的知识文件），原句在正文里恰好对上一处时当场套上并报出处数，对不上就报错。

## 怎么检查

```
python knowledge/check.py knowledge/lessons --legacy-ok [--app-name <留作评测的应用名> …]
python knowledge/check.py knowledge/lessons --only <id 前 8 位,…>     # 配知识的人查自己的（新格式，不加 --legacy-ok）
```

查：json 能解析、`lesson` 和文件名一致、经验在 `memory/` 里（store 里已退役的只列出）；条目六栏非空、kind 三选一、最多 6 条；source / fact / scope / code 没有本机路径和「文件:行号」；fact / scope 没有被迁移应用的名字（留作评测的应用名不写在仓库里，用 `--app-name` 传）；改句已在正文里（新句在、原句在新句之外不再出现），还没进正文的要能唯一定位。旧格式文件加 `--legacy-ok` 时，`id` 键、没有 scope、超过 6 条、kind「卡里验证」只列出。

新格式的文件（没有 `lesson` 键、`sdk` 里有 `verified_on` / `docs_commit` / `docs_date`）按写知识时的检查规则查，`--legacy-ok` 对它不起作用：顶层键齐全、`id` 和文件名一致；`sdk` 的核实日期、文档日期写成 YYYY-MM-DD，文档提交号是十六进制，`harmony` 写明 API 几；条目五栏非空，kind 四选一（含「卡里验证」）、origin 二选一、step 是正文的部分名，条数不设上限；卡里验证的事实不写返修怎么改，事实不带返修经过和做法建议的尾巴；文档出处写成文档仓库 master 的链接，网址只认一手来源，fact / after / note 里不放链接；没有本机路径、行号写法和应用名；改句已在正文里的同上，没进正文的按顺序要套得上。默认值缺「应用没有另设」一类限定、提到高于本机 SDK 的 API、新句提到设备或截图的只列出，给人看。出处和本机 SDK、文档的逐条核对不在这里做。

本分支的结果：106 个文件 0 处错误（加 `--legacy-ok`，只列出 111 处 = 旧格式 107 处 + 4 个退役经验）；第七版的 79 个文件不加 `--legacy-ok` 也是 0 处错误。

效果数据见 `shadow/README.md`。
