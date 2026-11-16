# AppCompat 菜单项用 android:showAsAction 时，规格写成溢出菜单，不写成图标

审的是：规格
触发（任一种）：
- 读到：菜单 XML 的 <item> 用 android:showAsAction="ifRoom" 并带 tools:ignore="AppCompatResource"；写错的样子：规格写「ActionBar 图标按钮形态，置于标题栏右侧」或「showAsAction=ifRoom 的图标按钮，等价 ActionBar」
适用范围：规格提取时，写 AppCompat Activity 的菜单形态
做法：
- 规格写明：「AppCompat 下 android:showAsAction 被忽略，全部菜单项在右上 ⋮ 溢出菜单」，并按菜单 XML 列出项的顺序
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- appcompat 的 MenuItem styleable 声明的是不带 android: 前缀的 showAsAction：android: 命名空间的 showAsAction 不被 AppCompat 读取（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，declare-styleable MenuItem 的 showAsAction（按应用依赖的版本））
来源：1 张卡，1 个应用
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 1 步 ← 建议 5、诊断
