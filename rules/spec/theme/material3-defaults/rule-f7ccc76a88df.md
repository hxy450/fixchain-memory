# 规格的设计系统节把 Material3 组件度量写成具体值

审的是：规格
触发（任一种）：
- 读到：源主题 parent 链到 Theme.Material3.*，界面用 MaterialToolbar、BottomNavigationView；写错的样子：设计系统节只写「Material3 为基、尺寸来自 dimens + Material3 默认」，没写工具栏高度、标题外观、内缩、底栏选中字重和徽标锚点的具体值
适用范围：规格提取阶段写设计系统节、源主题是 Material3 时
做法：
- 设计系统节列一张组件度量表：工具栏高 64dp、标题 TitleLarge 22sp 常规、标题起点 16dp（有导航图标约 60dp）、底栏选中标签加粗、徽标锚在 24dp 图标右上，并注明出自哪个主题和组件样式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Material3 主题 actionBarSize = 64dp：工具栏高度（出处：com.google.android.material:material 包内 res/values/values.xml，m3_comp_top_app_bar_small_container_height（按应用依赖的版本））
- TextAppearance.M3.Sys.Typescale.TitleLarge 的 android:textSize 22sp：工具栏标题字号（出处：com.google.android.material:material 包内 res/values/values.xml，TextAppearance.M3.Sys.Typescale.TitleLarge（按应用依赖的版本））
来源：1 张卡，1 个应用
- case-a3dc4d0187d7ddc456e8（AntennaPod）：做法第 1 步 ← 建议 5、建议 2
