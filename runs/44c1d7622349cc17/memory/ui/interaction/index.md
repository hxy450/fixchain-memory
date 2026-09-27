# ui/interaction

点击命中与遮罩：Stack 叠层的 hitTestBehavior、页面级全屏遮罩的挂载方式、覆盖层对下层控件点击的影响

[上一级](../index.md)

## 本级经验

- [Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，条件遮罩用根 Stack 条件子节点](lesson-4a4f8d845a204ffa244b.lesson.md)
  - 时机：界面实现阶段，把 FrameLayout 叠放层转成 ArkUI Stack 并确定各层 hitTestBehavior 时；为页面加保存中、引导等全屏遮罩时
  - 情境：源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。
