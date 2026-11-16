# 注释里记了尺寸和边距而修饰链没有应用时，按缺失补上

审的是：代码
触发（任一种）：
- 写错的样子：代码注释写着 mS16、mB20 这类边距或尺寸，对应组件的修饰链里没有 .margin(...) / .padding(...) / .width(...) 等对应调用
适用范围：界面实现写完后，注释里列了源端尺寸、边距的组件
做法：
- 把注释里列出的尺寸和边距逐项对照实际修饰链；注释有而代码没有的按缺失处理，补成对应的 .margin / .padding / .width / .height 调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- margin(value: Margin | Length | LocalizedMargin): T：外边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- padding(value: Padding | Length | LocalizedPadding): T：内边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
来源：1 张卡，1 个应用
- case-c85d8667f78c2cc8f53a（免费来电多多）：做法第 1 步 ← 建议 3
