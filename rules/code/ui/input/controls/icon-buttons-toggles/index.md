# ImageButton 一类图标按钮和开关的状态切换与获焦

agent 会看到什么：读到源端 ImageButton / ImageView 按状态 setImageResource、setTextColor 切换图标和文字颜色（按选中数、播放暂停、各开关自己的状态），或布局里的 <ImageButton> / <Button>；产物里 Image 的资源怎么选（两个独立 if）、开关行共用 @Builder 传 boolean 值参、复用开关组件的 @Event 回调、Image(...).onClick 没有 .focusable(true)

## 规矩

- rule-62c3021f8996｜Button 内做两态图标切换时写一个 if/else 或单个 Image 选资源，不写两个独立 if｜读到：源端按钮按状态切换图标（如播放 / 暂停的 ImageButton、setImageResource）；写错：Button() { if (!isPlaying) { Image(…) } if (isPlaying) { Image(…) } } 两个互斥的独立 if
- rule-0d310d0a5b6d｜源端按选中数量切换图标和文字颜色的操作栏，目标成组映射每个状态的图和色｜读到：Java 里按选中数量对按钮调 setImageResource(R.drawable....) 在灰图和高亮图之间切换、setTextColor(...) 切换文字颜色，删除文字另有颜色，置顶按钮在两张图之间切换；写错：目标的批量操作底栏只有文字，只按选中状态切换文字颜色，没有 Image 或 Image 不随状态切换
- rule-e340b6ba98e3｜会变的开关状态不作成员 @Builder 的值参，每个开关行直接绑定自己的状态｜读到：源端多个开关各自持有状态字段，各自的 setOnClickListener 只翻转自身字段、写对应偏好并 setImageResource 刷新自身图标；写错：几个开关行共用一个成员 `@Builder`，把随 @Local / @Trace 变化的开关状态（boolean）作为值参传入，在 Builder 里据此画图标或再传给子组件的 @Param
- rule-fbc212c90dcb｜接复用开关组件时，把 @Event 给出的目标值原样传给该开关的 setter，不改成无参回调再反转｜读到：复用开关组件的契约是 @Param 接当前状态、@Event 回调带一个下一状态参数（组件内点击时传当前状态取反）；写错：页面把组件的 @Event 回调写成无参的 (): void => action()，丢掉组件给出的值，再由页面变量或 ViewModel 的 toggle 反转接口拿旧值取反
- rule-d29854fb3686｜ImageButton/Button 转成 Image 时补 focusable(true)，焦点框设透明｜读到：布局 XML 里的 <ImageButton> 或 <Button>（安卓缺省可获焦）；写错：目标端写成只有 .onClick(...) 的 Image(...)，没有 .focusable(true)
- rule-dd7d1c879b91｜用复用开关组件替换原开关行时，整行点击热区和无障碍分组不能缩成只剩图标｜读到：被替换的原实现在整行的 Row 上挂 .onClick(…)；写错：换成复用开关组件后只有其中的 Image 上有 .onClick，行容器上的点击没了，整行也不再作为一个无障碍单元
- rule-8336139b7d2b｜@Builder 接收随状态变化的图标或文案时，改传 () => Resource 回调或在内部读状态，不按值传｜读到：安卓源码在模式切换、暂停等状态变化后调用 setImageResource 或刷新图标的方法，重设按钮的图标或描述；写错：@Builder 形参写成 resource: Resource、label: Resource，调用处传入读 this 上状态的三元表达式（cond ? $r('app.media.a') : $r('app.media.b')）求值后的结果，状态变了按钮仍停在首次渲染的图标和文案
- rule-1900b3d139af｜给状态驱动图标的按钮写回归时，断言改状态后重渲染的图标和文案，并覆盖双向切换｜读到：安卓源码在状态变化后调用 setImageResource 或刷新图标的方法重设按钮图标；写错：回归测试只断言控件布局坐标，或只用正则确认源码里有点击处理方法，没有「改状态后再取 Image 资源和 accessibilityText」的断言
- rule-7bdeaa1439c4｜只响应点击长按的 ImageButton 转成 Image 时，每个 Image 写 .draggable(false)｜读到：ImageButton，或挂了 setOnClickListener / setOnLongClickListener 的 ImageView（快门、图库缩略、屏上图标等），源端没有任何拖放逻辑；写错：Image(...) 直接挂 .onClick，或放在挂 onClick / LongPressGesture 的 Stack、Button 里，修饰链上没有 .draggable(false)
