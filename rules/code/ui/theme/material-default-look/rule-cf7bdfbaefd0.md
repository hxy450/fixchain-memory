# Material 控件没显式写外观属性时，列出主题和库的默认外观，逐项对照 ArkUI 默认值显式设置

审的是：代码
触发（任一种）：
- 读到：CheckBox、RadioButton、MaterialButton、TabLayout、EditText、Spinner 等 Material 控件在布局里没写外观属性，外观来自主题或组件库默认 style；写错的样子：目标组件只直译了 XML 里显式写的属性（checked、onChange、颜色），形状、指示器、字距、底色、标签样式等都留着 ArkUI 默认值
适用范围：界面实现阶段把 Android Material 控件映射成 ArkUI 组件、确定外观属性时
做法：
- 除 XML 显式属性外，先列出该控件在主题和组件库里的默认外观（复选框形状、单选指示器、按钮字距与前景色、Tab 标签字号字重与指示条、输入框下划线、Spinner 无底色），逐项和 ArkUI 组件的默认值对照，不同的显式设置
针对本应用要查的：
- 源控件的默认外观：源工程主题里该控件的默认 style 属性（如 checkboxStyle、materialButtonStyle、tabStyle），再到 com.google.android.material:material 包内 res/values/values.xml 找该 style 的 item（按应用依赖的版本）；顺着 parent 和 textAppearance 读出形状、颜色 selector、字号字重、字距、背景，逐项记下
- 目标组件的默认外观：鸿蒙 SDK 的 ets/component 下该组件的 .d.ts 和 OpenHarmony 文档里该组件的属性表，看各属性的默认值；和源端逐项比，默认值不同的在目标代码里显式写出
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 1
