# intent-filter 逐条映射为 module.json5 skills：有对应 action 的不合并，载荷键不自造，源端没有的不加

## 何时使用

规格提取阶段把 AndroidManifest 的 intent-filter 与入口 Intent 载荷翻成 module.json5 skills 与 Want 参数契约时；接线阶段按笔记或 skill 参考给出的片段修改 skills 时；集成阶段在入口 Ability 实现外部 Want 的参数解析时

## 适用情境

源 Activity 声明多条 intent-filter（SEARCH、VIEW 自定义 scheme、SEND/SEND_MULTIPLE */*、PROCESS_TEXT 等），入口分发读取 Intent.EXTRA_* 键，并可能在初始化或验密门之后才处理 Intent；目标为 UIAbility 的 module.json5 skills（actions、entities、uris，分享目标需 utd 与 maxFileSupported）与 Want parameters、systemShare 载荷；skill 参考或交接笔记可能给出“调用某系统能力须声明某 skill”的片段。也包括集成者在入口 Ability 解析第三方拉起 Want 的 extras：多个键表达同一选项、源端按固定顺序短路判定，且取值限定在少数几个值。

## 原因

skills 是本应用受理外部 Want 的过滤器：合并或漏登的 intent-filter，其入口不会被系统匹配（分享面板不出现本应用、搜索与多文件分享收不到）；多加的 skill 会让应用成为无关能力（如系统相机）的候选。自造的载荷键与外部调用方实际写入的键对不上，入口能拉起却读不到内容。

## 做法

1. 逐条列出 intent-filter，每条给一项 skill：action 映射到平台对应的 ohos.want.action.*（如 SEARCH → search，SEND → sendData，SEND_MULTIPLE → sendMultipleData，VIEW → viewData），data 映射为 uris（scheme/host/path，分享目标写 utd 与 maxFileSupported）；有对应 action 的不并入他条，也不改由应用内组件承接。
2. 载荷契约并列写出两侧：源端读取的 Intent.EXTRA_* 字符串值（如 android.intent.extra.SUBJECT）与目标标准键或接口（wantConstant.Params.CONTENT_TITLE_KEY、SHARE_ABSTRACT_KEY，系统分享用 systemShare.getSharedData）；查不到出处的键写为未知并说明影响，不写成契约。接线实现解析时，按源端读取代码逐键落实键名、值类型、取值域与判定先后（多个键表达同一选项时的短路顺序）；拿不准的键先查源码或规格原文，不凭记忆补键或别名。
3. 只为源 manifest 里有对应 intent-filter 的入口写 skill；参考文档或笔记要求“调用某系统能力须声明某 entity/action”（如拉起系统相机）时，先用 SDK d.ts 或官方文档复核，调用系统能力不需要本应用声明受理同类 Want。
4. 入口分发照抄源端前置条件：源端在初始化或验密门受理之后才处理 Intent 的，目标把落库、分享保存等动作放在同一道门之后，不在 EntryAbility 冷启分发里直接执行。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕skill 的 uris 匹配规则：want 既无 uri 也无 type 时，只有 skill 的 uris 为空、或其中有 scheme 和 type 都为空的元素才匹配；want 带 uri 时，skill 的 uris 为空则匹配失败。因此把不带数据的入口（如搜索）并进带 uris 的分享 skill，不带 uri 的 want 会匹配失败。〔成立范围：对隐式 Want 的 uri / type 匹配（未配置 linkFeature 时）；从 API 18 起 scheme、host 参与匹配时不区分大小写；最常见的不成立情形：want 只带 type 时，要有一条 scheme 为空且 type 匹配的 uris 元素才匹配。〕
- 〔做法第 1 步〕module.json5 的 skills 文档写明一个 skill 中不建议配置多个 action 或多个 entity，否则可能导致无法匹配预期场景；actions、entities、uris 均可缺省（缺省为空），want 带 action 而 skill 的 actions 为空时 action 匹配失败。〔成立范围：对 abilities 的每一项 skill；最常见的不成立情形：want 不带 action 时，skill 的 actions 只要不为空就算 action 匹配成功。〕
- 〔做法第 3 步〕隐式 Want 匹配时，系统拿调用方传入的 want（action、entities、uri、type、parameters）去和已安装的待匹配应用组件的 skills 比对，调用方自己的 skills 不参与；所以拉起系统相机等能力不需要本应用声明同类 skill，而本应用多声明的 skill 会让它成为这类 Want 的候选。〔成立范围：对隐式 Want；显式 Want 按 bundleName、abilityName 匹配；最常见的不成立情形：want 的五个属性都没配置时隐式匹配直接失败。〕
- 〔做法第 1 步〕鸿蒙预定义 action 字符串：搜索 ohos.want.action.search，发送单条数据 ohos.want.action.sendData，发送多条数据 ohos.want.action.sendMultipleData，查看数据 ohos.want.action.viewData；skills.actions 里写的是普通字符串，写错不会编译报错。〔成立范围：取值来自 @ohos.ability.wantConstant 的 Action 枚举（该枚举自 API 9 标为废弃，文档仍以它作为 action 取值说明）；文档把 action/entity 方式标为不推荐、系统会逐步废弃非必要的 action/entity；最常见的不成立情形：写成安卓的 android.intent.action.* 或漏掉 ohos.want.action. 前缀，不会按该能力被匹配。〕
- 〔做法第 1 步〕两端对类别的要求不同：安卓 Intent 带的 categories 必须全部列在组件的 intent-filter 里，Activity 通常要声明 CATEGORY_DEFAULT 才能被 Context.startActivity 找到；鸿蒙 want 不带 entities 时，skill 的 entities 为空或不为空都匹配成功，want 带 entities 时才要求 skill 的 entities 全部包含。〔成立范围：对隐式拉起时的类别 / entities 匹配；最常见的不成立情形：调用方 want 带了 entities（如浏览器类别）而 skill 没声明，匹配失败。〕
- 〔做法第 2 步〕系统分享接收端用 systemShare.getSharedData(want) 取内容：每条 SharedRecord 带 utd，文本、HTML 文本、URL 在 content，文件在 uri，另有可选的 title、description；Want 参数标准键 wantConstant.Params.CONTENT_TITLE_KEY 的值是 ohos.extra.param.key.contentTitle（内容标题），SHARE_ABSTRACT_KEY 是 ohos.extra.param.key.shareAbstract（分享摘要）。〔成立范围：SharedRecord 取自 Share Kit（@hms.collaboration.systemShare）声明，Params 键取自 @ohos.app.ability.wantConstant 声明，声明里没有写它们与安卓 EXTRA_* 的对应关系；content 与 uri 的分工依据是声明注释（content 注释为无需授权的信息，举例文本、HTML 文本、URL；uri 注释只写「记录的 uri」，文件走 uri 是据此推断）；最常见的不成立情形：content、uri 都是可选字段，同一条记录可能只有其中之一。〕
