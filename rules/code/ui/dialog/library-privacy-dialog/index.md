# 外部库模板按配置对象弹出的隐私协议弹窗

agent 会看到什么：读到源端构造 Config 配置对象（标题、条目及图标、checkImageId / unCheckImageId、linkColor、goServiceLink / goPrivacyLink 回调）交给外部库 Helper 弹窗，工程里没有这个弹窗的 layout；产物里自写的 CustomDialog / openCustomDialog 弹窗

## 规矩

- rule-7831cca858db｜源端弹窗由库加配置对象弹出时，按配置字段逐项实现弹层，不用现成控件简化｜读到：源端 Kotlin/Java 里构造一个弹窗配置对象（标题、说明条目及图标、勾选两态图、协议链接回调、拒绝回调）交给库的 Helper 弹出，页面 layout XML 和规格的 layout_sources 里都没有这个弹窗；写错：目标写成居中白色圆角卡片：标题和正文借用其他页面的 $r('app.string.…')，只有通用取消/确定两个按钮，缺说明条目、勾选控件和协议链接，同意/拒绝的语义丢失；报告的 uncertain_regions 也没提这处简化
- rule-5fc493aeb7b6｜只有外部模板的配置参数时，不把配置条目展开成可见分区，先取 AAR 布局或截图｜读到：源端只调用外部库模板方法并传入 Config 对象（标题、条目数组、图标、勾选图、链接色、链接回调），工程里没有模板的 layout；写错：目标页把 Config 里的条目数组展开成标题下的独立摘要分区，沿用两个等宽 Button，按钮文案是源码里没有的自拟文字
- rule-38562dae9e7b｜拿不到模板布局时，仍把配置里的勾选图和链接回调落实成确认状态和可点协议文本｜读到：源端模板 Config 里有勾选/未勾选图（checkImageId / unCheckImageId）、linkColor 和服务、隐私链接回调；写错：目标弹窗没有协议确认状态，也没有可点的服务/隐私协议文本；linkColor 和链接回调都没用上
- rule-13318025fefa｜按源码重写隐私弹窗时，源配置里每个协议链接回调在目标都要有可点击入口｜读到：源码隐私弹窗配置里有 goServiceLink / goPrivacyLink 这类回调，调用 WebView 页的启动方法打开协议 URL；写错：目标弹窗里协议名称只是没有 .onClick 的 Text，或者替换正文文案时把协议名称连同入口一起删掉；整页没有 pushPathByName 到 WebView 页的跳转
