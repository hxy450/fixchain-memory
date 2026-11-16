# 点击

源端有 android:onClick、setOnClickListener、数据绑定的 android:onClick="@{…}"、Compose Modifier.clickable，目标端有 .onClick、它挂在哪一层和点击前的门控时

## 触发族

- [点击动作前的确认弹窗和条件门控](click-action-gate/index.md)（3 条）：读到源端点击或批量动作执行前的 if 门控（地区、用户类型、基类标志）和有没有 AlertDialog 确认；产物里无条件 await 接口后静默 return，或照先例页拷入了确认弹窗和门控
- [onClick 回调的事件参数](click-event-param/index.md)（1 条）：读到映射参考或别处回调里的 event.stopPropagation()；产物里 .onClick((event: ClickEvent) => …) 调了 stopPropagation
- [源端的点击监听和目标的 .onClick](click-binding/index.md)（8 条）：读到源布局的 android:onClick、可点击容器或 Java/Kotlin 的 setOnClickListener，交回的代码在某个组件上写了 .onClick(...)：挂在哪一层、回调体接了什么、和异步接口谁先谁后
- [数据绑定布局里的点击绑定](databinding-click/index.md)（4 条）：读到 <layout><data><variable> 的数据绑定布局，控件上写 android:onClick="@{…}" 或按 ViewModel 状态切换 android:src，交回的代码在对应组件上写了（或没写）.onClick
- [Compose 的 clickable / toggleable 点击修饰](compose-clickable/index.md)（6 条）：读到 Compose 的 Modifier.clickable / combinedClickable / toggleable 或 Card(onClick) 及其 role、enabled、indication 参数；产物里组件只挂了 .onClick(...)，缺按压态、.enabled(...)、accessibilityRole 或合并朗读
- [写操作点击前的账号就绪守卫](click-account-guard/index.md)（1 条）：读到 Compose 里投票、收藏、删除、发送等写操作的 onClick lambda 包在源端的账号就绪守卫函数里，或按钮组件收 account 参数、点击前先校验；产物里自写判定只 showToast 后 return，或回调直接调 ViewModel 写方法不加守卫
