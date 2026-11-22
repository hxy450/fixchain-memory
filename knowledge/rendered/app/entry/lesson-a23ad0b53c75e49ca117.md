# intent-filter 逐条映射为 module.json5 skills：有对应 action 的不合并，载荷键不自造，源端没有的不加

## 何时使用

规格提取阶段把 AndroidManifest 的 intent-filter 与入口 Intent 载荷翻成 module.json5 skills 与 Want 参数契约时；接线阶段按笔记或 skill 参考给出的片段修改 skills 时；集成阶段在入口 Ability 实现外部 Want 的参数解析时

## 适用情境

源 Activity 声明多条 intent-filter（SEARCH、VIEW 自定义 scheme、SEND/SEND_MULTIPLE */*、PROCESS_TEXT 等），入口分发读取 Intent.EXTRA_* 键，并可能在初始化或验密门之后才处理 Intent；目标为 UIAbility 的 module.json5 skills（actions、entities、uris，分享目标需 utd 与 maxFileSupported）与 Want parameters、systemShare 载荷；skill 参考或交接笔记可能给出“调用某系统能力须声明某 skill”的片段。源端 MAIN/LAUNCHER 对应的入口 skill（ohos.want.action.home 加 entity.system.home）留在入口 Ability 上，不在“源端没有的不加”之列。也包括集成者在入口 Ability 解析第三方拉起 Want 的 extras：多个键表达同一选项、源端按固定顺序短路判定，且取值限定在少数几个值。源端某条 intent-filter 的 action 在鸿蒙没有对应值（如 PROCESS_TEXT）时，不自造 ohos.want.action.* 字符串当作已映射（skills 的 actions 收任意字符串，写错也不报错），在规格里写明鸿蒙没有对应入口。

## 原因

skills 是本应用受理外部 Want 的过滤器：合并或漏登的 intent-filter，其入口不会被系统匹配（分享面板不出现本应用、搜索与多文件分享收不到）；多加的 skill 会让应用成为无关能力（如系统相机）的候选。自造的载荷键与外部调用方实际写入的键对不上，入口能拉起却读不到内容。

## 做法

1. 逐条列出 intent-filter，每条给一项 skill：action 映射到平台对应的 ohos.want.action.*（如 SEARCH → search，SEND → sendData，SEND_MULTIPLE → sendMultipleData，VIEW → viewData），data 映射为 uris（scheme/host/path，分享目标写 utd 与 maxFileSupported）；有对应 action 的不并入他条，也不改由应用内组件承接。
2. 载荷契约并列写出两侧：源端读取的 Intent.EXTRA_* 字符串值（如 android.intent.extra.SUBJECT）与目标标准键或接口（wantConstant.Params.CONTENT_TITLE_KEY、SHARE_ABSTRACT_KEY，系统分享用 systemShare.getSharedData）；查不到出处的键写为未知并说明影响，不写成契约。接线实现解析时，按源端读取代码逐键落实键名、值类型、取值域与判定先后（多个键表达同一选项时的短路顺序）；拿不准的键先查源码或规格原文，不凭记忆补键或别名。
3. 只为源 manifest 里有对应 intent-filter 的入口写 skill；参考文档或笔记要求“调用某系统能力须声明某 entity/action”（如拉起系统相机）时，先用 SDK d.ts 或官方文档复核，调用系统能力不需要本应用声明受理同类 Want。
4. 入口分发照抄源端前置条件：源端在初始化或验密门受理之后才处理 Intent 的，目标把落库、分享保存等动作放在同一道门之后，不在 EntryAbility 冷启分发里直接执行。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、3 步〕module.json5 的 skills 标签标识 UIAbility 或 ExtensionAbility 能够接收的 Want 特征（actions、entities、uris、permissions 等），不写时为空；它描述的是本组件受理哪些隐式 Want
- 〔做法第 1 步〕一个 skill 中不建议配置多个 action 或多个 entity，文档说明这样可能导致无法匹配预期场景
- 〔做法第 1 步〕常用 action 的字符串：ohos.want.action.search（启动页面搜索）、ohos.want.action.sendData（发送单个数据记录）、ohos.want.action.sendMultipleData（发送多个数据记录）、ohos.want.action.viewData（查看数据）；skills 的 actions 允许自定义值，写错的字符串不会被当作非法值
- 〔做法第 1 步〕uris 中 utd 不写时为空；maxFileSupported 不写时为 0，表示对指定类型的文件一次能接收或打开的最大数量，需与 utd 配合，适用于分享等场景；uris 的字符串标签不支持 $string 资源引用
- 〔做法第 1 步〕uris 的 host 只在配置了 scheme 时生效；port 和 path、pathStartWith、pathRegex 只在 scheme 与 host 都配置时生效；path 全匹配、pathStartWith 前缀匹配、pathRegex 正则匹配，三者只能选一
- 〔做法第 1 步〕uris 的 scheme、host 从 API 18 起参与隐式 Want 匹配时不区分大小写；安卓 IntentFilter 的 scheme、authority、MIME type 匹配区分大小写
- 〔做法第 1 步〕安卓 Intent.ACTION_PROCESS_TEXT 的值是 android.intent.action.PROCESS_TEXT，所选文本放在 EXTRA_PROCESS_TEXT；@ohos.ability.wantConstant 的 Action 表里没有与之对应的 action
- 〔做法第 2 步〕安卓分享键的字符串值：Intent.EXTRA_SUBJECT 为 android.intent.extra.SUBJECT，EXTRA_TEXT 为 android.intent.extra.TEXT，EXTRA_STREAM 为 android.intent.extra.STREAM；ACTION_SEND 时 EXTRA_STREAM 是一个 content: URI，ACTION_SEND_MULTIPLE 时 EXTRA_TEXT 或 EXTRA_STREAM 以 ArrayList 携带（用 get*ArrayListExtra 读）
- 〔做法第 2 步〕wantConstant.Params 的 CONTENT_TITLE_KEY（ohos.extra.param.key.contentTitle）、SHARE_ABSTRACT_KEY（ohos.extra.param.key.shareAbstract）、SHARE_URL_KEY（ohos.extra.param.key.shareUrl）在文档中定义为原子化服务分享的标题、摘要和 URL，由开发者在跨端分享的 UIAbility.onShare 回调里设置
- 〔做法第 2 步〕systemShare.getSharedData(want) 从分享拉起本应用的 Want 解析出 SharedData，解析失败抛 1003703001；getRecords() 返回的每条 SharedRecord 带 utd（数据类型），content 放不需授权的文本、HTML 文本、URL 等，uri 放记录的 uri
