# ui/state

ArkUI V2 状态刷新与订阅：@Builder 参数、页面与共享模型的绑定、ForEach 键与子组件刷新、监听的注册与释放

[上一级](../index.md)

## 本级经验

- [列表条目以新对象替换时，ForEach 键要包含会变且需要显示的字段](lesson-2e636699fa65aefd63f0.lesson.md)
  - 时机：功能实现与页面接线阶段，为可编辑列表选定条目更新方式与 ForEach 键时
  - 情境：列表条目编辑（如改名）后以保留 id 的新对象替换，ArkUI 用 ForEach 渲染并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy 更新。
  - 例外：更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键
- [随状态变化的控件参数不作 @Builder 值参，改为内联读取状态或用 @ComponentV2 子组件的 @Param](lesson-8d2979542fa2cd65150c.lesson.md)
  - 时机：界面实现阶段（页面转换与公共组件抽取），为源端带状态参数的子控件选择 ArkUI 复用写法时
  - 情境：源端 Compose 子 Composable 以当前状态算出的值作参数（如 enabled = count &gt; 1、颜色随选中态变化），目标 ArkUI 组件需要在状态变化后刷新 enabled、颜色等属性，准备把子控件抽成 @Builder 方法。
  - 例外：传入 @Builder 的只有文案、尺寸等在该组件生命周期内不随状态变化的值
- [页面向单例仓库或偏好注册监听时，把回调或句柄存成字段，在 aboutToDisappear 用同一引用移除](lesson-14b7f4090b7b83873b22.lesson.md)
  - 时机：功能接线阶段，在页面 aboutToAppear 里向应用级单例仓库、数据库或偏好注册数据监听时
  - 情境：目标数据层是应用级单例，用 addListener/removeListener（按回调引用移除）提供可观察数据；源端页面用 observeAsState、collectAsState 这类随界面生命周期自动结束的观察；ArkTS 子页出栈时不会自动注销。
- [页面直接读共享 @ObservedV2 模型的 @Trace 字段，不复制成 @Local 快照再手动同步](lesson-08c38f950b69e991607d.lesson.md)
  - 时机：功能接线与组收尾阶段，把页面显示状态接到 @ObservedV2 模型，且其他页面也会修改同一模型时
  - 情境：源端由一个根状态持有者驱动多个屏幕；目标端拆成 Navigation 下的多个页面，共享同一个 @ObservedV2 + @Trace 模型（如 AppStorageV2.connect 取得），子页修改共享模型后返回原页面。
  - 例外：需要与模型解耦的纯界面态（弹窗开关、未提交的输入草稿）仍放在页面 @Local
