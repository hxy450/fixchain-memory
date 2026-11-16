# 随状态变化的文字和尺寸不按值传进 @Builder，留在 build 内联或用以内容为键的 ForEach

审的是：代码
触发（任一种）：
- 读到：源端值变化后立即更新显示（如 `Preference.setSummary`、重置后 `finish()` + `startActivity(getIntent())` 重建页面）；改写前的目标代码在 build 里内联 `Text(...)` 读 `@Local` / `@Param` 状态；写错的样子：为对齐几何新增的 `@Builder`，调用处实参直接读 this 上的状态变量、`@Param` 对象的字段或由它们算出的方法返回值；或把宽高等状态按值传给 `@Builder`
适用范围：ArkTS @ComponentV2 页面或组件里，为复刻版式把显示状态值的文字、尺寸抽进 @Builder 或绝对定位构建函数时
做法：
- 读状态的文字和属性留在 build 内联读取，或放进以内容为键的 ForEach，或交给 @ComponentV2 子组件的 @Param；@Builder 的值参只放标签、坐标等不随状态变化的值
- @Builder 里要用尺寸等状态时，改成无参 @Builder，在函数体里直接读 this 上的状态
- 落盘前搜新增 @Builder 的调用处，实参里有 this. 状态读取的都按上两步改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 调用 @Builder 默认按值传递；参数是状态变量时，状态变量改变不会引起 @Builder 内的 UI 刷新：按值传进去的文字和尺寸停在调用时的值（出处：arkts-builder.md，按值传递参数）
- 改回内联 Text 后切换选项 summary 即时更新；改成以内容为键的 ForEach 后重置统计全部归零；尺寸改成无参 Builder 内部读取后旋转能刷新：三种改法已上机验证（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7930b51b977ea17aee26（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2；取值 2 ← 诊断
