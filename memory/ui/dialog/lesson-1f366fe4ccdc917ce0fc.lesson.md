# 源弹窗按它实际加载的布局 XML、函数全文或依赖库模板逐控件还原并接通配置回调，不以行为代码、相邻弹窗外壳、通用确认弹窗或现成文案代替

ID：`lesson-1f366fe4ccdc917ce0fc` · 版本：6

[本主题](index.md)

## 何时使用

界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时；用自绘弹层替代源端第三方 SDK 或 Helper 弹窗（隐私概要、协议弹窗），确定其内容分区、文案与操作区并接线交互回调时（含收口时重写弹窗正文或操作区）；规格提取阶段为这类库弹窗写验收条目与导航表时

## 适用情境

源弹窗由 ViewBinding/inflate 或工具类加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。也包括源确认区是带形状背景、可点击的复合容器（勾选控件＋主文案＋小字号次文案），目标准备复用只收单个文字 label 的主题按钮 builder，或用一个共享弹窗组件承载普通、严格等多个变体。也包括源页通过 PrivacyDialogHelper.showXxx(PrivacyConfig{…}) 一类库调用弹出隐私概要：标题、权限说明条目与图标、勾选两态图、链接色、服务协议与隐私政策链接回调、拒绝回调都在配置对象里，弹窗布局不在页面 XML，页面规格与合成快照没有弹窗节点；依赖库坐标可能只写在 app/build.gradle，工程源码只有 import 与调用，生成期没有实机截图；参考规格可能只在页面结构描述里提到“协议链接”，验收条目没有对应项；目标 WebView 页已存在，协议 URL 提供者可能由后续切片负责。

## 原因

只读调用代码、功能描述或 toast 文案会漏掉布局里的控件：关闭图标被写成“取消”按钮、单按钮变双按钮、标题与图标缺失、hint 取自 toast；截断的 grep/head 读不到函数结尾的失败分支，会把“源端无提示”当成事实。通用确认弹窗缺任何一项都不等价，却常被注成“视觉由通用弹窗承载”后解除标记。另一应用里编排者写客服弹窗前只做了一次关键字搜索，输出被截断只见无关路径，便按功能自拟通用弹层：标题文案不同，缺专用图标、右上关闭与说明文字，多出整宽关闭按钮；工程 skill 已写明弹窗外观要取自布局抽取结果而非记忆。另一应用中，启动页隐私弹窗的实现者只读到 Activity 对 DialogHelper 的一行调用，没打开 helper 与它加载的布局，就断定源端没有拒绝路径，写成单按钮通用弹窗，缺了承诺卡片、权限图标与“不同意 → 二次确认 → 退出”；图标资源其实已迁移，只是没有引用。即使读全了布局，实现时把可点击的复合容器换成只收一个 label 的通用按钮，也会丢掉勾选控件与次行文案；共享组件承载多个变体时，只给带显式勾选状态的变体画勾选控件，其他变体同样缺件，而保留下来的延时等行为说明原结构曾被读到。配置对象驱动的库弹窗没有可读的布局文件，只按页面布局或“最小契约”收尾，会丢掉结构、按钮语义与链接跳转。反方向同样偏离：配置字段描述的是模板的输入，不是版面；把权限条目数组直接展开成独立摘要分区、保留占位的等宽双按钮并自拟按钮文案，会与依赖库模板实际的分区、文内协议链接和勾选确认式主操作不符。按“原文”重写正文时只对照文案、不对照回调，还会把尚未实现的协议入口一并删掉。

## 做法

