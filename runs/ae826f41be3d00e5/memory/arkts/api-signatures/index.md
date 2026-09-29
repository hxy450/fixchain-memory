# arkts/api-signatures

调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数：@BuilderParam 传入 builder 的写法与 this 绑定，intl 格式化等接口不能省略的参数

[上一级](../index.md)

## 本级经验

- [ArkTS intl.NumberFormat 用 style: 'currency' 时必须给 currency 代码，不会像 Java getCurrencyInstance 那样按 locale 推导币种](lesson-19cedec8ad1bc4b08b2c.lesson.md)
  - 时机：实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时
  - 情境：源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。
  - 例外：应用需要多币种或按用户地区切换币种时，不能用固定前缀代替格式化器
- [TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象](lesson-b402fa546504a1dd6db7.lesson.md)
  - 时机：页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时
  - 情境：目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。
- [传给 ArkUI 属性方法的值按其实际重载定型，不传 string | Resource 联合值](lesson-63660a8304f7d3920bfc.lesson.md)
  - 时机：规格提取阶段定义页面派生状态的类型，或页面实现阶段把派生状态接到 ArkUI 组件属性方法时
  - 情境：源端文本属性（如 contentDescription）的值一部分来自字符串资源、一部分来自运行时拼出的字符串，迁移时准备用一个派生状态（getter / @Computed）同时承载 Resource 与 string，再传给属性方法（如 accessibilityText）。
  - 例外：目标方法在当前 SDK 声明中有参数类型覆盖整个联合的重载（例如参数声明为 ResourceStr），此时可直接传入
- [向子组件 @BuilderParam 传页面自己的 @Builder 时用箭头闭包包装，不传 this.xxx 方法引用](lesson-7d643db6ab406ae64c77.lesson.md)
  - 时机：界面实现或编译修复阶段，把页面 @Builder 内容交给自定义容器组件（Scaffold、Card 一类）的 @BuilderParam，或为消除尾随闭包编译错误改写传参方式时
  - 情境：目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 调用页面状态或其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。
