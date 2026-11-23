# arkts/api-signatures

调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数，成员名、所属类型与返回可空性的声明核对，依赖单位、默认行为与作用范围时读到字段注释而不以签名推定等价：@BuilderParam 槽内容的写法（箭头闭包只调用 @Builder、this 绑定），intl 格式化等接口不能省略的参数，源端单调计时的目标 API；cryptoFramework 摘要的空输入

[上一级](../index.md)

## 本级经验

- [ArkTS intl.NumberFormat 用 style: 'currency' 时必须给 currency 代码，不会像 Java getCurrencyInstance 那样按 locale 推导币种](lesson-19cedec8ad1bc4b08b2c.lesson.md)
  - 时机：实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时
  - 情境：源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。
  - 例外：应用需要多币种或按用户地区切换币种时，不能用固定前缀代替格式化器；基线显示 $ 而 currencyDisplay 默认的 symbol 显示成 US$ 时，先改用 currencyDisplay: 'narrowSymbol'（文档以 USD 为例：symbol 为 -US$12,300.00，narrowSymbol 为 -$12,300.00），保留格式化器的分组和小数规则；它也拿不到基线形式时，才按第 2 步直接格式化。
- [MessageDigest 改用 cryptoFramework Md 时，空输入不调用 update，直接返回该算法的空输入摘要](lesson-31b2022cb16eba3d9f1e.lesson.md)
  - 时机：实现阶段，把对可能为空的字符串求摘要（缓存键、内容哈希）的 MessageDigest 调用改写为 cryptoFramework.createMd 时
  - 情境：源端对可能为空的字段（标题、摘要文本等）无条件求摘要，空串是正常路径；目标用 cryptoFramework.createMd + update({ data }) + digest()。
  - 例外：第 1 步给的常量是 SHA-256 的小写十六进制形式；源端用的是别的算法（如 MD5、SHA-1），或把摘要编码成大写十六进制、Base64 等其他形式时，空输入要返回同一算法、同一编码下的值，和非空路径的输出格式一致，否则同一内容得到的键与源端不同。
- [TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象](lesson-b402fa546504a1dd6db7.lesson.md)
  - 时机：页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时
  - 情境：目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。
  - 例外：只改以对象字面量写页签标题（如 { title }）的地方；已经以 @Builder（CustomBuilder）、TabBarOptions 或 SubTabBarStyle/BottomTabBarStyle 写的页签照原样保留，不为统一写法改成纯字符串——改成字符串会丢掉原有的图标、选中色等样式。；API 18 起 tabBar 还接受 ComponentContent；工程最低 API 不低于 18 时，已有的 ComponentContent 页签不算错。
- [传给 ArkUI 属性方法的值按其实际重载定型，不传 string | Resource 联合值](lesson-63660a8304f7d3920bfc.lesson.md)
  - 时机：规格提取阶段定义页面派生状态的类型，或页面实现阶段把派生状态接到 ArkUI 组件属性方法时；批量横切改动中把其他页面的修饰链模板复用到本文件时
  - 情境：源端文本属性（如 contentDescription）的值一部分来自字符串资源、一部分来自运行时拼出的字符串，迁移时准备用一个派生状态（getter / @Computed）同时承载 Resource 与 string，再传给属性方法（如 accessibilityText）。也包括数据类字段为方便声明成 ResourceStr（实际各分支都赋 $r() 资源），再把字段传给 accessibilityText 一类只有分开 string/Resource 重载的属性方法；以及跨文件复用修饰链时，参照页面的字段是 Resource，本文件对应字段却声明为 ResourceStr。
  - 例外：目标方法在当前 SDK 声明中有参数类型覆盖整个联合的重载（例如参数声明为 ResourceStr），此时可直接传入
