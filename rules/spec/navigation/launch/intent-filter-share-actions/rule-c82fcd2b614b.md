# 规格里的入口载荷键不自造：安卓 EXTRA_* 原键与鸿蒙标准键并列写，查不到来源的标未知

审的是：规格
触发（任一种）：
- 读到：源端入口分发读 Intent.EXTRA_SUBJECT / EXTRA_TEXT / EXTRA_STREAM；写错的样子：规格自造「参数映射表」把它们定为 params.subject / params.text / 文件 uri，没注明键的来源，也没列安卓原键和鸿蒙标准键
适用范围：规格提取阶段，写入口 Want 载荷契约（分享、外部调起）时
做法：
- 把安卓 EXTRA_* 字符串常量（android.intent.extra.SUBJECT / TEXT / STREAM）与鸿蒙标准键（wantConstant.Params.CONTENT_TITLE_KEY / SHARE_ABSTRACT_KEY、systemShare.getSharedData）并列写进契约
- 「参数键名映射表」每个键注明来源；查不到来源的键标未知，不定契
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- EXTRA_SUBJECT = "android.intent.extra.SUBJECT"；EXTRA_TEXT = "android.intent.extra.TEXT"；EXTRA_STREAM = "android.intent.extra.STREAM"：安卓原键的字符串（出处：android.content.Intent#EXTRA_SUBJECT、android.content.Intent#EXTRA_TEXT、android.content.Intent#EXTRA_STREAM）
- CONTENT_TITLE_KEY = 'ohos.extra.param.key.contentTitle'；SHARE_ABSTRACT_KEY = 'ohos.extra.param.key.shareAbstract'：鸿蒙 Want 参数的标准键（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.wantConstant.d.ts，wantConstant.Params）
- getSharedData(want: Want): Promise<SharedData>：从分享拉起的 Want 解析分享数据（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.systemShare.d.ts，systemShare.getSharedData）
来源：1 张卡，1 个应用
- case-7b71b27d8bbbbbd73267（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
