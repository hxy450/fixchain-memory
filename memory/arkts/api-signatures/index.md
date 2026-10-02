# arkts/api-signatures

调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数，成员名、所属类型与返回可空性的声明核对，依赖单位、默认行为与作用范围时读到字段注释而不以签名推定等价：@BuilderParam 槽内容的写法（箭头闭包只调用 @Builder、this 绑定），intl 格式化等接口不能省略的参数

[上一级](../index.md)

## 本级经验

- [ArkTS intl.NumberFormat 用 style: 'currency' 时必须给 currency 代码，不会像 Java getCurrencyInstance 那样按 locale 推导币种](lesson-19cedec8ad1bc4b08b2c.lesson.md)
  - 时机：实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时
  - 情境：源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。
  - 例外：应用需要多币种或按用户地区切换币种时，不能用固定前缀代替格式化器
- [TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象](lesson-b402fa546504a1dd6db7.lesson.md)
  - 时机：页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时
  - 情境：目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。
- [不能编译的生成批次写 SDK 调用前，按本地 .d.ts 核对成员名、所属类型、调用链每一跳与返回可空性](lesson-6e558834938be19c04e2.lesson.md)
  - 时机：页面或组件实现阶段，在禁止编译的转换批次里写组件构造选项、属性方法参数、需实现的 SDK 接口，或 UIContext、状态存储一类调用时
  - 情境：转换派工禁止编译或构建，映射参考与规格只给组件、接口名而不给成员签名；写者准备凭记忆填写选项字段名、参数类型、接口方法名或链式调用，或只看到一行 grep 命中的声明；本机 SDK 的 ets/component、ets/api 下 .d.ts 可以读取。
- [传给 ArkUI 属性方法的值按其实际重载定型，不传 string | Resource 联合值](lesson-63660a8304f7d3920bfc.lesson.md)
  - 时机：规格提取阶段定义页面派生状态的类型，或页面实现阶段把派生状态接到 ArkUI 组件属性方法时；批量横切改动中把其他页面的修饰链模板复用到本文件时
  - 情境：源端文本属性（如 contentDescription）的值一部分来自字符串资源、一部分来自运行时拼出的字符串，迁移时准备用一个派生状态（getter / @Computed）同时承载 Resource 与 string，再传给属性方法（如 accessibilityText）。也包括数据类字段为方便声明成 ResourceStr（实际各分支都赋 $r() 资源），再把字段传给 accessibilityText 一类只有分开 string/Resource 重载的属性方法；以及跨文件复用修饰链时，参照页面的字段是 Resource，本文件对应字段却声明为 ResourceStr。
  - 例外：目标方法在当前 SDK 声明中有参数类型覆盖整个联合的重载（例如参数声明为 ResourceStr），此时可直接传入
- [依赖 API 的单位、默认行为或作用范围时读到字段注释与语义说明，不以签名存在推定等价](lesson-f5cf8413ebea57f3b415.lesson.md)
  - 时机：规格提取、实现或接线阶段，准备依赖某个 API 的单位、默认行为、作用范围或字段含义写映射契约或代码时
  - 情境：当前疑点涉及数值单位（px 还是 vp）、默认是否占位、对子节点的作用、单行与多行的排版语义等；查询只返回同名签名、字段声明行或接口前言，或 grep 过滤掉了紧邻的注释行。
  - 例外：当前输入已有适用版本下的明确规则或已成立实现时，直接复用，无需重复查证或补写证明材料。
- [向 @BuilderParam 槽传内容时用箭头闭包只调用 @Builder：不传 this.xxx 方法引用，也不在闭包里直接实例化自定义组件](lesson-7d643db6ab406ae64c77.lesson.md)
  - 时机：界面实现、收敛改写或编译修复阶段，把页面 @Builder 内容或自定义组件交给自定义容器组件（Scaffold、Card、Surface、下拉刷新一类）的 @BuilderParam，或把原本内联在系统容器尾随闭包里的内容改交给新封装的公共组件，或为消除尾随闭包编译错误改写传参方式时
  - 情境：目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 读取页面状态（如列表数据）或调用其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。仓内可能已有 content: this.XxxBuilder 直传的先例。也包括槽内容本身含自定义组件，如共享容器层层嵌套时把中间层组件直接写在 content: () =&gt; { Inner({...}) } 里，而工程已有 content: () =&gt; { this.xxx() } 的范例。
