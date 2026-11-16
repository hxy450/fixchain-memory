# 分享接收的 sendData skill 在 uris 里写 utd，不把源 MIME 写成 type

审的是：资源
触发（任一种）：
- 读到：AndroidManifest 的 intent-filter 有 <action android:name="android.intent.action.SEND"/> + <data android:mimeType="text/plain"/>（或 "image/*"）；写错的样子：module.json5 的 sendData skill 里 uris 只有 {"type": "text/plain"} / {"type": "image/*"}，没有 utd 和 maxFileSupported；或挂在 EntryAbility 上带 entity.system.home
适用范围：把源端 SEND / SEND_MULTIPLE 分享接收入口迁成 module.json5 的 skills 时
做法：
- 另建承接分享的 Ability（"exported": true，"launchType": "multiton"），写一个 "actions": ["ohos.want.action.sendData"] 的 skill，"uris" 按源端每个 mimeType 逐项写 { "scheme": "file", "utd": <对应的 UTD>, "maxFileSupported": <条数> }（text/plain → general.plain-text，image/* → general.image 等）
- 不把源 mimeType 写成 uris 的 type，分享项不挂 entity.system.home；EntryAbility 只留 home 入口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- uris 的 utd：与 Want 相匹配的标准化数据类型，适用于分享等场景；maxFileSupported：一次能接收的最大数量，需与 utd 配合，缺省 0：分享接收端按这两个字段声明可接收的类型和数量（出处：module-configuration-file.md，uris标签说明）
- scheme：uris 中仅配置 type 时可以缺省，否则不可缺省：写 utd 时要带 "scheme": "file"（出处：module-configuration-file.md，uris标签说明）
- uris 对象允许的字段含 scheme、utd、maxFileSupported，scheme 必填：编译期校验认的字段（出处：鸿蒙 SDK 的 toolchains/modulecheck/module.json，skills.uris）
- PLAIN_TEXT = 'general.plain-text'、TEXT = 'general.text'、IMAGE = 'general.image'：utd 取值的写法：text/plain 对应 PLAIN_TEXT，文本、图片的父类型是 TEXT、IMAGE（出处：鸿蒙 SDK 的 ets/api/@ohos.data.uniformTypeDescriptor.d.ts，UniformDataType）
- ACTION_SEND_DATA = 'ohos.want.action.sendData'：发送单条数据记录的 action：分享接收 skills 的 action（出处：鸿蒙 SDK 的 ets/api/@ohos.ability.wantConstant.d.ts，wantConstant.Action.ACTION_SEND_DATA）
- 用 type: "text/plain" 声明时分享面板里不出现接收方；改成 scheme file + utd general.plain-text + maxFileSupported 1 后出现：按 MIME type 声明不会被系统分享面板列为目标（出处：卡里修好并验证过）
- 单个 sendData skill、uris 列 general.text / plain-text / hyperlink / image / jpeg / png / gif、scheme file、maxFileSupported 1：文本和图片都接收时修好后的声明（出处：卡里修好并验证过）
针对本应用要查的：
- 源 mimeType 对应的 UTD：鸿蒙 SDK 的 ets/api/@ohos.data.uniformTypeDescriptor.d.ts 里的 UniformDataType 枚举；或用该模块的 getUniformDataTypeByMIMEType(mimeType)（声明 @since 20）；按源 intent-filter 的 android:mimeType 找到对应的 'general.…' 字符串写进 utd
未核实：分享面板按 utd 选目标是卡里上机看到的；文档只说 utd 适用于分享等场景
来源：2 张卡，2 个应用
- case-4e3bf06f478ee642f9cb（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 6 ← 诊断
- case-6582e6c5e66cee6e4cc9（jerboa）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 7 ← 诊断
