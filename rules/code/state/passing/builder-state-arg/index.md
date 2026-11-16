# 多参数 @Builder 的状态值参

agent 会看到什么：读到 Compose 子 Composable 以状态算出的 enabled、颜色等作参数，或搬来的 @Builder 片段参数随状态变；产物里 @Builder 带 enabled: boolean 这类值参、调用处传 this.count > 1 一类状态表达式

## 规矩

- rule-4042e3261fa5｜子控件的启用态、颜色由当前状态算出时，不作 @Builder 值参，改内联属性链或 @Param 子组件｜读到：Compose 自定义子 Composable 以状态算出的布尔值作参数（如按钮的 label、enabled、onClick），内部 `Surface` 颜色和 `Modifier.clickable(enabled = enabled)` 由它决定，调用处传 `enabled = count > 1` 这类表达式；写错：目标写成 `@Builder` 函数带 `enabled: boolean` 值参，调用处传 `this.count > 1` 一类状态表达式，内部 `.enabled(enabled)`、fontColor、backgroundColor 读这个值参
- rule-42afc3802bdb｜随状态变化的文字和尺寸不按值传进 @Builder，留在 build 内联或用以内容为键的 ForEach｜读到：源端值变化后立即更新显示（如 `Preference.setSummary`、重置后 `finish()` + `startActivity(getIntent())` 重建页面）；改写前的目标代码在 build 里内联 `Text(...)` 读 `@Local` / `@Param` 状态；写错：为对齐几何新增的 `@Builder`，调用处实参直接读 this 上的状态变量、`@Param` 对象的字段或由它们算出的方法返回值；或把宽高等状态按值传给 `@Builder`
- rule-ffd1e0079c4e｜会被整体重赋的数组作多参数 @Builder 值参时，改成在 builder 内直接读 this 上的状态｜写错：多参数的 `@Builder` 收数组值参并在里面 `ForEach(items)`，调用处传 `this.<状态数组>`，而这个数组之后会被整体重新赋值（如异步查询结果）
- rule-9f59fe8f4380｜@ComponentV2 里把会变的状态当 @Builder 值参传入时，改为片段内直读或子组件 @Param｜写错：@ComponentV2 组件里调用带参 @Builder 时，实参是 @Local 状态或 @Trace 属性（延迟填充的数组、数值、文案、当前条目、enabled 布尔），片段里的菜单、数值、文案不随状态变化
- rule-9c22e9651baf｜随语言变化的文案不作 @Builder 值参，改传键在体内调 t(key)，或用 @Param 子组件｜读到：目标工程的文案在渲染期经 `t(key)` 或委托 `t()` 的 getter 取值，语言状态是 `@Trace` 字段、声明式驱动刷新；写错：带参 `@Builder` 的签名里有 `label: string` 一类文案值参，调用处传 getter 或 `t(…)` 的求值结果，再转交给子组件
