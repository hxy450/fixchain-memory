# Material3 底栏选中标签加粗，徽标宿主收到图标尺寸后 TopEnd 锚定

审的是：代码
触发（任一种）：
- 读到：BottomNavigationView（Material3 主题、没有 bottomNavigationStyle 覆写），itemTextAppearanceActive / itemTextAppearanceInactive 指向 TextAppearance.Material3.* 系的样式；写错的样子：目标端底栏选中和未选标签都写 FontWeight.Medium；徽标宿主 Stack({ alignContent: Alignment.TopEnd }) 设成 48×32 包住 24×24 图标，徽标不在图标右上
适用范围：Material3 主题的 BottomNavigationView 迁成 ArkUI 自绘底栏时的标签字重和徽标位置
做法：
- 选中项标签写 .fontWeight(FontWeight.Bold)（对应 itemTextAppearanceActiveBoldEnabled 的加粗），未选项按源 TextAppearance 的字重
- 徽标宿主写成 Stack({ alignContent: Alignment.TopEnd }).width(24).height(24)，和图标同尺寸，徽标放在里面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Base.Widget.Material3.BottomNavigationView 的 itemIconSize = m3_comp_navigation_bar_icon_size = 24dp：图标尺寸，徽标宿主取同一尺寸（出处：com.google.android.material:material 包内 res/values/values.xml，Base.Widget.Material3.BottomNavigationView、m3_comp_navigation_bar_icon_size（按应用依赖的版本））
- NavigationBarView 有布尔属性 itemTextAppearanceActiveBoldEnabled：选中标签是否加粗由它控制，资源里没给默认值（出处：com.google.android.material:material 包内 res/values/values.xml，NavigationBarView 的 itemTextAppearanceActiveBoldEnabled（按应用依赖的版本））
- alignContent?: Alignment：Stack 子组件的对齐，Alignment.TopEnd 让徽标贴右上（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- FontWeight.Bold 相当于 700：选中标签的加粗（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，FontWeight.Bold）
- 徽标宿主改为 24×24、选中标签改为 Bold 后和安卓一致：验证过的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a3dc4d0187d7ddc456e8（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
