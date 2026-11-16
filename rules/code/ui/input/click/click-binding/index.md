# 源端的点击监听和目标的 .onClick

agent 会看到什么：读到源布局的 android:onClick、可点击容器或 Java/Kotlin 的 setOnClickListener，交回的代码在某个组件上写了 .onClick(...)：挂在哪一层、回调体接了什么、和异步接口谁先谁后

## 通用查法

### 目标 .onClick 挂在哪、接什么，按源端点击监听的持有者和回调体定

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

## 规矩

- rule-bc7f16a6ff98｜源端只有外层容器持有点击时，onClick 只挂在外层 Row 上，去重时也保留外层｜读到：源布局只在整条 LinearLayout 上绑定点击（android:onClick、数据绑定的点击属性或 setOnClickListener），内部 ImageView、提示 TextView、分隔 View 都没有点击；写错：目标外层 Row 有 .onClick(...)，内部某个 Text 或 Image 又挂了同一个回调
- rule-ef19079c465c｜setOnClickListener 只绑行内子 TextView 时，只给对应 Text 加 onClick｜读到：Java/Kotlin 里 setOnClickListener 只绑在行内某个子 TextView（如右侧值文本）上；同页别的行才把整行 layout 设为可点；写错：对应的 Row 整行挂了 .onClick(...)，不是只给那个 Text 挂；或者注释写着某个子视图可点，.onClick 却挂在 Row 上
- rule-5828563c529b｜源端 setOnClickListener 回调体为空或调用被注释时，目标不接 onClick，按死按钮迁｜读到：源码 setOnClickListener(…) 的 onClick 回调体为空，或里面唯一的调用被 // 注释掉；写错：目标在对应组件上接了 .onClick(() => …) 并做成可用功能（弹菜单、选图等），注释自述「源码已注释为死码——按集成点接线」
- rule-31dce882ad81｜可点击容器里有勾选和两行文案时，目标写成复合 Button，不用单 label 文本按钮｜读到：布局里可点击的 LinearLayout（或带 shape 背景的容器，setOnClickListener 挂在容器上）内含 CheckBox 或图标、主文案 TextView 和小字号的次文案 TextView；写错：目标写成只收一个 label 的通用文本按钮（Button(label) 一类的 builder），勾选控件和次文案都没了
- rule-bd8c94f1b533｜规格要求点击即翻转（乐观更新）时，先翻本地状态再调接口，不把翻转放进 if (ok)｜读到：规格验收写「点击后状态翻转且 UI 即时刷新（乐观更新）」，而安卓源里 setOnClickListener 先调网络接口、在成功回调里才设选中态；写错：目标的点击处理先调异步接口，把状态变量的翻转放在 .then(ok => { if (ok) { … } }) 这类成功分支里，注释却写着乐观更新
- rule-2c99f4ccdfbb｜行组件内层 onClick 调空默认 @Event、外层 ListItem 也挂 onClick 时，点击只留一个归属｜读到：安卓 PreferenceScreen 里整行可点的 Preference、ListPreference 或子屏入口，规格要求点整行触发行动作（弹层、压栈、分支处理）；写错：@ComponentV2 行组件里声明了带默认空实现的 @Event 回调（= () => {}），组件内层 Row 的 .onClick 调用它；调用处不传这个事件，真实动作挂在外层 ListItem().onClick 上
- rule-2034ff657451｜父子组件都要响应点击时，在父组件上用 parallelGesture，不按 DOM 冒泡推理｜读到：安卓整行可点的 Preference 行里还带自己响应点击的子控件，行和子控件都要响应；写错：子组件挂了 .onClick，父容器（ListItem、Row）也挂 .onClick，注释或自检按「点子组件会冒泡到行」推理；父子都要响应却没有 .parallelGesture(...)
