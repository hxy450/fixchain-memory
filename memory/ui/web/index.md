# ui/web

Web 组件承载 H5：加载错误回调的范围与整页失败态，宿主原生标题栏与 H5 自带导航栏按页面状态的显隐，整页滚动中 wrap_content WebView 的测高与锁定自身滚动，导航拦截区分用户导航与程序装载、loadData 的挂接时机，WebSettings 排版（viewport）的显式落实，未设 WebViewClient 时链接的默认外部打开，未做设置的 WebView 按 Android 默认值对齐

[上一级](../index.md)

## 本级经验

- [ArkWeb 导航拦截按请求属性区分用户导航，loadData 在控制器挂接后调用](lesson-f095b7b87fbc8d8ed03d.lesson.md)
  - 时机：实现阶段，把 WebView.shouldOverrideUrlLoading 与 loadDataWithBaseURL 迁移为 Web 组件、onLoadIntercept 与 controller.loadData 时
  - 情境：源 shouldOverrideUrlLoading 只处理用户点开的链接，不为程序装载回调；目标 onLoadIntercept 对初始装载同样回调。
- [Web 组件的 onErrorReceive 也报告子资源错误：只在主框架出错时切换整页失败态](lesson-051f8984f21058916bd9.lesson.md)
  - 时机：WebView 页面实现阶段，为 Web 组件的加载错误回调决定是否切换整页失败/重试状态时
  - 情境：目标页用 Web 组件加载线上第三方 H5，自带加载进度与覆盖 Web 区域的失败重试卡片，在 onErrorReceive 中处理加载错误；参考模板可能把该回调写成无参形式。
- [WebView 排版与缩放按源端 WebSettings（未做设置时取 Android WebView 默认值）在 ArkWeb 中显式落实：HTML 声明 viewport，缩放与 JS 逐项对齐](lesson-65ebab594a9dabe77ac2.lesson.md)
  - 时机：规格映射、页面实现与 HTML 产出阶段，把 WebView（含未调用任何 WebSettings 的 WebView）迁移到 ArkWeb、确定 Web 属性时
  - 情境：源 WebView 通过设置按设备宽排版；目标 HTML 由独立服务产出，可能没有 viewport 声明。也包括源 Activity 只 loadUrl 本地 asset HTML、未修改任何 WebSettings，本地 HTML 没有 viewport meta；写者提出“对齐 Android 默认值”，只落实了 JS 一项。
- [宿主原生标题栏与 H5 自带导航栏按 H5 当前状态双向决定显隐；单页 H5 的状态从页面内容判断](lesson-1a5fbc237ad071a62aaa.lesson.md)
  - 时机：WebView 页面实现与修复阶段，决定宿主原生返回/标题栏在 H5 各页面状态下是否显示时
  - 情境：目标页用 Web 加载第三方单页 H5，宿主自带返回与标题栏；H5 首页没有自己的导航栏，而结果、查单、选择城市等子状态自带返回栏，状态切换时 URL 可能不变。
- [整页 ScrollView 内的 wrap_content WebView 转 ArkWeb：分别实现“高度跟随文档”和“Web 自身不滚”，锁 H5 滚动并对后加载内容复测](lesson-fd2dd522fdb03b3e5385.lesson.md)
  - 时机：界面实现或对齐修复阶段，把整页滚动容器内的 wrap_content WebView 转换为 ArkWeb，确定 Web 高度与滚动归属时
  - 情境：安卓 WebView layout_height=wrap_content，位于整页 ScrollView 内，加载含图片等后续资源的远程 H5；目标用 Scroll 包裹 Web，要求滚动全部交给外层页面。
- [源 WebView 未设 WebViewClient 时链接按 Android 默认交给外部浏览器：拦截非本地 URL，用 viewData + entity.system.browsable 拉起，失败再由 Web 自行加载；页内锚点与本地资源放行](lesson-42cf412cacabb3c8c281.lesson.md)
  - 时机：界面实现阶段，把未设置 WebViewClient 的 Android WebView 迁移为 ArkWeb、确定链接点击的导航处理与外链打开写法时；复用其他页面已有的外链打开函数时
  - 情境：源 Activity 只 findViewById 后 loadUrl 本地 asset HTML，没有 setWebViewClient；HTML 含页内锚点与外部 http(s) 链接；目标拦截外链后用 startAbility 打开，工程其他页面可能照抄同一个外链函数。
  - 例外：源端设置了 WebViewClient 并覆写 shouldOverrideUrlLoading：按其逻辑实现
