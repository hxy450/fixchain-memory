# 源端只有外层容器持有点击时，onClick 只挂在外层 Row 上，去重时也保留外层

审的是：代码
触发（任一种）：
- 读到：源布局只在整条 LinearLayout 上绑定点击（android:onClick、数据绑定的点击属性或 setOnClickListener），内部 ImageView、提示 TextView、分隔 View 都没有点击；写错的样子：目标外层 Row 有 .onClick(...)，内部某个 Text 或 Image 又挂了同一个回调
- 写错的样子：返修清理重复点击时删掉了外层 Row 的 .onClick(...)，只留子控件上的绑定，整栏中间的提示区域点不动
适用范围：用 Row + Image + Text 拼成的占位搜索栏、入口条（不是 TextInput），点击后跳转
做法：
- 按源布局里真正持有点击的节点挂：源端只有外层容器可点时，只给外层 Row 写 .onClick(() => <源端的点击处理>)，内部 Text、Image 不挂同一个回调
- 已有重复绑定要去重时，先查源布局的点击持有者和视觉上的点击区域：保留覆盖整栏的外层 Row 事件，删子控件事件，不把外层容器降成纯布局包装
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onClick(event: (event: ClickEvent) => void): T：组件的点击回调，挂在哪个组件上就是哪个组件的点击区域（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- 外层 Row 加回 onClick、删除右侧文字上的 onClick，只保留整栏一个入口：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-adacd41d159c24498006（android-panorama-map-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；取值 2 ← 诊断
