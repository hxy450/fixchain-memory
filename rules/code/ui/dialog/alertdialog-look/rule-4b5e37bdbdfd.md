# AlertDialog 按钮条按框架布局落位成右簇，按钮带框架的 inset 和内距

审的是：代码
触发（任一种）：
- 读到：框架 AlertDialog 的 setPositiveButton / setNegativeButton（按钮条布局 alert_dialog_button_bar_material）；写错的样子：按钮条 Row 写成 [negative][Blank()][positive]，取消键被推到左边缘；或按钮写成无内距的 Text
适用范围：用自绘卡片复刻框架 AlertDialog 的按钮条时
做法：
- 按布局子项顺序落位 [neutral][Blank()][negative][positive]，Blank 放在 negative 之前；规格里的「负左正右」只表示右簇内的相对顺序；写完把 Row 子项顺序与布局逐项对一遍
- 按钮按 Widget.Material.Button.ButtonBar.AlertDialog 复刻：最小宽 64、最小高 48，外 inset 左右 4 上下 6，内距左右 8 上下 4；工程里已有共享对话框按钮组件的直接复用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ButtonBarLayout 子项：button3（buttonBarNeutralButtonStyle）→ Space（layout_weight=1）→ button2（Negative）→ button1（Positive）：源端按钮条的排位（出处：Android SDK 平台资源 data/res/layout/alert_dialog_button_bar_material.xml，button3、spacer、button2、button1（按应用的 compileSdk 取对应平台））
- Widget.Material.Button.ButtonBar.AlertDialog：minWidth = alert_dialog_button_bar_width 64dp，minHeight = alert_dialog_button_bar_height 48dip：按钮的最小尺寸（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.Button.ButtonBar.AlertDialog；data/res/values/dimens.xml，alert_dialog_button_bar_width（按应用的 compileSdk 取对应平台））
- btn_default_mtrl_shape：inset 左右 button_inset_horizontal_material（4dp）、上下 button_inset_vertical_material 6dp；padding 左右 button_padding_horizontal_material 8dp、上下 control_padding_material 4dp：无边框按钮的外 inset 和内距（出处：Android SDK 平台资源 data/res/drawable/btn_default_mtrl_shape.xml；data/res/values/dimens_material.xml，button_padding_horizontal_material（按应用的 compileSdk 取对应平台））
- 改为 [Blank][取消][确定] 并换成共享按钮组件后与源端一致：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9d195db79dc4cccc7d1a（Sokoban）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 4；取值 4 ← 诊断
