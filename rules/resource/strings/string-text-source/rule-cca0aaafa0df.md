# 外部模板弹窗的文案从依赖 AAR 的字符串取，string.json 不写源端没有的文案

审的是：资源
触发（任一种）：
- 读到：源端模板方法的 Config 只传标题和条目数组，源码里 grep 不到按钮文案；写错的样子：string.json 里新增了取自 Config 条目的分区标题和摘要，或写入源码和依赖库里都没有的按钮文案（如「同意并继续」）
适用范围：为第三方库或 SDK 模板渲染的界面写目标端字符串资源时
做法：
- 文案从依赖 AAR 解包后的 res/values 字符串或安卓实机截图取；取不到的不自拟，在交付记录里标为未验证
针对本应用要查的：
- 模板里的文案：Gradle 缓存 caches 下解包的 aar：transforms-<N>/<hash>/transformed/<artifact>-<version>/res/values/values.xml，按模板布局里引用的 @string/ 名找；读出 <string name=…> 的文字，写进目标端 string.json；有多语言目录时一并取
来源：1 张卡，1 个应用
- case-b2c7b25e7fdfde0c6ec1（电子风水罗盘）：做法第 1 步 ← 建议 2、建议 3