- [依赖 API 的单位、默认行为或作用范围时，源端与目标端都读到语义说明：行为级契约写出源 API 实际的作用区域与度量，不只抄字面参数，也不以签名存在推定等价](lesson-f5cf8413ebea57f3b415.lesson.md)
  - 时机：规格提取、实现或接线阶段，准备依赖某个 API（源端或目标端）的单位、默认行为、作用范围或字段含义写映射契约或代码时
  - 情境：当前疑点涉及数值单位（px 还是 vp）、默认是否占位、对子节点的作用、单行与多行的排版语义等；查询只返回同名签名、字段声明行或接口前言，或 grep 过滤掉了紧邻的注释行。也包括同名接口的多个重载（如按 Resource 对象与按数字 id 取资源字符串），查询只证明它们都存在。也包括源端在 Button/AppCompatButton 子类或带 style 的 TextView 上调用 setAutoSizeTextTypeUniformWithConfiguration，规格行只写字号区间与“自适应块宽”；以及目标用 measureTextSize 一类测量 API，参数与返回值单位不同。
  - 例外：当前输入已有适用版本下的明确规则或已成立实现时，直接复用，无需重复查证或补写证明材料。；同名的阴影参数单位不一定相同：ShadowOptions（含 shadow、textShadow、弹窗与半模态的 shadow）按 px，要 vp2px；DataPanel、Gauge 的阴影选项（MultiShadowOptions）按 vp，已按 vp 写的数值保留，不套 vp2px。
- [向 @BuilderParam 槽传内容时用箭头闭包只调用 @Builder：不传 this.xxx 方法引用，也不在闭包里直接实例化自定义组件](lesson-7d643db6ab406ae64c77.lesson.md)
  - 时机：界面实现、收敛改写或编译修复阶段，把页面 @Builder 内容或自定义组件交给自定义容器组件（Scaffold、Card、Surface、下拉刷新一类）的 @BuilderParam，或把原本内联在系统容器尾随闭包里的内容改交给新封装的公共组件，或为消除尾随闭包编译错误改写传参方式时
  - 情境：目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 读取页面状态（如列表数据、弹窗变体）或调用其他 builder（如通用弹窗容器 contentBuilder 接收的、按变体分派内容的 builder），名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。仓内可能已有 content: this.XxxBuilder 直传的先例。也包括槽内容本身含自定义组件，如共享容器层层嵌套时把中间层组件直接写在 content: () =&gt; { Inner({...}) } 里，而工程已有 content: () =&gt; { this.xxx() } 的范例。
  - 例外：@BuilderParam 带参数时（如 row: (item: T) =&gt; void），箭头闭包要保留同样的参数列表并原样转交：row: (item: T) =&gt; { this.rowBuilder(item) }；不要写成无参的 () =&gt; { this.rowBuilder() }——无参函数能赋给带参类型，编译照常通过，参数却被丢掉。；只管以 this.xxx 传入的成员 @Builder；直接传全局 @Builder 函数（不经 this）不涉及 this 改绑，不必为此改成闭包。
- [源端单调计时（System.nanoTime、SystemClock.elapsedRealtime）映射到 systemDateTime.getUptime，并按是否计入深睡眠选 TimeType：不写未经 SDK 核实的 performance.now，也不退回会随校时跳变的 Date.now](lesson-ce456d60534d97524aa4.lesson.md)
  - 时机：规格提取阶段为 System.nanoTime、SystemClock.elapsedRealtime 等源端系统计时 API 选目标 API 或写平台差异时；实现或编译修复阶段，时钟映射在当前 SDK 中不存在、需要换时钟源时
  - 情境：源端帧动画或计时用 System.nanoTime（CLOCK_MONOTONIC）求帧间隔与进度；目标 ArkTS 把时钟封装在单点函数里，规格映射写了 Web API（performance.now），构建报找不到符号或 Kit 无导出。也包括后台计时用 elapsedRealtime（计入深睡眠）记录起点与偏移，规格准备映射为墙钟，并写“平台未开放跨休眠单调时钟”。
  - 例外：只管源端取单调时钟的调用；源端用 System.currentTimeMillis 取墙钟时间（显示日期时间、存盘时间戳、跨重启比较）的地方，目标端继续用 Date.now 或 systemDateTime.getTime，不改成 getUptime——开机时长重启后从零算起，不能当日期用。；帧间隔已经取自 displaySync 帧回调 IntervalInfo 的 timestamp/targetTimestamp 时，它本身是系统启动以来单调递增的纳秒时间，不需要再换成 getUptime。
