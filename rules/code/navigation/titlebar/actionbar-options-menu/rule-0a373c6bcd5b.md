# AppCompat 下菜单用 android:showAsAction 时，全部项进右上 ⋮ 溢出菜单，不做成标题栏图标

审的是：代码
触发（任一种）：
- 读到：菜单 XML 的 <item> 用 android:showAsAction="ifRoom"（常带 tools:ignore="AppCompatResource"），Activity 基于 AppCompat；写错的样子：这些项被做成标题栏右侧的图标按钮，或 NavDestination 的 .menus 图标项
适用范围：源端 Activity 基于 AppCompat、菜单 XML 用 android: 命名空间的 showAsAction 时
做法：
- 全部菜单项按菜单 XML 的顺序放进标题栏右上 ⋮ 按钮弹出的溢出菜单；不转成标题栏图标，也不用 .menus 图标项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- appcompat 的 MenuItem styleable 声明的是不带 android: 前缀的 showAsAction（app: 命名空间）：AppCompat 读 app:showAsAction，android:showAsAction 被忽略（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，declare-styleable MenuItem 的 showAsAction（按应用依赖的版本））
- AppCompat 下 android:showAsAction 被忽略，所有项进 ⋮ 溢出菜单；修复改为右上 ⋮ 弹层：按这一语义替换后与源端一致（出处：卡里修好并验证过）
- menus(value: Array<NavigationMenuItem> | CustomBuilder): NavDestinationAttribute：NavDestination 标题栏菜单；这类图标菜单不对应源端的溢出菜单（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.menus）
来源：1 张卡，1 个应用
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 1 步 ← 建议 5、诊断；取值 2 ← 诊断
