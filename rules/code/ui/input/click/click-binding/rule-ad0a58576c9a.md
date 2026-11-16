# 目标 .onClick 挂在哪、接什么，按源端点击监听的持有者和回调体定

审的是：代码
触发（任一种）：
- 读到：源布局 XML 的 android:onClick、数据绑定的点击属性，或 Java/Kotlin 里某个 View 的 setOnClickListener(…)；写错的样子：目标的 .onClick(...) 挂在和源端持有者不同的组件上（外层 Row 和内部 Text、Image 之间挂错或重复挂），或源端回调体为空、被注释，目标仍接了可用功能
适用范围：把安卓布局和页面代码里的点击绑定迁成 ArkUI 组件的 .onClick，或返修时增删、去重 .onClick
做法：
- 先找源端的点击持有者：布局里带 android:onClick 或数据绑定点击属性的节点；代码里 setOnClickListener 的接收者顺着 findViewById(R.id.…) 或绑定类字段对回布局里同 android:id 的节点
- 打开回调体全文；要求连源码缺陷一并 1:1 复刻时，回调体为空或唯一调用被注释的按无响应处理，不接 .onClick
- 目标只在和持有者对应的那个组件上写 .onClick(() => <源端回调里的处理>)，同一回调不在父子组件上重复挂
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setOnClickListener(@Nullable OnClickListener l)：给这个 View 注册点击回调，不可点的 View 会变成可点：点击区就是被调用的那个 View，不会扩到父布局（出处：android.view.View#setOnClickListener）
- onClick(event: (event: ClickEvent) => void): T：ArkUI 组件的点击事件，挂在哪个组件上就只有它响应（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
针对本应用要查的：
- 源端谁持有点击、回调里做了什么：源工程的页面布局 XML（含 include 进来的布局）和对应 Activity、Fragment、Adapter 的 Java 或 Kotlin 文件，按 android:onClick、setOnClickListener 搜；代码里的接收者顺着 findViewById(R.id.…) 或绑定类字段对回布局里同 android:id 的节点，记下它是外层容器还是内部子控件；再读回调体是否为空或被注释
来源：3 张卡，2 个应用
- case-784ba4ab52f98f7156b6（企业安全培训）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-a732e742bcad3963e050（企业安全培训）：做法第 2 步 ← 建议 2
- case-adacd41d159c24498006（android-panorama-map-vest7）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
