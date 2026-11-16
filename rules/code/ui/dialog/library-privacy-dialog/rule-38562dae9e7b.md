# 拿不到模板布局时，仍把配置里的勾选图和链接回调落实成确认状态和可点协议文本

审的是：代码
触发（任一种）：
- 读到：源端模板 Config 里有勾选/未勾选图（checkImageId / unCheckImageId）、linkColor 和服务、隐私链接回调；写错的样子：目标弹窗没有协议确认状态，也没有可点的服务/隐私协议文本；linkColor 和链接回调都没用上
适用范围：迁移第三方模板弹窗、暂时拿不到模板布局时
做法：
- 勾选/未勾选图对应一个 @State 的协议确认状态，点击切换并换图，主操作带上勾选图标
- 链接回调和 linkColor 写成文内可点的协议文本：Text() { Span('…') Span('《服务协议》').fontColor(<linkColor>).onClick(() => <服务链接回调>) … }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontColor(value: ResourceColor): SpanAttribute：给协议链接那段文字上 linkColor（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.fontColor）
- Span 的通用事件只支持点击事件 onClick 和悬浮事件 onHover：文内链接用 Span.onClick 接回调（出处：ts-basic-components-span.md，事件）
- 「已阅读并同意《服务协议》及《隐私协议》」写成文内链接，链接色取配置的 linkColor；主操作带勾选图标：以安卓截图为基准重构后的写法（出处：卡里修好并验证过）
未核实：文内链接 Span 的点击区域在小字号下是否够用，卡里没有说
来源：1 张卡，1 个应用
- case-b2c7b25e7fdfde0c6ec1（电子风水罗盘）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
