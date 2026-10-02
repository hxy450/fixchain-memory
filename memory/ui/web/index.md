# ui/web

Web 组件承载 H5：加载错误回调的范围与整页失败态，宿主原生标题栏与 H5 自带导航栏按页面状态的显隐，整页滚动中 wrap_content WebView 的测高与锁定自身滚动

[上一级](../index.md)

## 本级经验

- [Web 组件的 onErrorReceive 也报告子资源错误：只在主框架出错时切换整页失败态](lesson-051f8984f21058916bd9.lesson.md)
  - 时机：WebView 页面实现阶段，为 Web 组件的加载错误回调决定是否切换整页失败/重试状态时
  - 情境：目标页用 Web 组件加载线上第三方 H5，自带加载进度与覆盖 Web 区域的失败重试卡片，在 onErrorReceive 中处理加载错误；参考模板可能把该回调写成无参形式。
- [宿主原生标题栏与 H5 自带导航栏按 H5 当前状态双向决定显隐；单页 H5 的状态从页面内容判断](lesson-1a5fbc237ad071a62aaa.lesson.md)
  - 时机：WebView 页面实现与修复阶段，决定宿主原生返回/标题栏在 H5 各页面状态下是否显示时
  - 情境：目标页用 Web 加载第三方单页 H5，宿主自带返回与标题栏；H5 首页没有自己的导航栏，而结果、查单、选择城市等子状态自带返回栏，状态切换时 URL 可能不变。
- [整页 ScrollView 内的 wrap_content WebView 转 ArkWeb：分别实现“高度跟随文档”和“Web 自身不滚”，锁 H5 滚动并对后加载内容复测](lesson-fd2dd522fdb03b3e5385.lesson.md)
  - 时机：界面实现或对齐修复阶段，把整页滚动容器内的 wrap_content WebView 转换为 ArkWeb，确定 Web 高度与滚动归属时
  - 情境：安卓 WebView layout_height=wrap_content，位于整页 ScrollView 内，加载含图片等后续资源的远程 H5；目标用 Scroll 包裹 Web，要求滚动全部交给外层页面。
