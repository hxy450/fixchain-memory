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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；Share Kit 声明在 SDK 的 hms/ets 下；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕module.json5 的 skills 标识 UIAbility 或 ExtensionAbility 能够接收的 Want 的特征，字段 actions、entities、uris、permissions、domainVerify；一个 skill 里不建议配置多个 action，也不建议配置多个 entity，否则可能无法匹配预期场景
- 〔原因〕隐式 Want 匹配：want 的 parameters 里 linkFeature 不为空时先按 linkFeature 匹配；否则 action、entities、uri、type 四项都与 skills 匹配通过，应用才会被应用选择器列出。action：want 带 action 而 skill 的 actions 为空或不含它则失败，want 不带 action 而 skill 的 actions 不为空则成功；entities：want 带的 entities 必须全部包含在 skill 的 entities 里，want 不带 entities 时成功；uris 数组里只要有一项与 want 的 uri 和 type 匹配即成功
- 〔原因 / 做法第 1 步〕鸿蒙系统分享面板按 skills uris 的 utd 选接收目标：分享接收入口的 sendData skill 不写 utd 与 maxFileSupported（只写 MIME type 如 */*）时，本应用不出现在系统分享面板里
- 〔做法第 1 步〕鸿蒙 action 字符串：ohos.want.action.search（启动页面搜索）、ohos.want.action.sendData（发送单个数据记录）、ohos.want.action.sendMultipleData（发送多个数据记录）、ohos.want.action.viewData（查看数据）。它们出自 @ohos.ability.wantConstant 的 Action 枚举（ACTION_SEARCH、ACTION_SEND_DATA、ACTION_SEND_MULTIPLE_DATA、ACTION_VIEW_DATA），这个模块 API 9 起废弃，新模块 @ohos.app.ability.wantConstant 的声明里没有 Action 枚举，module.json5 里直接写字符串；文档另说明系统会逐步废弃非必要的 action/entity
- 〔做法第 1、2 步〕安卓 action 与 extra 字符串：ACTION_SEARCH = "android.intent.action.SEARCH"（查询串在 SearchManager.QUERY = "query"）、ACTION_VIEW = "android.intent.action.VIEW"、ACTION_SEND = "android.intent.action.SEND"、ACTION_SEND_MULTIPLE = "android.intent.action.SEND_MULTIPLE"、ACTION_PROCESS_TEXT = "android.intent.action.PROCESS_TEXT"（文本在 EXTRA_PROCESS_TEXT = "android.intent.extra.PROCESS_TEXT"）。SEND 的数据在 EXTRA_TEXT（此时 MIME 应为 text/plain）或 EXTRA_STREAM，可选 EXTRA_SUBJECT 等；SEND_MULTIPLE 用 get*ArrayListExtra 取 EXTRA_TEXT 或 EXTRA_STREAM 的列表，各项类型可以混合，intent 的 type 写最具体的 MIME，混合时退到 <主类型>/*（如 image/jpg 与 image/png 混发为 image/*）或 */*
- 〔做法第 1 步〕skills.uris 的每一项可写 scheme、host、port、path | pathStartWith | pathRegex、type、utd、maxFileSupported、linkFeature；type 用 MIME 或 UTD 规范；utd 是与 Want 相匹配的标准化数据类型，适用于分享等场景；maxFileSupported 是对指定类型的文件一次能接收或打开的最大数量，需与 utd 配合，缺省 0；scheme 只在这一项仅配置 type 时可缺省，API 18 起 scheme、host 匹配不区分大小写。编译期校验（toolchains/modulecheck/module.json）对 uris 每一项的要求：要么带 scheme（其余字段取上面那些），要么只有 type 一个字段
- 〔做法第 1 步〕uniformTypeDescriptor（从 @kit.ArkData 导入）的 UniformDataType：OBJECT = 'general.object'（所有表示逻辑内容类型的基类型）、TEXT = 'general.text'、PLAIN_TEXT = 'general.plain-text'、HYPERLINK = 'general.hyperlink'、IMAGE = 'general.image'、JPEG = 'general.jpeg'、PNG = 'general.png'、FILE = 'general.file'；UTD 预置列表里 general.plain-text 对应 MIME text/plain，general.object、general.text、general.image 是基类型，没有对应的 MIME
- 〔做法第 2 步〕安卓分享 extra 键的字符串：EXTRA_SUBJECT = "android.intent.extra.SUBJECT"、EXTRA_TEXT = "android.intent.extra.TEXT"、EXTRA_STREAM = "android.intent.extra.STREAM"
- 〔做法第 2 步〕wantConstant（从 @kit.AbilityKit 导入）的 Params：CONTENT_TITLE_KEY = 'ohos.extra.param.key.contentTitle'、SHARE_ABSTRACT_KEY = 'ohos.extra.param.key.shareAbstract'、SHARE_URL_KEY = 'ohos.extra.param.key.shareUrl'（首段 @since 10）。Want.parameters 的声明注释把这三个键列在「由系统赋值、手动设置不生效」的一组里，说明为原子化服务可分享的标题、内容和 URL；同一注释里 ability.params.stream 是调用方赋值、要授权给目标 Ability 的文件 URI 数组（string）
- 〔做法第 2 步〕Want.parameters?: Record<string, Object>（首段 @since 9）：外部拉起时携带的参数，按键名取，值的类型要自己判断；值只能是 String、Number、Boolean、Object、undefined、null，对象里的函数不会传递；WantParams 最多传 200KB
- 〔做法第 2 步〕systemShare（从 @kit.ShareKit 导入，HarmonyOS 能力，声明在 SDK 的 hms 下）：getSharedData(want: Want): Promise<SharedData>（@since 4.1.0(11)）从拉起分享接收 Ability 的 want 里解析分享数据，解析失败抛 1003703001；SharedData.getRecords(): Array<SharedRecord>；SharedRecord 有 utd: string、content?: string（文本、HTML 文本、URL 等）、uri?: string、title?: string、description?: string
- 〔做法第 3 步〕cameraPicker.pick(context: Context, mediaTypes: Array<PickerMediaType>, pickerProfile: PickerProfile): Promise<PickerResult>（首段 @since 11，cameraPicker 从 @kit.CameraKit 导入）拉起系统相机拍照或录像；它的声明和文档都没有要求调用方在 module.json5 的 skills 里声明 entity 或 action
- 〔做法第 3 步〕module.json5 的 skills 里声明 entity.system.camera 与 ohos.want.action.camera 的应用，会被列为拍照类隐式 Want 的候选应用
