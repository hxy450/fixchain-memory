# arkts/api-signatures

调用 ArkUI 组件属性方法或 SDK 接口时的参数类型与重载匹配

[上一级](../index.md)

## 本级经验

- [TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象](lesson-b402fa546504a1dd6db7.lesson.md)
  - 时机：页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时
  - 情境：目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。
- [传给 ArkUI 属性方法的值按其实际重载定型，不传 string | Resource 联合值](lesson-63660a8304f7d3920bfc.lesson.md)
  - 时机：规格提取阶段定义页面派生状态的类型，或页面实现阶段把派生状态接到 ArkUI 组件属性方法时
  - 情境：源端文本属性（如 contentDescription）的值一部分来自字符串资源、一部分来自运行时拼出的字符串，迁移时准备用一个派生状态（getter / @Computed）同时承载 Resource 与 string，再传给属性方法（如 accessibilityText）。
  - 例外：目标方法在当前 SDK 声明中有参数类型覆盖整个联合的重载（例如参数声明为 ResourceStr），此时可直接传入
