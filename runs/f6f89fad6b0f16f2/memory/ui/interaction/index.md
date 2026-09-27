# ui/interaction

点击命中与遮罩：Stack 叠层的 hitTestBehavior、页面级全屏遮罩的挂载方式、覆盖层对下层控件点击的影响、点击事件挂在哪一层节点，以及控件点击处理器副作用（音效、振动、持久化、面板）的迁移

[上一级](../index.md)

## 本级经验

- [Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，条件遮罩用根 Stack 条件子节点](lesson-4a4f8d845a204ffa244b.lesson.md)
  - 时机：界面实现阶段，把 FrameLayout 叠放层转成 ArkUI Stack 并确定各层 hitTestBehavior 时；为页面加保存中、引导等全屏遮罩时
  - 情境：源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。
- [点击事件挂在源布局真正持有点击的节点上；清理重复绑定时保留整栏容器的事件](lesson-fd3add7128663eb9998f.lesson.md)
  - 时机：界面实现与返修阶段，为由多个子控件拼成的搜索栏、入口条决定 onClick 挂在哪一层，或清理其中的重复点击绑定时
  - 情境：源布局只在整条容器上绑定点击（如 LinearLayout 的 onClick 或 DataBinding 点击），内部图标、提示文字、“搜索”字样只负责展示；目标用 Row + Image + Text 模拟占位搜索框（不是 TextInput），点击后压栈进入目标页。
- [迁移带点击绑定的控件时按源点击处理器的分支逐项迁移副作用，不只做状态取反和换图](lesson-55e33a0621c3008ab8b3.lesson.md)
  - 时机：界面迁移阶段，为布局中带 onClick 绑定、状态选图或滑动面板的控件编写 ArkUI 事件与状态逻辑时
  - 情境：源布局控件用 android:onClick/数据绑定声明点击，或按 ViewModel 状态选图；实际行为（按键音、振动、偏好持久化、历史面板展开与回填）写在 Fragment 统一点击处理器、ViewModel 或第三方面板组件中；目标页需复刻这些开关与面板。
