# 会被异步更新的展示对象不作多参数 @Builder 的值参，改传整个 @ObservedV2 对象或拆子组件

审的是：代码
触发（任一种）：
- 读到：源端卡片的数据在页面出现（onResume）或定位回调（onLocationChanged）完成后才更新；写错的样子：普通 class 对象由 @Local 持有，经两个以上参数的 @Builder（如 this.行Builder(this.item, true)）按值渲染，数据更新后卡片不刷新
适用范围：@ComponentV2 页面用 @Builder 渲染会被 @Local / @Trace 异步更新的展示项时
做法：
- 展示模型写成 @ObservedV2 类、显示字段加 @Trace，把整个对象传给 @Builder，在 builder 内读它的属性
- 或者在 builder 内直接读 this 上的状态，或拆成 @ComponentV2 子组件用 @Param 传入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @Builder 默认按值传递，参数为状态变量时其改变不会引起 @Builder 内的 UI 刷新：普通对象按值传入，后续更新看不到（出处：arkts-builder.md，按值传递参数）
- 按引用传递只在传入一个参数且该参数直接传入对象字面量时生效，有多个参数时不支持 @Builder 内 UI 刷新：两参以上的 @Builder 不能靠按引用刷新（出处：arkts-builder.md，参数传递规则）
- @ComponentV2 中配合 @ObservedV2 和 @Trace，按值传递也能刷新：传 @ObservedV2 对象、builder 内读 @Trace 属性（出处：arkts-builder.md，使用@ComponentV2装饰器触发动态刷新）
来源：1 张卡，1 个应用
- case-8a889aba046e2d2f1f3e（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
