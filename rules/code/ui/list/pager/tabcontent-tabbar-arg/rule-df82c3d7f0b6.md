# tabBar 传了 { title } 等自造对象时，改用字符串、@Builder 或 TabBarOptions

审的是：代码
触发（任一种）：
- 写错的样子：TabContent 上写 .tabBar({ title: '…' }) 这类不在任何重载里的对象字面量，编译报 10505001 No overload matches this call
适用范围：ArkUI Tabs + TabContent 做页签，写或改 tabBar 参数时
做法：
- 纯文字页签写 .tabBar('页签文字')；自定义样式用 @Builder 方法传 .tabBar(this.某个 @Builder 方法(…))；要图标加文字用 TabBarOptions 的 { icon, text }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- tabBar(content: ComponentContent | SubTabBarStyle | BottomTabBarStyle | string | Resource | CustomBuilder | TabBarOptions): TabContentAttribute：tabBar 可接受的全部类型（@since 18 的重载）（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，TabContentAttribute.tabBar）
- tabBar(options: string | Resource | CustomBuilder | TabBarOptions): TabContentAttribute：较早的重载（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，TabContentAttribute.tabBar）
- TabBarOptions 的字段是 icon?: string | Resource 和 text?: string | Resource：对象形式只有 icon、text 两个字段，没有 title（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，TabBarOptions）
- 四处改为 .tabBar('文字') 后同次编译 BUILD SUCCESSFUL：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-11c15d99c36e52d8aa59（星途清单）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
