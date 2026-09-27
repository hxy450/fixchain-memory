# ui

界面迁移：布局与尺寸约束、安全区、主题样式、状态刷新、输入控件、点击命中、弹窗、分页与列表、图形资源、结果反馈与多页面导航（含返回键）的跨栈转换

[上一级](../index.md)

## 子主题

- [dialog](dialog/index.md) — 弹窗与半模态：V2 页面可用的弹窗载体、sheet 内二级弹窗的层级、按源 Dialog 类型选择呈现形态、按源布局还原弹窗内容
- [feedback](feedback/index.md) — 操作结果反馈：异步结果各分支的提示与去向，Snackbar 一类提示的宿主与渲染，多入口 loading 的起链与收口，降级方案的成功引导
- [graphics](graphics/index.md) — 图标与图形资源：动画矢量的状态帧、系统符号替代、资源迁移中的静态化标注，图标固有尺寸与 scaleType
- [input](input/index.md) — 输入控件：源端输入约束到 TextInput 等组件属性的转换，格子式密码输入层与获焦，自定义控件 XML 属性的初值
- [interaction](interaction/index.md) — 点击命中与遮罩：Stack 叠层的 hitTestBehavior、页面级全屏遮罩的挂载方式、覆盖层对下层控件点击的影响，点击事件挂在哪一层节点
- [layout](layout/index.md) — 容器选择、约束与定位（ConstraintLayout、RelativeContainer、Column 等），默认对齐差异、百分比尺寸与 margin、跟随等高、滚动容器的包含范围、运行时挂载层与锚点转换、随滚动折叠的顶栏、全屏底层与状态覆盖层骨架、gone 节点与列表 item 布局，以及视觉修复中固定尺寸的依据
- [list](list/index.md) — 列表与宫格：分页加载的并发门闩与刷新互斥，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退
- [navigation](navigation/index.md) — 多屏拆成多页面后的导航：入口 Navigation 宿主与首屏入栈，main_pages 路由页登记与子组件/弹窗的划分，Tab/Swiper 子页的导航栈来源，目的地命名与参数（含多入口共享载荷、router 页面取参），点击出口的跳转接线，返回栈重建、同一结果的单一导航出口、跳转前的状态交接、返回键分发、挂载与生命周期归属
- [pager](pager/index.md) — 分页与标签容器：ViewPager/ViewPager2 到 Swiper 的页数与手势（禁滑方式）、初始页定位、自绘 tab 与分页的双向联动
- [safearea](safearea/index.md) — 沉浸式安全区：避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅，全屏页底部按钮与贴底弹层的避让，逐页落实前景避让
- [state](state/index.md) — ArkUI V2 状态刷新与订阅：@Builder 参数、复用开关组件的事件值、页面与共享模型的绑定、共享状态 key 的命名、按状态显隐、事件驱动的重新加载、ForEach 键与子组件刷新、监听的注册与释放、乐观更新与访问器兜底
- [text](text/index.md) — 文本展示：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，以及静态说明页的逐字文案与图文结构
- [theme](theme/index.md) — 主题、语义色、控件默认样式与 style 继承属性（圆角、高度、渐变）的迁移，颜色约束的写法，以及按色值选择颜色资源
