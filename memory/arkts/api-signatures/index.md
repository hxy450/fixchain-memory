# arkts/api-signatures

调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数，成员名、所属类型与返回可空性的声明核对，依赖单位、默认行为与作用范围时读到字段注释而不以签名推定等价（含 measureTextSize 的 vp 入参与 px 返回）：@BuilderParam 槽内容与声明默认值的写法（箭头闭包只调用 @Builder、this 绑定），intl 格式化等接口不能省略的参数，源端单调计时的目标 API

[上一级](../index.md)

## 本级经验

- [为 TabContent 写页签时按 tab_content.d.ts 的 tabBar 重载传值，不传 { title } 对象](lesson-b402fa546504a1dd6db7.lesson.md)
  - 时机：页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时
  - 情境：目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。
- [传给 ArkUI 属性方法的值按其实际重载定型，不传 string | Resource 联合值](lesson-63660a8304f7d3920bfc.lesson.md)
  - 时机：规格提取阶段定义页面派生状态的类型，或页面实现阶段把派生状态接到 ArkUI 组件属性方法时；批量横切改动中把其他页面的修饰链模板复用到本文件时
  - 情境：源端文本属性（如 contentDescription）的值一部分来自字符串资源、一部分来自运行时拼出的字符串，迁移时准备用一个派生状态（getter / @Computed）同时承载 Resource 与 string，再传给属性方法（如 accessibilityText）。也包括数据类字段为方便声明成 ResourceStr（实际各分支都赋 $r() 资源），再把字段传给 accessibilityText 一类只有分开 string/Resource 重载的属性方法；以及跨文件复用修饰链时，参照页面的字段是 Resource，本文件对应字段却声明为 ResourceStr。
  - 例外：目标方法在当前 SDK 声明中有参数类型覆盖整个联合的重载（例如参数声明为 ResourceStr），此时可直接传入
- [依赖 API 的单位、默认行为或作用范围写契约或代码时，源端与目标端都读到声明注释或文档的语义说明，不以签名存在推定等价](lesson-f5cf8413ebea57f3b415.lesson.md)
  - 时机：规格提取、实现或接线阶段，准备依赖某个 API（源端或目标端）的数值单位、默认是否占位、对子节点的作用、单行与多行排版语义写映射契约或代码时，例如 ShadowOptions 半径与偏移、hitTestBehavior 的 HitTestMode、Compose lineHeight、根 Navigation 标题栏是否占位、同名接口的不同重载
  - 情境：当前疑点涉及数值单位（px 还是 vp）、默认是否占位、对子节点的作用、单行与多行的排版语义等；查询只返回同名签名、字段声明行或接口前言，或 grep 过滤掉了紧邻的注释行；或同名接口有多个重载（如按 Resource 对象与按数字 id 取资源字符串），查询只证明它们都存在。
  - 例外：当前输入已有适用版本下的明确规则或已成立实现时，直接复用，无需重复查证或补写证明材料。
- [写 SDK 调用前按本地 .d.ts 核对成员名、所属类型、调用链每一跳与返回可空性，不凭记忆写、不靠编译门兜底](lesson-6e558834938be19c04e2.lesson.md)
  - 时机：页面或组件实现阶段，写组件构造选项、属性方法参数、需实现的 SDK 接口或 UIContext、状态存储一类调用时，尤其在禁止编译的批次里，或准备“先写、等编译门报错再改”时
  - 情境：映射参考与规格只给组件、接口名而不给成员签名；写者准备凭记忆或 Android 命名填写选项字段名、参数类型、接口方法名或链式调用，或只看到一行 grep 命中的声明；本机 SDK 的 ets/component、ets/api 下 .d.ts 可以读取。也包括派工要求颜色、尺寸一律经 $r 资源绑定，或参照同批尚未编译的兄弟页、rg 到的零散用法改写参数。
- [向 @BuilderParam 槽传内容用箭头闭包只调用 @Builder，不传 this.xxx 方法引用、不在闭包里直接实例化组件](lesson-7d643db6ab406ae64c77.lesson.md)
  - 时机：界面实现、收敛改写或编译修复阶段，把页面 @Builder 内容或自定义组件交给自定义容器组件（Scaffold、Card、Surface、下拉刷新一类）的 @BuilderParam，或把原本内联在系统容器尾随闭包里的内容改交给新封装的公共组件，或为消除尾随闭包编译错误改写传参方式时；在组件内为可选 @BuilderParam 声明默认值时
  - 情境：目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 读取页面状态（如列表数据、弹窗变体）或调用其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。仓内可能已有 content: this.XxxBuilder 直传的先例。也包括槽内容本身含自定义组件（共享容器层层嵌套时把中间层组件直接写在 content: () =&gt; { Inner({...}) } 里），以及为可选插槽写空默认值时准备用箭头函数。
- [改写 getCurrencyInstance() 为 intl.NumberFormat 时显式传 currency 代码，不靠 locale 推导币种](lesson-19cedec8ad1bc4b08b2c.lesson.md)
  - 时机：实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时
  - 情境：源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。
  - 例外：应用需要多币种或按用户地区切换币种时，不能用固定符号拼接代替格式化器
- [源端单调计时映射到 getUptime 并按是否计入深睡眠选 TimeType，不用 performance.now 或 Date.now](lesson-ce456d60534d97524aa4.lesson.md)
  - 时机：规格提取阶段为 System.nanoTime、SystemClock.elapsedRealtime 等源端系统计时 API 选目标 API 或写平台差异时；实现或编译修复阶段，时钟映射在当前 SDK 中不存在、需要换时钟源时
  - 情境：源端帧动画或计时用 System.nanoTime（CLOCK_MONOTONIC）求帧间隔与进度；目标 ArkTS 把时钟封装在单点函数里，规格映射写了 Web API（performance.now），构建报找不到符号或 Kit 无导出。也包括后台计时用 elapsedRealtime（计入深睡眠）记录起点与偏移，规格准备映射为墙钟，并写“平台未开放跨休眠单调时钟”。
- [用 measureTextSize 按宽度判断折行时，constraintWidth 直接传 vp 数值，返回的宽高是 px，比较前换算到同一单位](lesson-b7b935e86195ed85927d.lesson.md)
  - 时机：界面实现或返修阶段，用 UIContext.getMeasureUtils().measureTextSize 计算文本宽高、按列宽判断折行行数时
  - 情境：源端 wrap_content 的 TextView 在列宽内折行会变高并下推后续内容；目标用 measureTextSize 先测单行高、再按列宽测折行高，列宽是布局里的 vp 数值。