1. 从调用代码定位实际加载的布局（XxxBinding.inflate → xxx.xml、setContentView/inflate 的 R.layout 名，或弹窗工具函数里的布局名），读完该 XML 与弹窗函数全文（被截断就继续读），工程提供弹窗 probe 时用其控件清单，再写。
2. 按源布局逐控件核对：标题文案、图标、正文与说明、按钮数量与文案、关闭控件类型与位置、遮罩点击行为，hint 取 android:hint；每个容器自身的 layout_margin/padding 与子控件属性分开检查。
3. 通用弹窗缺少任一项时不作为等价实现；公共组件不在写权限内时，在页面内用条件浮层复刻，确实做不到就登记未决项并写明缺口。
4. 源确认区是可点击的复合容器（勾选或图标与多行文本）时整体转成复合按钮，如 Button() { Column() { Row() { 勾选, 主文案 } 次文案 } }，点击挂在整体上；不要用只收单个 label 的通用按钮 builder 代替。共享弹窗承载多个变体时，每个变体分别对照自己的布局，不因只有某个变体有显式勾选状态就推断其他变体没有勾选控件；保留延时等行为时，同时核对它依附的视觉元素。
5. 源弹窗由 Helper 或配置对象生成时，把配置字段与回调逐项列成清单（标题、说明条目、勾选控件及两态图、链接色与协议链接、同意与拒绝分支），按字段表达的语义落实：勾选两态图对应协议确认状态，链接回调与链接色对应可点击的服务/隐私协议文本，每个回调绑定到控件 onClick 与路由。重写正文或操作区前先与目标 onClick 逐项对账，替换文案时不删除仍未实现的入口；目标页已存在而 URL 提供者在后续切片时，仍绑定点击并留下指向负责切片的前向引用，不把链接降级为只改字色的静态文字。
6. 配置字段不等于版面：库渲染弹窗的分区、文案与操作区以依赖库为准，从 build.gradle 定位库坐标，解包其 AAR 的 res/layout 与 values/strings，或取实机截图，再按其结构实现。暂时取不到时，不把条目数组等数据直接展开成独立分区、不自拟按钮文案、不自定简化形态，把未核的文案与面板几何列为待截图或真机核对的差异写进报告，不标为“Android 原文”。规格提取阶段为会弹出库弹窗的页面补一节弹层结构：源调用锚点、全部配置字段、“布局由依赖库提供”及结构基准来源，每个交互回调写成验收条目并在导航表登记去向页（如各协议链接 → WebView 页）；上下文压缩后再写这类 UI 先重开对应源码片段。

来源支持：10 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-1f107c5992d58b6efb4a](../../../store/cases/case-1f107c5992d58b6efb4a/5ae192b7117bed1d100e13ba402fd45f8f07dc25ed314c6029218d6c31211882.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`5ae192b7117bed1d100e13ba402fd45f8f07dc25ed314c6029218d6c31211882`
- [case-89e7732b8a374944c6b2](../../../store/cases/case-89e7732b8a374944c6b2/810639d11dab94e726e28bbf772da715ae79949171acbf4ea64889179116cb69.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`810639d11dab94e726e28bbf772da715ae79949171acbf4ea64889179116cb69`
- [case-91f8e7d157380a2457fa](../../../store/cases/case-91f8e7d157380a2457fa/8a4c1a540d46c44dc344bf09c6d3da044f8195e0bfe2f99609096816d6dd39f8.json) · 结论：recommendation:2
  卡片版本：`8a4c1a540d46c44dc344bf09c6d3da044f8195e0bfe2f99609096816d6dd39f8`
- [case-9714f0bc8ce70721ee6b](../../../store/cases/case-9714f0bc8ce70721ee6b/904b1c0e79b747236aa970f4432e438efba4c53086442809077d6bfb09bac6ff.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`904b1c0e79b747236aa970f4432e438efba4c53086442809077d6bfb09bac6ff`
- [case-9f9881c4a9db00d14d07](../../../store/cases/case-9f9881c4a9db00d14d07/7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649`
- [case-a3404675917f8a352eb9](../../../store/cases/case-a3404675917f8a352eb9/251cba380648c037ead6cf198430233a569adb360f6b3ef5ae66404b79cb74ab.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`251cba380648c037ead6cf198430233a569adb360f6b3ef5ae66404b79cb74ab`
- [case-ae1e7b09c5cfe5214cd2](../../../store/cases/case-ae1e7b09c5cfe5214cd2/330b086d78a6625e9a9a7fa9cdcd53c10d3ecfef919ec81b12a73fcae4c061c4.json) · 结论：diagnosis, recommendation:1
  卡片版本：`330b086d78a6625e9a9a7fa9cdcd53c10d3ecfef919ec81b12a73fcae4c061c4`
- [case-b2c7b25e7fdfde0c6ec1](../../../store/cases/case-b2c7b25e7fdfde0c6ec1/54fdf7375c7df149cf80bacb158a266cee12c29172076257f335c61a1270bc70.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`54fdf7375c7df149cf80bacb158a266cee12c29172076257f335c61a1270bc70`
- [case-d5caf639de4ba1e70e28](../../../store/cases/case-d5caf639de4ba1e70e28/aad7cc6e4136641bd8650afd37bf490a21d6d2f71fcbafdb80a0f351bf46b3b7.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`aad7cc6e4136641bd8650afd37bf490a21d6d2f71fcbafdb80a0f351bf46b3b7`
- [case-f62209d059dec8e6aca4](../../../store/cases/case-f62209d059dec8e6aca4/1a18e9b5dfbae66db4693b94563e6ad2a12b31a37a4e5e77f33b0299d6effed1.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`1a18e9b5dfbae66db4693b94563e6ad2a12b31a37a4e5e77f33b0299d6effed1`
