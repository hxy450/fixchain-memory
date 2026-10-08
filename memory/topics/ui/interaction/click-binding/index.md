# ui/interaction/click-binding

点击绑定的归属与副作用：挂在源端真正持有点击的节点、按处理器分支迁副作用、回调契约兑现、被注释的监听视为死按钮。

[上一级](../index.md)

## 本级经验

- [onClick 挂在源端真正持有点击的节点，整栏或子控件](lesson-fd3add7128663eb9998f.lesson.md) · 阶段：execute/repair · 信号：setOnClickListener, onClick, LinearLayout, DataBinding
- [两态按钮图标写成 if/else 或单 Image 选资源](lesson-ed5556325b6d8f510e2f.lesson.md) · 阶段：execute · 信号：Button, Image, setImageResource, ImageButton
- [带点击绑定控件按源处理器分支逐项迁移副作用](lesson-55e33a0621c3008ab8b3.lesson.md) · 阶段：execute · 信号：android:onClick, setChecked, postDelayed, ohos.permission.VIBRATE
- [接入专页时逐项兑现 @Event 回调契约不用空值短路](lesson-c061106fa1d809e518da.lesson.md) · 阶段：execute · 信号：@Event, requestPhotoEditorSession, dragEnable, cropEnable
- [监听回调体被注释时按无响应控件迁移，审计不放行](lesson-f3e614f295aa409485fd.lesson.md) · 阶段：execute/verify/repair · 信号：setOnClickListener, android:clickable, onClick, TODO
