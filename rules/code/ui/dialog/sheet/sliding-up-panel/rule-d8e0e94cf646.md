# SlidingUpPanelLayout 包着历史列表时，目标实现展开收起和点击回填，指示图不当装饰

审的是：代码
触发（任一种）：
- 读到：布局 XML 里 SlidingUpPanelLayout（带 umanoPanelHeight）包着历史 RecyclerView 和一个下拉指示图；写错的样子：指示图只写成没有 .onClick 的 Image 当装饰，没有展开、收起的 @State 和历史 List，或 ListItem 没有回填的 .onClick
适用范围：安卓布局里用滑动面板或容器组件承载历史记录这类可展开列表，迁成 ArkUI 页面时
做法：
- 把面板的展开、收起当作交互迁移：指示图 Image 加 .onClick 切换一个 @State 展开状态，按状态显示或收起历史 List
- List 的数据取源端的历史来源（源端初始化列表适配器时读的偏好历史），条数上限和清空按规格里的历史验收项；ListItem 的 .onClick 把该项回填到显示区
针对本应用要查的：
- 历史数据从哪来、点击一项做什么：源工程里 Fragment/Activity 创建时初始化历史列表适配器的那段，以及适配器的点击回调；记下读历史的偏好来源和上限，点击回调里写回显示区的是哪个字段
来源：1 张卡，1 个应用
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
