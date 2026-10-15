# 源弹窗由依赖库按配置对象（如 PrivacyConfig）渲染时，版面取自库模板，配置里的每个回调逐项接到目标控件

ID：`lesson-afc5868d6c1a6dec04fa` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与收口阶段，用自绘弹层替代源端第三方 SDK 或 Helper 渲染的弹窗（隐私概要、协议弹窗），确定分区、文案与操作区并接线回调时（含收口时重写弹窗正文或操作区）；规格提取阶段为会弹出这类库弹窗的页面写验收条目与导航表时

## 适用情境

源页通过库调用加配置对象弹窗：标题、权限说明条目与图标、勾选两态图、链接色、服务协议与隐私政策链接回调、同意与拒绝回调都在配置对象里，弹窗布局不在工程 XML，页面规格与合成快照没有弹窗节点；依赖库坐标可能只写在 app/build.gradle，工程源码只有 import 与调用；参考规格可能只在页面结构描述里提到“协议链接”；目标 WebView 页已存在，协议 URL 提供者可能由后续切片负责。

## 原因

配置对象驱动的库弹窗没有可读的布局文件，只按页面布局或“最小契约”收尾会丢掉结构、按钮语义与链接跳转。反方向同样偏离：配置字段描述的是模板的输入，不是版面；把条目数组直接展开成独立分区、自拟按钮文案，会与库模板实际的分区、文内协议链接和勾选确认式主操作不符。按“原文”重写正文时只对照文案、不对照回调，还会把尚未实现的协议入口一并删掉。

## 做法

1. 把配置字段与回调逐项列成清单（标题、说明条目、勾选控件及两态图、链接色与协议链接、同意与拒绝分支），按字段语义落实：勾选两态图对应协议确认状态，链接回调与链接色对应可点击的服务/隐私协议文本，每个回调绑定到控件 onClick 与路由。
2. 版面以依赖库为准：从 build.gradle 定位库坐标，到 Gradle 缓存（~/.gradle/caches/modules-2/files-2.1/<group>/<artifact>/<version>）解包 AAR 的 res/layout 与 values/strings，或取实机截图，再按其分区、文案与操作区实现；不把条目数组直接展开成独立分区，不自拟按钮文案。
3. 依赖从未下载、也没有实机截图时，向协调者索取截图或依赖包，并在报告中把未核的文案与面板几何列为未验证差异，不标为“Android 原文”，也不自定简化形态。
4. 重写正文或操作区前先与目标 onClick 逐项对账，替换文案时不删除仍未实现的入口；目标页已存在而 URL 提供者在后续切片时，仍绑定点击并留下指向负责切片的前向引用，不把链接降级为只改字色的静态文字。
5. 规格提取阶段为会弹出库弹窗的页面补一节弹层结构：源调用锚点、全部配置字段、“布局由依赖库提供”及结构基准来源；每个交互回调写成验收条目，并在导航表登记去向页（如各协议链接 → WebView 页）。上下文压缩后再写这类 UI，先重开对应源码片段。

来源支持：4 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-1f107c5992d58b6efb4a](../../../store/cases/case-1f107c5992d58b6efb4a/5ae192b7117bed1d100e13ba402fd45f8f07dc25ed314c6029218d6c31211882.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`5ae192b7117bed1d100e13ba402fd45f8f07dc25ed314c6029218d6c31211882`
- [case-9714f0bc8ce70721ee6b](../../../store/cases/case-9714f0bc8ce70721ee6b/904b1c0e79b747236aa970f4432e438efba4c53086442809077d6bfb09bac6ff.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`904b1c0e79b747236aa970f4432e438efba4c53086442809077d6bfb09bac6ff`
- [case-9f9881c4a9db00d14d07](../../../store/cases/case-9f9881c4a9db00d14d07/7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649`
- [case-b2c7b25e7fdfde0c6ec1](../../../store/cases/case-b2c7b25e7fdfde0c6ec1/54fdf7375c7df149cf80bacb158a266cee12c29172076257f335c61a1270bc70.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`54fdf7375c7df149cf80bacb158a266cee12c29172076257f335c61a1270bc70`
