# ui

界面迁移：布局与尺寸约束、安全区、主题样式、状态刷新、输入控件、点击命中与控件行为、弹窗、分页与列表、图形资源、结果反馈、Web 页承载与多页面导航（含返回键）的跨栈转换

[上一级](../index.md)

## 子主题

- [dialog](dialog/index.md) — 弹窗与半模态：V2 页面可用的弹窗载体、sheet 内二级弹窗的层级、按源 Dialog 类型选择呈现形态（路由约束不改变弹窗形态）、弹窗内二级选择器的层级、按源布局还原弹窗内容、源 Dialog 用 setView 注入自定义内容时的承载方式
- [feedback](feedback/index.md) — 操作结果反馈：异步结果各分支的提示与去向，多来源页面按区块的失败隔离与缓存降级，Snackbar 一类提示的宿主与渲染，校验失败提示的承载与可见性，多入口 loading 的起链与收口，降级方案的成功引导
- [graphics](graphics/index.md) — 图标与图形资源：动画矢量的状态帧、Lottie 动画层的接入、被注释的自定义绘制绑定、系统符号替代、资源迁移中的静态化标注，图标固有尺寸与 scaleType，整屏背景图的缩放方式，自定义图片组件的形状与裁剪，自绘图表的坐标原点，按使用场景区分的资源变体映射
- [input](input/index.md) — 输入与选择控件：源端输入约束到 TextInput 等组件属性的转换（含小数输入），格子式密码输入层与获焦，自定义控件 XML 属性的初值，选择列表行的选中标记（条件勾选与 Radio 的取舍）
- [interaction](interaction/index.md) — 点击命中与遮罩：Stack 叠层的 hitTestBehavior、贴底栏定位壳与页面级全屏遮罩的挂载方式、覆盖层对下层控件点击的影响、点击事件挂在哪一层节点，以及控件点击处理器副作用（音效、振动、持久化、面板）的迁移，以及 Button 等单子组件容器内按状态切换内容的写法
- [layout](layout/index.md) — 容器选择、约束与定位（ConstraintLayout、RelativeContainer、RelativeLayout 无相对规则子项的叠放、Column、Stack 内子项的纵向定位等），默认对齐差异、百分比尺寸与 margin、并排 wrap_content 列的宽度分配、跟随等高、滚动容器的包含范围、运行时挂载层与锚点转换、随滚动折叠的顶栏、全屏底层与状态覆盖层骨架、gone 节点与列表 item 布局，以及视觉修复中固定尺寸的依据；方向相关边距（start/end）的 LengthMetrics 写法
- [list](list/index.md) — 列表与宫格：多类型 Adapter 页面的 item 布局与绑定分支（默认态、文案模板、附属子卡），分页加载的并发门闩与刷新互斥，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退，多组列表的数据源绑定与级联选择，列表项滑动操作（swipeAction）的挂载位置
- [navigation](navigation/index.md) — 多屏拆成多页面后的导航：入口 Navigation 宿主与首屏入栈，main_pages 路由页登记与子组件/弹窗的划分，Tab/Swiper 子页的导航栈来源，目的地命名与参数（含多入口共享载荷、router 页面取参、源端 arguments/extras 的承接与宿主传参），点击出口的跳转接线，路由跳板 Activity，按启动来源的返回处理，返回栈重建、同一结果的单一导航出口、跳转前的状态交接、返回键分发、挂载与生命周期归属
- [pager](pager/index.md) — 分页与标签容器：ViewPager/ViewPager2 到 Swiper 的页数与手势（禁滑方式）、初始页定位、自绘 tab 与分页的双向联动
- [safearea](safearea/index.md) — 沉浸式安全区：全屏布局下前景避让与 expandSafeArea 的区别，避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅，路由页内容原点与顶部 inset 的消费位置，Tab 宿主按各 Tab 沉浸设置处理顶部安全区，全屏页底部按钮、按键区与贴底弹层的避让及承载层，逐页落实前景避让
- [state](state/index.md) — ArkUI V2 状态刷新与订阅：@Builder 参数（含异步重赋值的数组与对象）、复用开关组件的事件值、页面与共享模型的绑定、共享状态 key 的命名、按状态显隐、事件驱动的重新加载、单例 ViewModel 的取消语义与页面加载入口单飞、ForEach 键与子组件刷新、监听的注册与释放、乐观更新与访问器兜底
- [text](text/index.md) — 文本展示：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，静态说明页的逐字文案与图文结构，Tab、页面标题、设置行等可见文案的逐字取值，以及字符串资源生成哪些语言限定目录
- [theme](theme/index.md) — 主题、语义色、排版样式、控件默认样式与 style 继承属性（圆角、高度、渐变、字号）的迁移，被引用 drawable 的取值，Compose Brush 渐变与宿主内容色，视觉属性逐项取自源布局与适配器，颜色约束的写法，以及按色值与字号选择资源键
- [web](web/index.md) — Web 组件承载 H5：加载错误回调的范围与整页失败态，宿主原生标题栏与 H5 自带导航栏按页面状态的显隐
